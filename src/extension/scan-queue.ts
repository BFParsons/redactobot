/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview A queue that runs one on-device model task at a time and gives
 * paste checks priority over diagnostics.
 */

import {abortable} from '../core/abortable';

type Kind = 'paste' | 'diagnostic';
interface Task {
  kind: Kind;
  controller: AbortController;
  stage: string;
  started: number;
  run(): Promise<unknown>;
  resolve(value: unknown): void;
  reject(error: unknown): void;
  cancel(): void;
}

/**
 * One native request at a time. Diagnostics must never hold up a real paste.
 * Cancellation releases both queued and running work even if a native promise
 * never settles. Late completion cannot release a newer task's slot.
 */
export class ScanQueue {
  private active?: Task;
  private waiting: Task[] = [];

  /**
   * Returns the running task's kind, stage and elapsed time, and the number of
   * tasks waiting.
   */
  snapshot() {
    return {
      active: this.active
        ? {
            kind: this.active.kind,
            stage: this.active.stage,
            elapsedMs: Math.round(performance.now() - this.active.started),
          }
        : null,
      waiting: this.waiting.length,
    };
  }
  /** Records the stage of the running task, if `controller` belongs to it. */
  stage(controller: AbortController, stage: string) {
    if (this.active?.controller === controller) this.active.stage = stage;
  }
  /**
   * Queues `run` and resolves with its result. A diagnostic is rejected when
   * any task is running or waiting; a paste aborts a running diagnostic.
   * Aborting `controller` rejects the task whether it is waiting or running.
   */
  run<T>(
    kind: Kind,
    controller: AbortController,
    run: () => Promise<T>,
  ): Promise<T> {
    if (kind === 'diagnostic' && (this.active || this.waiting.length)) {
      return Promise.reject(
        new Error('A paste check is running. Try this test after it finishes.'),
      );
    }
    if (kind === 'paste' && this.active?.kind === 'diagnostic') {
      this.active.controller.abort(
        new Error('The test stopped to let a paste check run.'),
      );
    }
    return new Promise<T>((resolve, reject) => {
      const task: Task = {
        kind,
        controller,
        run,
        resolve: value => resolve(value as T),
        reject,
        started: 0,
        stage: 'starting',
        cancel: () => {
          const index = this.waiting.indexOf(task);
          if (index >= 0) {
            this.waiting.splice(index, 1);
            controller.signal.removeEventListener('abort', task.cancel);
            reject(controller.signal.reason);
          }
        },
      };
      if (controller.signal.aborted) {
        reject(controller.signal.reason);
        return;
      }
      controller.signal.addEventListener('abort', task.cancel, {once: true});
      this.waiting.push(task);
      this.next();
    });
  }
  private next() {
    if (this.active || !this.waiting.length) return;
    const task = this.waiting.shift()!;
    this.active = task;
    task.started = performance.now();
    void abortable(
      Promise.resolve().then(() => {
        task.controller.signal.throwIfAborted();
        return task.run();
      }),
      task.controller.signal,
    )
      .then(task.resolve, task.reject)
      .finally(() => {
        task.controller.signal.removeEventListener('abort', task.cancel);
        if (this.active === task) this.active = undefined;
        this.next();
      });
  }
}
