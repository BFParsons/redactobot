/**
 * @license
 * Copyright 2026 B Parsons
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview The `<redactobot-app>` element, which is the whole web app UI:
 * composing or importing a document, reviewing what was found, and the answer
 * view.
 */

import {LitElement, html, nothing, type TemplateResult} from 'lit';
import {customElement, state} from 'lit/decorators.js';
import {live} from 'lit/directives/live.js';
import {styleMap} from 'lit/directives/style-map.js';
import {
  ACCURACY_TIERS,
  DATA_CLASSES,
  DEFAULT_CLASSES,
  FRAMEWORKS,
  KEEP,
  PROFESSIONAL_DUTIES,
  coverage,
  dataClassById,
  detectorById,
  frameworkById,
  planForClasses,
} from '../taxonomy/taxonomy.js';
import {
  NO_TOPICS,
  applyRedactions,
  buildDetections,
  chunkText,
  restore,
  unexplainedCapitals,
  type Detection,
  type Names,
  type Topics,
} from './core/redact';
import {
  deviceCold,
  deviceStatus,
  detectNames,
  detectTopics,
  prepareDevice,
  warmDevice,
  wakeDevice,
} from './core/ai';
import {askCloud, cleanupCloud, cloudSetupProblem} from './core/cloud-client';
import {
  prepareCloudInput,
  approveCleanedResult,
  type CloudCleanup,
} from './core/cloud-gate';
import {privacyBucket} from './core/privacy-buckets';
import {extract, prepareModel} from './extension/model';
import {makeReport, cleanedText} from './extension/policy';
import {
  boxFill,
  defaultExemption,
  EXEMPTIONS,
  exemptionFor,
  exemptionsUsed,
  foiaText,
  RELEASE,
  type FoiaSettings,
} from './core/foia';
import {namespace, type ScanReport} from './extension/protocol';
import {
  ACCEPT,
  ACCEPT_LABEL,
  ImportError,
  importFile,
  type Imported,
} from './core/import';
import {JazzPlayer} from './core/jazz';
import {
  loadingMessage,
  shuffledMessages,
  warmPercent,
} from './core/loading-messages';
import {SAMPLES} from './core/samples';
import {icon, type IconName} from './icons';

// Typewriter timing: words revealed per frame, red flash, then placeholder
// typing.
const TYPE_WORDS_PER_FRAME = 2;
const TYPE_FLASH_MS = 150;
const TYPE_SWAP_MS = 100;

/**
 * The data types whose checks a regulation calls for (planned, unbuilt checks
 * are ignored).
 */
function classesForRule(id: string): string[] {
  const f = frameworkById(id);
  if (!f) return [];
  const needed = new Set(
    f.requirements
      .flatMap((r: {detectors: string[]}) => r.detectors)
      .filter((d: string) => detectorById(d)?.status === 'ready'),
  );
  return DATA_CLASSES.filter(c =>
    c.detectors.some((d: string) => needed.has(d)),
  ).map(c => c.id);
}

type View = 'compose' | 'review' | 'answer';
interface Requirement {
  ref: string;
  text: string;
  detectors: string[];
  keep?: string;
  gap?: string;
  na?: boolean;
}
type Scan =
  | {state: 'idle'}
  | {state: 'loading'; fraction: number}
  | {state: 'running'; stage: 'names' | 'topics'; done: number; total: number}
  | {state: 'done'}
  | {state: 'skipped'; reason: 'not-needed' | 'unsupported' | 'unavailable'};

// Settings only: which rules and types of data are ticked. Never document text.
const RULES_KEY = 'redactobot.rules.v1';
// Display choices only (theme, colours, motion).
const DISPLAY_KEY = 'redactobot.display.v1';
// Output mode and exemption choices only, never document text.
const FOIA_KEY = 'redactobot.foia.v1';
/**
 * The two ways to say what gets replaced: by the rule that calls for it, or by
 * the type of data.
 */
type DataClass = (typeof DATA_CLASSES)[number];
/**
 * A measured rate as shown to the user. Never "100%": no check is right every
 * time.
 */
const shownRate = (c: DataClass) =>
  c.rate >= 0.995 ? '99%+' : `${Math.floor(c.rate * 100)}%`;
interface CloudCandidate {
  source: string;
  report: ScanReport;
  prefix: string;
  remove: string[];
  preview: string;
}

const COVER: Record<string, {icon: IconName; text: string}> = {
  covered: {icon: 'check_circle', text: 'Caught automatically'},
  partial: {icon: 'rule', text: 'Partly caught'},
  planned: {icon: 'schedule', text: 'Not built yet'},
  none: {icon: 'visibility', text: 'Check yourself'},
  na: {icon: 'block', text: 'Does not apply to text'},
};

/** The web app's root element. Renders into light DOM. */
@customElement('redactobot-app')
export class RedactobotApp extends LitElement {
  // Light DOM: global Material tokens and type scale classes apply, and text
  // selection works.
  protected createRenderRoot() {
    return this;
  }

  @state() private view: View = 'compose';
  @state() private text = '';
  @state() private openSection = {types: true, rules: false};
  @state() private classes = new Set<string>(DEFAULT_CLASSES);
  // Regulations the user ticked. Explicit, so a box is either ticked or blank
  // and always unticks; a ticked regulation whose data types are later switched
  // off is unticked too.
  @state() private rules = new Set<string>();
  @state() private names: Names = {people: [], companies: []};
  @state() private topics: Topics = NO_TOPICS;
  @state() private manual: Array<{text: string; kind: string}> = [];
  @state() private disabled = new Set<string>();
  @state() private scan: Scan = {state: 'idle'};
  @state() private scanErrors = 0;
  @state() private tab = 0;
  @state() private answerTab = 0;
  @state() private selection = '';
  @state() private question = '';
  @state() private asking = false;
  @state() private answerRaw = '';
  @state() private answerError = '';
  @state() private ruleDialog: string | null = null;
  @state() private aboutOpen = false;
  @state() private displayOpen = false;
  // Display choices: 'system' follows the computer. Saved in this browser only
  // (no document data).
  @state() private display: {
    theme: 'system' | 'light' | 'dark';
    palette: 'standard' | 'cb';
    motion: 'full' | 'reduced';
  } = {theme: 'system', palette: 'standard', motion: 'full'};
  @state() private robotPaused = false;
  // Output: placeholders for an AI chat, or a US FOIA release with boxed,
  // exemption-marked withholdings.
  @state() private output: 'ai' | 'foia' = 'ai';
  @state() private foia: FoiaSettings = {lawEnforcement: false, overrides: {}};
  @state() private scrolled = false;
  @state() private imported: Omit<Imported, 'text'> | null = null;
  @state() private importing = false;
  // Is the on-device model ready? 'off' = not needed, needs a download (which
  // takes a click) or not supported: the rules still run and nothing is
  // blocked. 'warming' blocks Find with a visible bar.
  @state() private modelState: 'checking' | 'warming' | 'ready' | 'off' =
    'checking';
  private warming?: Promise<void>;
  // Cold-start progress. Chrome reports no progress while it loads the model,
  // so the bar is an estimate from elapsed time (it eases towards 95% and jumps
  // to 100% when the model answers).
  @state() private warmStart = 0;
  @state() private warmNow = 0;
  @state() private warmReady = false;
  private warmOrder: number[] = [];
  // Optional music while the model starts: an original loop synthesised in the
  // browser. It starts only from the Play button and stops when the model is
  // ready.
  @state() private jazzOn = false;
  private jazz = new JazzPlayer();
  // Typewriter reveal: position in the original text, and the found detail
  // animating there.
  @state() private anim: {pos: number; found: Map<number, number>} | null =
    null; // found: detail start -> time revealed
  private typer = 0;
  private userScrolled = false;
  @state() private importError = '';
  @state() private dragging = false;
  private dragDepth = 0;
  @state() private copied = false;
  @state() private cloudCandidate?: CloudCandidate;
  @state() private cloudReviewed = false;
  @state() private cloudResult?: CloudCleanup;
  @state() private cloudStage = '';
  private cloudAbort?: AbortController;

  /**
   * placeholder -> real value for the last request. Memory only; cleared on
   * "Start over".
   */
  private map = new Map<string, string>();
  private sent = {doc: '', question: ''};
  private runId = 0;

  connectedCallback() {
    super.connectedCallback();
    try {
      // Settings saved before the rename to Redactobot live under the old key.
      const saved = JSON.parse(
        localStorage.getItem(RULES_KEY) ||
          localStorage.getItem('csa.rules.v1') ||
          'null',
      );
      if (
        saved?.classes &&
        (saved.pickBy === undefined || saved.pickBy === 'classes')
      ) {
        this.classes = new Set(
          (saved.classes as string[]).filter(id => dataClassById(id)),
        );
      }
      // Settings saved by the old "By rule" tab become the data types those
      // rules cover.
      else if (saved?.chosen) {
        this.classes = new Set(
          (saved.chosen as string[]).flatMap(id => classesForRule(id)),
        );
      }
      if (Array.isArray(saved?.rules)) {
        this.rules = new Set(
          (saved.rules as string[]).filter(
            id => frameworkById(id) && this.covers(id),
          ),
        );
      }
    } catch {
      /* storage unavailable: defaults apply */
    }
    // Start loading an already-downloaded on-device model now, so the first
    // scan does not wait for a cold start. No text is involved; download still
    // needs a click.
    try {
      const d = JSON.parse(localStorage.getItem(DISPLAY_KEY) || '{}');
      this.display = {
        theme: ['light', 'dark'].includes(d.theme) ? d.theme : 'system',
        palette: d.palette === 'cb' ? 'cb' : 'standard',
        motion: d.motion === 'reduced' ? 'reduced' : 'full',
      };
    } catch {
      /* storage unavailable */
    }
    try {
      const f = JSON.parse(localStorage.getItem(FOIA_KEY) || '{}');
      this.output = f.output === 'foia' ? 'foia' : 'ai';
      this.foia = {
        lawEnforcement: !!f.lawEnforcement,
        overrides:
          typeof f.overrides === 'object' && f.overrides ? f.overrides : {},
      };
    } catch {
      /* storage unavailable */
    }
    this.warmModel();
    document.addEventListener('visibilitychange', this.onVisible);
    this.keepAlive = setInterval(this.onVisible, 60_000);
    window.addEventListener('scroll', this.onScroll, {passive: true});
    document.addEventListener('selectionchange', this.onSelection);
    window.addEventListener('dragenter', this.onDragEnter);
    window.addEventListener('dragover', this.onDragOver);
    window.addEventListener('dragleave', this.onDragLeave);
    window.addEventListener('drop', this.onDrop);
    window.addEventListener('paste', this.onPaste);
  }
  disconnectedCallback() {
    this.stopJazz();
    cancelAnimationFrame(this.typer);
    this.cloudAbort?.abort();
    window.removeEventListener('dragenter', this.onDragEnter);
    window.removeEventListener('dragover', this.onDragOver);
    window.removeEventListener('dragleave', this.onDragLeave);
    window.removeEventListener('drop', this.onDrop);
    window.removeEventListener('paste', this.onPaste);
    window.removeEventListener('scroll', this.onScroll);
    document.removeEventListener('visibilitychange', this.onVisible);
    clearInterval(this.keepAlive);
    document.removeEventListener('selectionchange', this.onSelection);
    super.disconnectedCallback();
  }
  private onScroll = () => {
    this.scrolled = window.scrollY > 0;
  };
  // Chrome unloads the on-device model when idle and reloading takes minutes.
  // Keep it loaded while this tab is visible (text-free, and only when it has
  // been idle).
  private keepAlive?: ReturnType<typeof setInterval>;
  private onVisible = () => {
    if (document.visibilityState === 'visible' && !this.scanning) {
      this.warmModel();
    }
  };
  /**
   * Load the on-device model as soon as the page opens (and wake it again after
   * a break), so a scan never starts while Chrome is still loading it. A cold
   * start can take a minute or two; the bar appears only if waking takes longer
   * than a moment, so routine keep-alives do not flash.
   */
  private warmModel() {
    if (!this.plan.usesModel) {
      if (this.modelState === 'checking') this.modelState = 'off';
      return;
    }
    if (this.warming) return;
    this.warming = (async () => {
      const status = await deviceStatus();
      if (status !== 'available') {
        this.modelState = 'off';
        return;
      }
      let tick: ReturnType<typeof setInterval> | undefined;
      const slow = setTimeout(
        () => {
          this.modelState = 'warming';
          const now = Date.now();
          this.warmNow = now;
          this.warmStart = now;
          this.warmOrder = shuffledMessages();
          this.warmReady = false;
          tick = setInterval(() => {
            this.warmNow = Date.now();
          }, 200);
        },
        this.modelState === 'checking' || deviceCold() ? 0 : 400,
      );
      try {
        await warmDevice();
        this.stopJazz();
        if (this.modelState === 'warming') {
          this.warmReady = true;
          setTimeout(() => {
            this.warmReady = false;
          }, 1400);
        }
        this.modelState = 'ready';
      } catch {
        this.stopJazz();
        this.modelState = 'off';
      } finally {
        // the scan reports a real failure
        clearTimeout(slow);
        clearInterval(tick);
      }
    })().finally(() => {
      this.warming = undefined;
    });
  }
  private get modelBlocking() {
    return (
      this.plan.usesModel &&
      (this.modelState === 'checking' || this.modelState === 'warming')
    );
  }
  private onSelection = () => {
    const sel = document.getSelection();
    const doc = this.querySelector('#doc');
    const inside =
      sel &&
      !sel.isCollapsed &&
      doc &&
      sel.anchorNode &&
      sel.focusNode &&
      doc.contains(sel.anchorNode) &&
      doc.contains(sel.focusNode);
    const picked = inside ? sel.toString().replace(/\s+/g, ' ').trim() : '';
    this.selection = picked.length >= 2 && picked.length <= 80 ? picked : '';
  };

  // ---------- document import ---------- Files are read in this tab. Dropping
  // is always intercepted so the browser never navigates to (and displays) a
  // dropped client file.
  private hasFiles = (e: DragEvent) =>
    Array.from(e.dataTransfer?.types ?? []).includes('Files');
  private onDragEnter = (e: DragEvent) => {
    if (!this.hasFiles(e)) return;
    e.preventDefault();
    this.dragDepth++;
    this.dragging = this.view === 'compose';
  };
  private onDragOver = (e: DragEvent) => {
    if (!this.hasFiles(e)) return;
    e.preventDefault();
    if (e.dataTransfer) {
      e.dataTransfer.dropEffect = this.view === 'compose' ? 'copy' : 'none';
    }
  };
  private onDragLeave = (e: DragEvent) => {
    if (!this.hasFiles(e)) return;
    this.dragDepth = Math.max(0, this.dragDepth - 1);
    if (this.dragDepth === 0) this.dragging = false;
  };
  private onDrop = (e: DragEvent) => {
    if (!this.hasFiles(e)) return;
    e.preventDefault();
    this.dragDepth = 0;
    this.dragging = false;
    if (this.view === 'compose') {
      void this.addFiles(Array.from(e.dataTransfer?.files ?? []));
    }
  };
  private onPaste = (e: ClipboardEvent) => {
    const files = Array.from(e.clipboardData?.files ?? []);
    if (!files.length || this.view !== 'compose') return;
    e.preventDefault();
    void this.addFiles(files);
  };
  private pickFile() {
    this.querySelector<HTMLInputElement>('#file-input')?.click();
  }
  private onPicked(e: Event) {
    const input = e.target as HTMLInputElement;
    void this.addFiles(Array.from(input.files ?? []));
    input.value = ''; // let the same file be chosen again
  }
  private async addFiles(files: File[]) {
    if (!files.length || this.importing) return;
    this.importing = true;
    this.importError = '';
    try {
      const {text, ...info} = await importFile(files[0]);
      this.text = text;
      this.imported =
        files.length > 1
          ? {
              ...info,
              notes: [
                ...info.notes,
                `Only ${files[0].name} was added. Add one document at a time.`,
              ],
            }
          : info;
    } catch (err) {
      const why =
        err instanceof ImportError
          ? err.message
          : 'This file could not be read.';
      this.importError = `${files[0].name} was not added. ${why}`;
    } finally {
      this.importing = false;
    }
  }
  private removeImported() {
    this.imported = null;
    this.text = '';
    this.importError = '';
  }

  // ---------- derived ---------- Data types are the one selection; regulations
  // are shortcuts that tick the types they require.
  private get plan() {
    return planForClasses([...this.classes]);
  }
  // buildDetections is ~350 ms on a 60-page document. Every input is replaced,
  // never mutated, so reuse the last result until one of them changes. Without
  // this, each selection change and question keystroke re-ran the full
  // detection.
  private detectionCache?: {key: readonly unknown[]; value: Detection[]};
  private get detections(): Detection[] {
    const key = [
      this.text,
      this.plan.detectorIds.join(),
      this.names,
      this.manual,
      this.disabled,
      this.topics,
    ] as const;
    const cached = this.detectionCache;
    if (cached && cached.key.every((part, i) => part === key[i])) {
      return cached.value;
    }
    const value = buildDetections(
      this.text,
      this.plan.detectorIds,
      this.names,
      this.manual,
      this.disabled,
      this.topics,
    );
    this.detectionCache = {key, value};
    return value;
  }
  private get scanning() {
    return this.scan.state === 'loading' || this.scan.state === 'running';
  }

  private saveRules() {
    try {
      localStorage.setItem(
        RULES_KEY,
        JSON.stringify({classes: [...this.classes], rules: [...this.rules]}),
      );
    } catch {
      /* ignore */
    }
  }
  private invalidateCloud() {
    this.cloudAbort?.abort();
    this.cloudCandidate = undefined;
    this.cloudResult = undefined;
    this.cloudReviewed = false;
  }
  private setClasses(ids: string[]) {
    if (this.asking) return;
    this.invalidateCloud();
    this.classes = new Set(ids);
    // A regulation stays ticked only while every data type it requires is on.
    this.rules = new Set([...this.rules].filter(id => this.covers(id)));
    for (const id of [...this.ruleAdded.keys()]) {
      if (!this.rules.has(id)) this.ruleAdded.delete(id);
    }
    this.saveRules();
    this.warmModel();
  }
  /** Every data type the regulation requires is ticked. */
  private covers(id: string) {
    return classesForRule(id).every(c => this.classes.has(c));
  }
  private toggleClass(id: string, on: boolean) {
    const next = new Set(this.classes);
    if (on) next.add(id);
    else next.delete(id);
    this.setClasses([...next]);
  }
  private ruleAdded = new Map<string, string[]>();
  /**
   * Ticking a regulation adds its data types; unticking removes the ones it
   * added that no other ticked regulation needs.
   */
  private toggleRule(id: string, on: boolean) {
    if (this.asking) return;
    const rules = new Set(this.rules);
    const next = new Set(this.classes);
    if (on) {
      rules.add(id);
      // Remember which types this tick switched on, so unticking removes only
      // those.
      this.ruleAdded.set(
        id,
        classesForRule(id).filter(c => !next.has(c)),
      );
      for (const c of classesForRule(id)) next.add(c);
    } else {
      rules.delete(id);
      const keep = new Set([...rules].flatMap(other => classesForRule(other)));
      for (const c of this.ruleAdded.get(id) ?? []) {
        if (!keep.has(c)) next.delete(c);
      }
      this.ruleAdded.delete(id);
    }
    this.rules = rules;
    this.setClasses([...next]);
  }
  /**
   * FOIA is an output style, not a list of data types: it marks every
   * withholding with its exemption.
   */
  private toggleFoia(on: boolean) {
    if (on) this.setClasses(DEFAULT_CLASSES);
    this.setOutput(on ? 'foia' : 'ai');
  }

  // ---------- actions ----------
  private async find() {
    this.invalidateCloud();
    const run = ++this.runId;
    this.names = {people: [], companies: []};
    this.topics = NO_TOPICS;
    this.manual = [];
    this.disabled = new Set();
    this.scanErrors = 0;
    this.tab = 0;
    this.view = 'review';
    this.startTypewriter();
    window.scrollTo({top: 0});

    if (!this.plan.usesModel) {
      this.scan = {state: 'skipped', reason: 'not-needed'};
      return;
    }
    const status = await deviceStatus();
    if (run !== this.runId) return;
    if (status === 'unsupported' || status === 'unavailable') {
      this.scan = {state: 'skipped', reason: status};
      return;
    }

    try {
      this.scan = {state: 'loading', fraction: status === 'available' ? 1 : 0};
      await prepareDevice(fraction => {
        if (run === this.runId) this.scan = {state: 'loading', fraction};
      });
      // A model Chrome unloaded while idle reloads here, under the loading
      // state, instead of timing out the first chunk.
      await wakeDevice();
    } catch {
      if (run === this.runId) {
        this.scan = {state: 'skipped', reason: 'unavailable'};
      }
      return;
    }
    const chunks = chunkText(this.text);
    const ids = this.plan.detectorIds;
    for (let i = 0; i < chunks.length && ids.includes('names'); i++) {
      if (run !== this.runId) return;
      this.scan = {
        state: 'running',
        stage: 'names',
        done: i,
        total: chunks.length,
      };
      try {
        const found = await detectNames(
          this.text.slice(chunks[i].start, chunks[i].end),
        );
        if (run !== this.runId) return;
        this.names = {
          people: [...new Set([...this.names.people, ...found.people])],
          companies: [
            ...new Set([...this.names.companies, ...found.companies]),
          ],
        };
      } catch {
        this.scanErrors++;
      }
    }
    // Second pass, after names are on screen: places, sensitive topics, first
    // names.
    for (
      let i = 0;
      i < chunks.length &&
      (ids.includes('sensitive_topics') || ids.includes('places'));
      i++
    ) {
      if (run !== this.runId) return;
      this.scan = {
        state: 'running',
        stage: 'topics',
        done: i,
        total: chunks.length,
      };
      try {
        const found = await detectTopics(
          this.text.slice(chunks[i].start, chunks[i].end),
        );
        if (run !== this.runId) return;
        const merge = (a: string[], b: string[]) => [...new Set([...a, ...b])];
        this.topics = {
          places: merge(this.topics.places, found.places),
          health: merge(this.topics.health, found.health),
          sensitive: merge(this.topics.sensitive, found.sensitive),
          names: merge(this.topics.names, found.names),
        };
      } catch {
        this.scanErrors++;
      }
    }
    if (run === this.runId) this.scan = {state: 'done'};
    // While the user reviews, load the session the cloud preview's local check
    // uses.
    if (run === this.runId) {
      void prepareModel(false).catch(() => {
        /* prepareCloud reports failures */
      });
    }
  }

  private toggle(ids: string[], on: boolean) {
    if (this.asking) return;
    this.invalidateCloud();
    // `disabled` holds the detections switched away from their default (most
    // default to replaced; sensitive topics default to flagged only).
    const defaults = new Map(this.detections.map(d => [d.id, d.defaultOn]));
    const next = new Set(this.disabled);
    for (const id of ids) {
      if (on === (defaults.get(id) ?? true)) next.delete(id);
      else next.add(id);
    }
    this.disabled = next;
  }
  private addManual(text: string, kind: string) {
    if (this.asking) return;
    this.invalidateCloud();
    if (!this.manual.some(m => m.text === text)) {
      this.manual = [...this.manual, {text, kind}];
    }
    document.getSelection()?.removeAllRanges();
    this.selection = '';
  }

  private async copy(cleaned: string) {
    try {
      await navigator.clipboard.writeText(cleaned);
      this.copied = true;
      setTimeout(() => {
        this.copied = false;
      }, 4000);
    } catch {
      this.answerError =
        'Copying was blocked by the browser. Select the text and copy it yourself.';
    }
  }

  private cloudSource() {
    return `DOCUMENT:\n${this.text}\n\nQUESTION:\n${this.question.trim()}`;
  }
  private async prepareCloud() {
    if (this.asking) return;
    this.cloudAbort?.abort();
    this.cloudAbort = new AbortController();
    const signal = this.cloudAbort.signal;
    const source = this.cloudSource();
    this.asking = true;
    this.answerError = '';
    this.cloudCandidate = undefined;
    this.cloudResult = undefined;
    this.cloudReviewed = false;
    try {
      this.cloudStage = 'Checking the document and question locally…';
      await prepareModel(true, label => {
        this.cloudStage = label;
      });
      const evidence = await extract(source, signal, label => {
        this.cloudStage = label;
      });
      signal.throwIfAborted();
      if (source !== this.cloudSource()) {
        throw new Error(
          'The document or question changed. Prepare the preview again.',
        );
      }
      const prefix = namespace();
      const identifying = [
        ...evidence.identifying,
        ...this.manual.map(d => ({
          text: d.text,
          reason: 'Marked for local removal.',
        })),
      ];
      // The on-device model is not deterministic. Keep every name the review
      // scan found, so a name shown as replaced there cannot appear raw in the
      // cloud preview.
      const union = (a: string[], b: string[]) => [...new Set([...a, ...b])];
      const names = {
        people: union(evidence.names.people, this.names.people),
        companies: union(evidence.names.companies, this.names.companies),
      };
      const topics = {
        ...evidence.topics,
        names: union(evidence.topics.names, this.topics.names),
      };
      const report = makeReport(
        source,
        names,
        topics,
        evidence.ambiguous,
        prefix,
        true,
        undefined,
        identifying,
      );
      // Honor sensitive details explicitly selected for local removal in the
      // app.
      const selected = this.detections.filter(d => d.enabled).map(d => d.text);
      const remove = report.findings
        .filter(
          d =>
            privacyBucket(d) === 'cloud-cleanup' && selected.includes(d.text),
        )
        .map(d => d.id);
      const preview = cleanedText(
        source,
        report.findings,
        prefix,
        report.findings
          .filter(
            d => privacyBucket(d) === 'cloud-cleanup' && !remove.includes(d.id),
          )
          .map(d => d.id),
      );
      this.cloudCandidate = {source, report, prefix, remove, preview};
    } catch (err) {
      if (!signal.aborted) {
        this.answerError =
          err instanceof Error
            ? err.message
            : 'The local identity check did not finish.';
      }
    } finally {
      this.asking = false;
      this.cloudStage = '';
    }
  }
  private async send() {
    if (this.asking) return;
    const candidate = this.cloudCandidate;
    if (!candidate || candidate.source !== this.cloudSource()) {
      this.answerError = 'Prepare a current cloud preview first.';
      return;
    }
    this.cloudAbort?.abort();
    this.cloudAbort = new AbortController();
    const signal = this.cloudAbort.signal;
    this.asking = true;
    this.answerError = '';
    this.cloudStage = 'Removing remaining sensitive details in cloud…';
    try {
      const input = prepareCloudInput(
        candidate.source,
        candidate.report,
        candidate.prefix,
        this.cloudReviewed,
        candidate.remove,
      );
      const result = await cleanupCloud(input, signal);
      signal.throwIfAborted();
      if (candidate.source !== this.cloudSource()) {
        throw new Error('The request changed. Prepare a new preview.');
      }
      this.cloudResult = result;
      this.map = applyRedactions(
        candidate.source,
        candidate.report.findings.map(d => ({
          ...d,
          base: `${d.base}_${candidate.prefix}`,
        })),
      ).map;
      for (const [placeholder, value] of result.replacements) {
        this.map.set(placeholder, value);
      }
      this.sent = {doc: result.report.cleaned, question: ''};
      if (!result.report.needsReview && this.question.trim()) {
        await this.answerCleaned(false, signal);
      }
    } catch (err) {
      if (!signal.aborted) {
        this.answerError =
          err instanceof Error ? err.message : 'Cloud cleanup did not finish.';
      }
    } finally {
      this.asking = false;
      this.cloudStage = '';
    }
  }
  private async answerCleaned(
    reviewed = true,
    signal = this.cloudAbort?.signal,
  ) {
    if (
      !this.cloudResult ||
      this.cloudCandidate?.source !== this.cloudSource()
    ) {
      return;
    }
    this.asking = true;
    this.cloudStage = 'Answering using the cleaned request…';
    try {
      this.answerRaw = await askCloud(
        approveCleanedResult(this.cloudResult, reviewed),
        signal,
      );
      signal?.throwIfAborted();
      this.answerTab = 0;
      this.view = 'answer';
      window.scrollTo({top: 0});
    } catch (error) {
      if (!signal?.aborted) {
        this.answerError =
          error instanceof Error ? error.message : 'The cloud answer failed.';
      }
    } finally {
      this.asking = false;
      this.cloudStage = '';
    }
  }

  private startOver() {
    this.finishTypewriter();
    this.cloudAbort?.abort();
    this.cloudCandidate = undefined;
    this.cloudResult = undefined;
    this.cloudReviewed = false;
    this.runId++;
    this.map = new Map();
    this.sent = {doc: '', question: ''};
    this.text = '';
    this.question = '';
    this.answerRaw = '';
    this.answerError = '';
    this.imported = null;
    this.importError = '';
    this.names = {people: [], companies: []};
    this.topics = NO_TOPICS;
    this.manual = [];
    this.disabled = new Set();
    this.scan = {state: 'idle'};
    this.view = 'compose';
  }
  private back() {
    this.cloudAbort?.abort();
    this.cloudCandidate = undefined;
    this.cloudResult = undefined;
    if (this.view === 'answer') {
      this.view = 'review';
      return;
    }
    this.runId++;
    this.scan = {state: 'idle'};
    this.view = 'compose';
  }

  // ---------- render ----------
  render() {
    const title = {
      compose: 'Redactobot',
      review: 'Review before sending',
      answer: 'Answer',
    }[this.view];
    return html`
      <a class="skip-link" href="#main">Skip to main content</a>
      <header class="app-bar ${this.scrolled ? 'scrolled' : ''}">
        ${
          this.view === 'compose'
            ? nothing
            : html`
          <md-icon-button aria-label="Back" @click=${this.back}>${icon('arrow_back')}</md-icon-button>`
        }
        <span class="logo-wrap ${this.view === 'compose' ? 'no-lead' : ''} ${this.jazzOn ? 'jazzing' : ''}">
          <img class="logo for-dark" src="/redactobot-logo.webp" alt="Redactobot" width="307" height="120">
          <img class="logo for-light" src="/redactobot-logo-light.webp" alt="Redactobot" width="307" height="120">
          ${this.jazzOn ? this.eyeNotes() : nothing}
        </span>
        <h1 class="title md-typescale-title-large ${this.view === 'compose' ? 'visually-hidden' : ''}">${title}</h1>
        <md-icon-button aria-label="Display: theme, colours and motion" title="Display settings" @click=${() => {
          this.displayOpen = true;
        }}>
          ${icon('contrast')}
        </md-icon-button>
        <md-icon-button aria-label="How this works" @click=${() => {
          this.aboutOpen = true;
        }}>
          ${icon('info')}
        </md-icon-button>
        ${this.progressBar()}
      </header>
      <main id="main" tabindex="-1">
        ${this.view === 'compose' ? this.composeView() : this.view === 'review' ? this.reviewView() : this.answerView()}
      </main>
      ${this.ruleDialogView()}
      ${this.aboutDialogView()}
      ${this.displayDialogView()}
`;
  }

  /**
   * The robot at work, at the top of the right-hand column: it slides open
   * while work runs.
   */
  private robotVideo() {
    return html`
      <div class="robot-slot ${this.busy && !this.reducedMotion ? 'on' : ''}">
        <div class="robot-inner">
          <video muted loop playsinline preload="auto" aria-hidden="true">
            <source src="/redactobot-working.webm" type="video/webm"><source src="/redactobot-working.mp4" type="video/mp4">
          </video>
          <md-icon-button class="robot-pause" aria-label=${this.robotPaused ? 'Play the animation' : 'Pause the animation'}
            @click=${() => {
              this.robotPaused = !this.robotPaused;
            }}>${icon(this.robotPaused ? 'play_arrow' : 'pause')}</md-icon-button>
        </div>
      </div>`;
  }

  /**
   * Something is being worked on: reading a file, finding details, revealing
   * them, or the cloud step.
   */
  private get busy() {
    return this.importing || this.scanning || this.asking || !!this.anim;
  }
  /** Reduced motion: the user's choice here, or the computer's setting. */
  private get reducedMotion() {
    return (
      this.display.motion === 'reduced' ||
      (typeof matchMedia === 'function' &&
        matchMedia('(prefers-reduced-motion: reduce)').matches)
    );
  }
  /**
   * The looping robot video plays only while work is running; otherwise it is
   * hidden and paused.
   */
  private syncRobotVideo() {
    const video = this.querySelector<HTMLVideoElement>('.robot-slot video');
    if (!video) return;
    const wide =
      typeof matchMedia !== 'function' ||
      matchMedia('(min-width: 840px)').matches;
    if (this.busy && wide && !this.reducedMotion && !this.robotPaused) {
      if (video.paused) {
        void Promise.resolve(video.play()).catch(() => {
          /* autoplay blocked: stays still */
        });
      }
    } else if (!video.paused) {
      video.pause();
    }
  }

  private progressBar() {
    if (
      this.modelState === 'warming' &&
      this.plan.usesModel &&
      this.view === 'compose'
    ) {
      return html`<md-linear-progress indeterminate aria-label="Starting the on-device AI model"></md-linear-progress>`;
    }
    if (this.asking) {
      return html`<md-linear-progress indeterminate aria-label="Waiting for the cloud AI"></md-linear-progress>`;
    }
    if (this.importing) {
      return html`<md-linear-progress indeterminate aria-label="Reading the document"></md-linear-progress>`;
    }
    if (this.scan.state === 'loading') {
      return this.scan.fraction > 0 && this.scan.fraction < 1
        ? html`<md-linear-progress .value=${this.scan.fraction} aria-label="Downloading the on-device model"></md-linear-progress>`
        : html`<md-linear-progress indeterminate aria-label="Loading the on-device model"></md-linear-progress>`;
    }
    if (this.scan.state === 'running') {
      return this.scan.total > 1
        ? html`<md-linear-progress .value=${this.scan.done / this.scan.total} aria-label="Checking for names"></md-linear-progress>`
        : html`<md-linear-progress indeterminate aria-label="Checking for names"></md-linear-progress>`;
    }
    return nothing;
  }

  // Each click loads the next sample, starting from a random one.
  private sampleIndex = Math.floor(Math.random() * SAMPLES.length);
  private useSample = () => {
    this.text = SAMPLES[this.sampleIndex % SAMPLES.length].text;
    this.sampleIndex++;
    this.imported = null;
    this.importError = '';
  };

  // ----- compose -----
  private composeView() {
    const words = (this.text.trim().match(/\S+/g) || []).length;
    return html`
      <div class="panes">
        <div class="stack">
          ${(this.modelState === 'warming' || this.warmReady) && this.plan.usesModel ? this.warmCard() : nothing}
          <p class="md-typescale-body-large muted">
            Add a document or paste text to remove sensitive information like names, birthdays, addresses and
            financial details. This is a technology demonstration and not a validated compliance tool. Use at
            your own risk. <a href="/privacy.html">Privacy and terms</a>
            · <a href="https://github.com/BFParsons/redactobot/releases/latest" target="_blank" rel="noopener noreferrer">Get the Chrome extension</a>
          </p>
          ${this.dropZone()}
          <md-outlined-text-field type="textarea" rows="12" label=${this.imported ? 'Text from the document' : 'Paste here'}
            supporting-text=${words ? `${words.toLocaleString('en-US')} words. Nothing has left this device.` : 'You can also type or paste here. Nothing leaves this device at this step.'}
            .value=${live(this.text)}
            @input=${(e: Event) => {
              this.text = (e.target as HTMLInputElement).value;
            }}>
          </md-outlined-text-field>
          <div class="actions">
            <md-text-button @click=${this.useSample}>Use a sample document</md-text-button>
            <md-filled-button ?disabled=${!this.text.trim() || this.plan.detectorIds.length === 0 || this.modelBlocking} @click=${this.find}>
              ${icon('search', 'icon')}${this.modelBlocking ? 'Starting on-device AI…' : 'Find private details'}
            </md-filled-button>
          </div>
        </div>
        <aside class="supporting">${this.robotVideo()}${this.rulesCard()}</aside>
      </div>`;
  }

  private toggleJazz = () => {
    if (this.jazzOn) this.stopJazz();
    else this.jazzOn = this.jazz.start();
  };
  private stopJazz() {
    this.jazz.stop();
    this.jazzOn = false;
  }
  /**
   * Notes in the robot's eyes, and fainter ones drifting up from them, while
   * the music plays. Decorative only.
   */
  private eyeNotes() {
    const drifting = ['♪', '♫', '♩', '♪', '♬', '♫'];
    return html`<span class="eye-notes" aria-hidden="true">
      <span class="eye-note left">♪</span>
      <span class="eye-note right">♫</span>
      ${drifting.map(
        (glyph, i) =>
          html`<span class="float-note ${i % 2 ? 'right' : 'left'}" style=${styleMap({'--i': String(i)})}>${glyph}</span>`,
      )}
    </span>`;
  }

  /** The cold-start card: an estimated, animated bar plus elapsed time. */
  private warmCard() {
    const ms = Math.max(0, this.warmNow - this.warmStart);
    const pct = warmPercent(ms, this.warmReady);
    const line = this.warmReady
      ? 'On-device AI is ready.'
      : loadingMessage(this.warmOrder, ms, 'Starting the on-device AI model…');
    const secs = Math.floor(ms / 1000);
    const clock = `${Math.floor(secs / 60)}:${String(secs % 60).padStart(2, '0')}`;
    return html`
      <div class="notice warm-card ${this.warmReady ? 'done' : ''}">
        ${icon(this.warmReady ? 'check_circle' : 'downloading')}
        <div class="md-typescale-body-medium">
          <strong aria-hidden="true">${line}</strong>
          <span class="visually-hidden" role="status">${this.warmReady ? 'On-device AI is ready.' : 'Starting the on-device AI model. This can take a minute or two.'}</span>
          <div class="warm-bar" role="progressbar" aria-label="Starting the on-device AI model" aria-valuemin="0" aria-valuemax="100"
            aria-valuenow=${pct} aria-valuetext=${this.warmReady ? 'Ready' : `About ${pct}%, ${secs} seconds so far`}>
            <div class="warm-fill" style=${styleMap({width: `${pct}%`})}></div>
          </div>
          <div class="warm-meta md-typescale-body-small"><span>${this.warmReady ? 'Ready' : `About ${pct}%`}</span><span>${clock}</span></div>
          ${
            this.warmReady
              ? nothing
              : html`<div>Your local AI is getting set up. It will take a moment. In the meantime, why not listen to
            smooth jazz?</div>
          <md-outlined-button class="jazz-button" aria-pressed=${this.jazzOn ? 'true' : 'false'} @click=${this.toggleJazz}>
            ${icon(this.jazzOn ? 'pause' : 'play_arrow', 'icon')}${this.jazzOn ? 'Pause the jazz' : 'Play smooth jazz'}
          </md-outlined-button>`
          }
        </div>
      </div>`;
  }

  private dropZone() {
    const f = this.imported;
    return html`
      <div class="dropzone ${this.dragging ? 'over' : ''}">
        <input id="file-input" type="file" accept=${ACCEPT} hidden @change=${this.onPicked}>
        ${
          f
            ? html`
          ${icon('description')}
          <div class="dropzone-text">
            <md-chip-set aria-label="Added document" style="padding:0">
              <md-input-chip label=${f.name} remove-only @remove=${this.removeImported}></md-input-chip>
            </md-chip-set>
            <p class="md-typescale-body-medium muted">${f.kind} · ${f.detail}. Read on this device; the file was not uploaded.</p>
          </div>
          <md-text-button @click=${this.pickFile}>Replace</md-text-button>`
            : html`
          ${icon('upload_file')}
          <div class="dropzone-text">
            <p class="md-typescale-title-medium">${this.dragging ? 'Drop the document to add it' : 'Drag a document here'}</p>
            <p class="md-typescale-body-medium muted">${ACCEPT_LABEL}. Up to 25 MB.
              The file is read on this device and is not uploaded.</p>
          </div>
          <md-outlined-button ?disabled=${this.importing} @click=${this.pickFile}>Choose a file</md-outlined-button>`
        }
      </div>
      ${
        this.importError
          ? html`
        <div class="notice warn" role="alert">${icon('error')}
          <div class="md-typescale-body-medium">${this.importError}</div></div>`
          : nothing
      }
      ${
        f?.notes.map(
          note => html`
        <div class="notice plain" role="status">${icon('info')}
          <div class="md-typescale-body-medium">${note}</div></div>`,
        ) ?? nothing
      }`;
  }

  private rulesCard() {
    const p = this.plan;
    const nothingChosen = this.classes.size === 0;
    const rulesOn = this.rules.size + (this.output === 'foia' ? 1 : 0);
    const toggle = (key: 'types' | 'rules') => (e: Event) => {
      this.openSection = {
        ...this.openSection,
        [key]: (e.target as HTMLDetailsElement).open,
      };
    };
    return html`
      <md-outlined-card class="picker">
        <div class="card-head">
          <h2 class="md-typescale-title-medium">What to replace</h2>
          <p class="md-typescale-body-medium muted">Select which information you want scanned and redacted</p>
        </div>
        <details class="pick-section" ?open=${this.openSection.types} @toggle=${toggle('types')}>
          <summary>
            <span class="md-typescale-title-small">Data type</span>
            <span class="md-typescale-body-small muted">${this.classes.size} of ${DATA_CLASSES.length} on</span>
            ${icon('chevron_right')}
          </summary>
          ${this.classPicker()}
        </details>
        <md-divider></md-divider>
        <details class="pick-section" ?open=${this.openSection.rules} @toggle=${toggle('rules')}>
          <summary>
            <span class="md-typescale-title-small">Regulatory</span>
            <span class="md-typescale-body-small muted">${rulesOn === 0 ? 'None selected' : `${rulesOn} selected`}</span>
            ${icon('chevron_right')}
          </summary>
          ${this.rulePicker()}
        </details>
        <md-divider></md-divider>
        <div class="card-body">
          <p class="md-typescale-body-medium muted" role="status">
            ${
              nothingChosen
                ? 'Choose at least one type of data.'
                : html`
              ${p.detectorIds.length - (p.usesModel ? 1 : 0)} instant checks.
              ${p.usesModel ? 'Names are found by an AI model that runs on this device.' : 'No names to find, so the on-device AI model is not used.'}`
            }
          </p>
        </div>
      </md-outlined-card>`;
  }

  /**
   * Choose by type of data, grouped by how often each type was fully replaced
   * in testing.
   */
  private classPicker() {
    const replaced = DATA_CLASSES.filter(c => c.action === 'replace');
    const flagged = DATA_CLASSES.filter(c => c.action === 'flag');
    const upTo = (tiers: string[]) =>
      [...replaced.filter(c => tiers.includes(c.tier)), ...flagged].map(
        c => c.id,
      );
    const quick = [
      {label: 'Highly accurate only', ids: upTo(['high'])},
      {label: 'Highly accurate and accurate', ids: upTo(['high', 'medium'])},
      {label: 'Everything', ids: DEFAULT_CLASSES},
    ];
    const sameSet = (ids: string[]) =>
      ids.length === this.classes.size && ids.every(id => this.classes.has(id));
    const row = (c: DataClass, trailing: string) => html`
      <label class="pick-row" title="For example: ${c.example}">
        <md-checkbox touch-target="wrapper" aria-label=${c.label}
          .checked=${live(this.classes.has(c.id))}
          @change=${(e: Event) => this.toggleClass(c.id, (e.target as HTMLInputElement).checked)}></md-checkbox>
        <span class="md-typescale-body-medium">${c.label}</span>
        <span class="rate md-typescale-body-small muted" title="${c.caught} of ${c.of} test values">${trailing}</span>
      </label>`;
    return html`
      <md-chip-set aria-label="Quick pick" class="pick-chips">
        ${quick.map(
          q => html`
          <md-filter-chip label=${q.label} .selected=${live(sameSet(q.ids))}
            @click=${(e: Event) => {
              e.preventDefault();
              this.setClasses(q.ids);
            }}></md-filter-chip>`,
        )}
      </md-chip-set>
      ${ACCURACY_TIERS.map(t => {
        const items = replaced.filter(c => c.tier === t.id);
        return items.length === 0
          ? nothing
          : html`
          <div class="tier-head" title=${t.note}>
            <h3 class="md-typescale-label-large">${t.label}</h3>
            <span class="md-typescale-body-small muted">${t.note}</span>
          </div>
          <div class="pick-list" role="group" aria-label=${t.label}>${items.map(c => row(c, shownRate(c)))}</div>`;
      })}
      ${
        flagged.length === 0
          ? nothing
          : html`
        <div class="tier-head">
          <h3 class="md-typescale-label-large">Flagged, not replaced</h3>
          <span class="md-typescale-body-small muted">Underlined for you to decide.</span>
        </div>
        <div class="pick-list" role="group" aria-label="Flagged, not replaced">${flagged.map(c => row(c, `${shownRate(c)} flagged`))}</div>`
      }
      <p class="md-typescale-body-small muted pick-note">
        Rates: share of test values fully replaced on 60 documents the app had not seen. No type is caught every time.
      </p>`;
  }

  /**
   * Regulations as shortcuts: each one ticks the data types it requires. A box
   * is ticked or blank.
   */
  private rulePicker() {
    return html`
      <div class="pick-list" role="group" aria-label="Regulations">
        ${FRAMEWORKS.map(
          f => html`
          <div class="pick-row">
            <md-checkbox touch-target="wrapper" aria-label=${f.short}
              .checked=${live(this.rules.has(f.id))}
              @change=${(e: Event) => this.toggleRule(f.id, (e.target as HTMLInputElement).checked)}></md-checkbox>
            <span class="md-typescale-body-medium" title=${f.cite}>${f.short}</span>
            <md-icon-button aria-label="What ${f.short} covers" @click=${() => {
              this.ruleDialog = f.id;
            }}>
              ${icon('list_alt')}
            </md-icon-button>
          </div>`,
        )}
        <div class="pick-row">
          <md-checkbox touch-target="wrapper" aria-label="FOIA release (US)"
            .checked=${live(this.output === 'foia')}
            @change=${(e: Event) => this.toggleFoia((e.target as HTMLInputElement).checked)}></md-checkbox>
          <span class="md-typescale-body-medium" title="5 U.S.C. § 552(b)">FOIA release (US)</span>
          <md-icon-button aria-label="What FOIA release does" @click=${() => {
            this.ruleDialog = 'foia';
          }}>
            ${icon('list_alt')}
          </md-icon-button>
        </div>
      </div>
      <p class="md-typescale-body-small muted pick-note">Ticking a regulation ticks the data types it requires. FOIA release checks every
        data type and marks each withholding with its exemption, such as (b)(6).</p>`;
  }

  // ----- review -----
  private reviewView() {
    const dets = this.detections;
    const red = applyRedactions(this.text, dets);
    const active = dets.filter(d => d.enabled).length;
    const candidate = this.cloudCandidate;
    const setupProblem = cloudSetupProblem();
    const canSend =
      !setupProblem &&
      !this.scanning &&
      !this.asking &&
      candidate?.source === this.cloudSource() &&
      candidate.report.complete &&
      candidate.report.reasons.length === 0 &&
      (!candidate.report.needsReview || this.cloudReviewed);
    return html`
      <div class="panes">
        <div class="stack">
          ${this.verdict(dets)}
          ${this.scanNotice()}
          ${
            dets.some(d => !d.defaultOn)
              ? html`
            <div class="notice" role="status">${icon('visibility')}
              <div class="md-typescale-body-medium"><strong>${dets.filter(d => !d.defaultOn).length} sensitive details are flagged.</strong>
                Health, religion, immigration status and similar topics are underlined. Select any you want removed locally.
                Cloud cleanup has a separate mandatory identity check and an exact preview before sending.</div></div>`
              : nothing
          }
          <div class="output-row" role="group" aria-label="Output">
            <span class="md-typescale-label-large">Output</span>
            <md-chip-set>
              <md-filter-chip label="For an AI chat" .selected=${live(this.output === 'ai')}
                @click=${(e: Event) => {
                  e.preventDefault();
                  this.setOutput('ai');
                }}></md-filter-chip>
              <md-filter-chip label="FOIA release (US)" .selected=${live(this.output === 'foia')}
                @click=${(e: Event) => {
                  e.preventDefault();
                  this.setOutput('foia');
                }}></md-filter-chip>
            </md-chip-set>
          </div>
          <md-outlined-card>
            <md-tabs aria-label="Document view" .activeTabIndex=${this.tab}
              @change=${(e: Event) => {
                this.tab = (
                  e.target as unknown as {activeTabIndex: number}
                ).activeTabIndex;
              }}>
              <md-primary-tab>${this.output === 'foia' ? 'Release' : 'Cleaned text'}</md-primary-tab>
              <md-primary-tab>What was found</md-primary-tab>
            </md-tabs>
            ${
              this.tab === 1
                ? html`
              <div id="doc" class="doc md-typescale-body-large">${this.highlighted(dets, red.placeholders)}</div>
              <div class="legend md-typescale-label-medium muted" aria-hidden="true">
                <span><i style="background:var(--md-sys-color-tertiary-container)"></i>Person</span>
                <span><i style="background:var(--md-sys-color-secondary-container)"></i>Organization</span>
                <span><i style="background:var(--md-sys-color-primary-container)"></i>Number or contact detail</span>
                <span><i style="outline:1px dashed var(--md-sys-color-outline);outline-offset:-1px"></i>Kept as written</span>
                <span><i class="flag-swatch"></i>Sensitive topic, flagged only</span>
              </div>`
                : html`
              <div class="doc md-typescale-body-large ${this.anim ? 'typing' : ''} ${this.output === 'foia' ? 'foia-paper' : ''}" aria-busy=${this.anim ? 'true' : 'false'} title=${this.anim ? 'Click to show everything now' : ''}
                @click=${this.finishTypewriter} @wheel=${this.stopFollowing} @touchstart=${this.stopFollowing}
                >${this.output === 'foia' ? this.foiaStamp(dets) : nothing}${this.cleanedView(dets, red.placeholders)}${
                  this.output === 'foia' && !this.anim
                    ? this.foiaLegend(dets)
                    : nothing
                }</div>
              ${
                this.output === 'foia'
                  ? html`
              <div class="actions card-actions">
                <span class="md-typescale-body-medium muted" role="status">
                  ${this.copied ? 'Copied with the markings as text.' : 'Each withholding is boxed and marked with its exemption.'}
                </span>
                <md-text-button @click=${() => this.copy(foiaText(this.text, dets, this.foia))}>
                  ${icon(this.copied ? 'check_circle' : 'content_copy', 'icon')}${this.copied ? 'Copied' : 'Copy as text'}
                </md-text-button>
                <md-filled-tonal-button @click=${this.printRelease}>${icon('description', 'icon')}Print or save as PDF</md-filled-tonal-button>
              </div>`
                  : html`
              <div class="actions card-actions">
                <span class="md-typescale-body-medium muted" role="status">
                  ${this.copied ? 'Copied. Paste it into your AI chat.' : 'Use this text in any AI chat.'}
                </span>
                <md-text-button @click=${() => this.copy(red.cleaned)}>
                  ${icon(this.copied ? 'check_circle' : 'content_copy', 'icon')}${this.copied ? 'Copied' : 'Copy replaced text'}
                </md-text-button>
              </div>`
              }`
            }
          </md-outlined-card>
          ${
            this.selection && this.tab === 1
              ? html`
            <div class="selection-bar" role="group" aria-label="Replace the selected text">
              <span class="md-typescale-body-medium">Replace “${this.selection}” everywhere as</span>
              <md-assist-chip label="Person" @click=${() => this.addManual(this.selection, 'person')}></md-assist-chip>
              <md-assist-chip label="Organization" @click=${() => this.addManual(this.selection, 'company')}></md-assist-chip>
              <md-assist-chip label="Other detail" @click=${() => this.addManual(this.selection, 'other')}></md-assist-chip>
            </div>`
              : html`
            <p class="md-typescale-body-medium muted">
              ${
                this.tab === 1
                  ? 'Select a highlight to keep it as written. Select any other text to replace it too.'
                  : 'To change what is replaced, open What was found.'
              }
            </p>`
          }
          ${
            this.output === 'foia'
              ? html`
          <div class="notice plain" role="note">${icon('devices')}
            <div class="md-typescale-body-medium"><strong>A FOIA release stays on this device.</strong>
              Cloud cleanup is off in this mode. Check every withholding and its exemption before release;
              the defaults are a starting point, not a legal determination.</div></div>`
              : html`
          <md-outlined-card>
            <div class="card-body">
              <h2 class="md-typescale-title-medium">Cloud cleanup and optional question</h2>
              <md-outlined-text-field type="textarea" rows="3" label="Your question"
                supporting-text="The document and question both pass the local identity check. Leave blank for cleanup only."
                .value=${live(this.question)}
                ?disabled=${this.asking}
                @input=${(e: Event) => {
                  this.question = (e.target as HTMLInputElement).value;
                  this.cloudCandidate = undefined;
                  this.cloudResult = undefined;
                  this.cloudReviewed = false;
                }}>
              </md-outlined-text-field>
              ${
                setupProblem
                  ? html`
                <div class="notice plain" role="status">
                  ${icon('cloud_off')}
                  <div class="md-typescale-body-medium">${setupProblem} You can still prepare the preview locally.</div>
                </div>`
                  : nothing
              }
              ${
                candidate
                  ? html`
                <h3 class="md-typescale-title-small">Exact text the cloud will receive</h3>
                <p class="md-typescale-body-medium">Identifiers are removed locally. Remaining medical and sensitive details may be sent to Gemini through Firebase for removal. Files, filenames, chat history and identity mappings are excluded. This does not guarantee anonymity.</p>
                <pre class="doc md-typescale-body-medium">${candidate.preview}</pre>
                ${candidate.report.reasons.length ? html`<p role="alert">${candidate.report.reasons.join(' ')}</p>` : nothing}
                ${
                  candidate.report.needsReview
                    ? html`<label class="md-typescale-body-medium"><input type="checkbox" .checked=${this.cloudReviewed}
                  @change=${(event: Event) => {
                    this.cloudReviewed = (
                      event.target as HTMLInputElement
                    ).checked;
                  }}>
                  I reviewed this preview for identifying context. Any further identifying details must be marked for local removal.</label>`
                    : nothing
                }
              `
                  : nothing
              }
              ${
                this.cloudResult
                  ? html`
                <h3 class="md-typescale-title-small">After cloud cleanup</h3><pre class="doc md-typescale-body-medium">${this.cloudResult.report.cleaned}</pre>
                ${this.cloudResult.report.needsReview ? html`<p role="alert">The cloud found a possible identifying or ambiguous detail. It has been removed; review this result before continuing.</p>` : nothing}
                <md-text-button @click=${() => this.copy(this.cloudResult!.report.cleaned)}>Copy scrubbed result</md-text-button>
                ${this.question.trim() && this.cloudResult.report.needsReview ? html`<md-filled-button ?disabled=${this.asking} @click=${() => this.answerCleaned(true)}>Use reviewed result to answer</md-filled-button>` : nothing}
              `
                  : nothing
              }
              ${
                this.answerError
                  ? html`
                <div class="notice warn" role="alert">
                  ${icon('error')}
                  <div class="md-typescale-body-medium">${this.answerError}</div>
                </div>`
                  : nothing
              }
              <div class="actions">
                <span class="md-typescale-body-medium muted" role="status">
                  ${this.cloudStage || (this.scanning ? 'Still checking for names.' : `${active} details selected for local removal.`)}
                </span>
                <md-outlined-button ?disabled=${this.scanning || this.asking} @click=${this.prepareCloud}>Prepare cloud preview locally</md-outlined-button>
                <md-filled-button ?disabled=${!canSend} @click=${this.send}>
                  ${icon('send', 'icon')}${this.question.trim() ? 'Clean up, then answer' : 'Run cloud cleanup'}
                </md-filled-button>
              </div>
            </div>
          </md-outlined-card>`
          }
        </div>
        <aside class="supporting stack">
          ${this.robotVideo()}
          ${this.output === 'foia' ? this.exemptionsCard(dets) : nothing}
          ${this.detectionsCard(dets, red.placeholders)}
          ${this.worthALookCard(dets)}
        </aside>
      </div>`;
  }

  private scanNotice() {
    const s = this.scan;
    const notice = (
      cls: string,
      name: IconName,
      body: TemplateResult | string,
      role = 'status',
    ) => html`
      <div class="notice ${cls}" role=${role}>${icon(name)}
        <div class="md-typescale-body-medium">${body}</div></div>`;
    if (s.state === 'loading') {
      return notice(
        '',
        'downloading',
        s.fraction > 0 && s.fraction < 1
          ? `Downloading the on-device AI model: ${Math.round(s.fraction * 100)}%. This happens once.`
          : 'Loading the on-device AI model. Numbers and contact details are already marked below.',
      );
    }
    if (s.state === 'running') {
      const what =
        s.stage === 'names' ? 'names' : 'places and sensitive topics';
      return notice(
        '',
        'manage_search',
        s.total > 1
          ? `Checking for ${what} on this device: part ${s.done + 1} of ${s.total}. You can start reviewing.`
          : `Checking for ${what} on this device. This can take a little while. You can start reviewing.`,
      );
    }
    if (s.state === 'skipped' && s.reason !== 'not-needed') {
      return notice(
        'warn',
        'warning',
        html`<strong>Names were not checked.</strong>
        ${
          s.reason === 'unsupported'
            ? 'This browser has no on-device AI model. Use Chrome on a desktop computer.'
            : 'This computer cannot run the on-device AI model.'
        }
        Numbers and contact details are marked. Select each name yourself before sending.`,
        'alert',
      );
    }
    if (this.scanErrors > 0 && s.state === 'done') {
      return notice(
        'warn',
        'warning',
        html`<strong>Part of the document was not checked for names.</strong>
        The on-device AI model failed on ${this.scanErrors} part${this.scanErrors > 1 ? 's' : ''}. Read through and select any names that are not marked.`,
        'alert',
      );
    }
    return nothing;
  }

  /**
   * The headline after a scan. Green only when nothing is left in doubt: the
   * on-device check finished (or was not needed), no sensitive topic is flagged
   * and no possible name is left unmarked. Otherwise orange, with the reason.
   * Never a claim of perfect redaction.
   */
  private verdict(dets: Detection[]) {
    const s = this.scan;
    if (s.state === 'loading' || s.state === 'running') return nothing;
    const modelOk =
      (s.state === 'done' && this.scanErrors === 0) ||
      (s.state === 'skipped' && s.reason === 'not-needed');
    const flagged = dets.filter(d => !d.defaultOn && !d.enabled).length;
    const unmarked = unexplainedCapitals(this.text, dets).length;
    const clean = modelOk && flagged === 0 && unmarked === 0;
    const reasons = [
      !modelOk ? 'names were not fully checked on this device' : '',
      flagged
        ? `${flagged} sensitive detail${flagged > 1 ? 's are' : ' is'} flagged but not removed`
        : '',
      unmarked
        ? `${unmarked} word${unmarked > 1 ? 's' : ''} under Worth a look may be names`
        : '',
    ].filter(Boolean);
    return clean
      ? html`
      <div class="verdict clean" role="status">
        ${icon('check_circle')}
        <div><p class="md-typescale-title-large">Your text looks clean</p>
          <p class="md-typescale-body-large">${this.output === 'foia' ? 'Read it once more and confirm each exemption before release.' : 'Read it once more before you paste it into an AI chat.'}</p></div>
      </div>`
      : html`
      <div class="verdict review" role="status">
        ${icon('warning')}
        <div><p class="md-typescale-title-large">Review before you share</p>
          <p class="md-typescale-body-large">We removed what we found, but ${reasons.join('; ')}.
            ${
              this.output === 'foia'
                ? 'Box every detail that must be withheld and confirm its exemption before release.'
                : 'Once every identifying detail is gone, use cloud cleanup below to remove secondary details such as medical conditions.'
            }</p></div>
      </div>`;
  }

  private highlighted(dets: Detection[], placeholders: Map<string, string>) {
    const parts: Array<string | TemplateResult> = [];
    let at = 0;
    for (const d of dets) {
      if (d.start < at) continue;
      parts.push(this.text.slice(at, d.start));
      const ph = placeholders.get(d.id);
      const tip = d.enabled
        ? `${d.label}. Will be sent as [${ph}]. Select to keep as written.`
        : d.defaultOn
          ? `${d.label}. Kept as written. Select to replace.`
          : `${d.label}. Flagged for you to check; sent as written unless you select it.`;
      // A span, not a <button>: buttons cannot wrap across lines, and names
      // often do.
      const flip = () => this.toggle([d.id], !d.enabled);
      parts.push(html`<span class="hl ${d.kind} ${d.defaultOn ? '' : 'flag'}" role="button" tabindex="0" aria-pressed=${d.enabled ? 'true' : 'false'}
        title=${tip} aria-label="${d.text.replace(/\s+/g, ' ')}. ${tip}" @click=${flip}
        @keydown=${(e: KeyboardEvent) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            flip();
          }
        }}>${d.text}</span>`);
      at = d.end;
    }
    parts.push(this.text.slice(at));
    return parts;
  }

  private withPlaceholders(cleaned: string) {
    return cleaned
      .split(/(\[[A-Z][A-Z_]*_\d+\])/g)
      .map((part, i) => (i % 2 ? html`<span class="ph">${part}</span>` : part));
  }

  /**
   * The cleaned text, built from the original and the detections: replaced
   * details show as highlighted placeholders, and sensitive details that are
   * flagged but not removed stay in red so they are seen at once (click one to
   * remove it). While the typewriter runs, only the revealed part shows, found
   * details flash red, then type out their placeholder.
   */
  private cleanedView(dets: Detection[], placeholders: Map<string, string>) {
    const a = this.anim;
    const now = performance.now();
    const end = a ? a.pos : this.text.length;
    const spans = dets
      .filter(d => d.enabled || !d.defaultOn)
      .sort((x, y) => x.start - y.start);
    const out: unknown[] = [];
    let at = 0;
    for (const d of spans) {
      if (d.start >= end) break;
      if (d.start < at) continue;
      out.push(this.text.slice(at, d.start));
      if (!d.enabled) {
        const remove = (e: Event) => {
          e.stopPropagation();
          e.preventDefault();
          this.toggle([d.id], true);
        };
        out.push(html`<span class="flagged-detail" role="button" tabindex="0"
          title="Sensitive detail, not removed. Click to remove it." aria-label="Sensitive detail, not removed: ${this.text.slice(d.start, d.end)}. Press to remove it."
          @click=${remove} @keydown=${(e: KeyboardEvent) => {
            if (e.key === 'Enter' || e.key === ' ') remove(e);
          }}>${this.text.slice(d.start, Math.min(d.end, end))}</span>`);
      } else {
        const ph = `[${placeholders.get(d.id) ?? ''}]`;
        const t0 = a?.found.get(d.start);
        const age = t0 === undefined ? Infinity : now - t0;
        if (this.output === 'foia') {
          const code = exemptionFor(d.kind, this.foia);
          const withheld = this.text.slice(d.start, d.end);
          out.push(
            age < TYPE_FLASH_MS
              ? html`<span class="ph-found">${withheld}</span>`
              : html`<span class="foia-box" role="img"
            aria-label="Withheld under ${code}"><span class="foia-code" aria-hidden="true">${code}</span><span aria-hidden="true">${boxFill(withheld, code)}</span></span>`,
          );
          at = d.end;
          continue;
        }
        out.push(
          age < TYPE_FLASH_MS
            ? html`<span class="ph-found">${this.text.slice(d.start, d.end)}</span>`
            : html`<span class="ph">${ph.slice(0, Math.max(1, Math.ceil((ph.length * (age - TYPE_FLASH_MS)) / TYPE_SWAP_MS)))}</span>`,
        );
      }
      at = d.end;
    }
    if (at < end) out.push(this.text.slice(at, end));
    if (a) out.push(html`<span class="type-cursor" aria-hidden="true"></span>`);
    return out;
  }

  /**
   * Reveal the document a couple of words per frame, like model output on a
   * terminal. Each detail that will be replaced flashes red, then its
   * placeholder types out and stays highlighted; these effects run alongside
   * the reveal, so the cursor never waits. Click the text to skip. Display
   * only: the cleaned text is complete and copyable throughout. Off when the
   * user prefers reduced motion.
   */
  private startTypewriter() {
    cancelAnimationFrame(this.typer);
    this.anim = null;
    if (this.reducedMotion) return;
    this.anim = {pos: 0, found: new Map()};
    this.userScrolled = false;
    this.typer = requestAnimationFrame(this.typeStep);
  }
  private finishTypewriter = () => {
    cancelAnimationFrame(this.typer);
    this.anim = null;
  };
  private stopFollowing = () => {
    this.userScrolled = true;
  };
  private typeStep = (now: number) => {
    const a = this.anim;
    if (!a || this.view !== 'review') return;
    const text = this.text;
    const spans = this.detections
      .filter(d => d.enabled)
      .sort((x, y) => x.start - y.start);
    let pos = a.pos;
    const found = new Map(a.found);
    for (let words = 0; words < TYPE_WORDS_PER_FRAME && pos < text.length;) {
      const upcoming = spans.find(s => s.start >= pos);
      if (upcoming && upcoming.start === pos) {
        found.set(pos, now);
        pos = upcoming.end;
        words++;
        continue;
      }
      const word = /\s*\S+\s*/y;
      word.lastIndex = pos;
      const m = word.exec(text);
      let to = m ? pos + m[0].length : text.length;
      if (upcoming && upcoming.start < to) to = upcoming.start;
      pos = to;
      words++;
    }
    const settling = [...found.values()].some(
      t0 => now - t0 < TYPE_FLASH_MS + TYPE_SWAP_MS,
    );
    if (pos >= text.length && !settling) {
      this.anim = null;
      return;
    }
    this.anim = {pos, found};
    this.typer = requestAnimationFrame(this.typeStep);
  };
  protected updated() {
    this.syncRobotVideo();
    if (this.anim && !this.userScrolled) {
      this.querySelector('.type-cursor')?.scrollIntoView({block: 'nearest'});
    }
  }

  private detectionsCard(dets: Detection[], placeholders: Map<string, string>) {
    const groups = new Map<string, Map<string, Detection[]>>();
    for (const d of dets) {
      const g =
        groups.get(d.label) ?? groups.set(d.label, new Map()).get(d.label)!;
      (g.get(d.entity) ?? g.set(d.entity, []).get(d.entity)!).push(d);
    }
    return html`
      <md-outlined-card>
        <div class="card-head">
          <h2 class="md-typescale-title-medium">Found in this document</h2>
          <p class="md-typescale-body-medium muted">
            ${dets.length ? 'Clear a box to keep that detail as written.' : this.scanning ? 'Nothing yet.' : 'Nothing was found.'}
          </p>
        </div>
        ${[...groups].map(
          ([label, entities]) => html`
          <div class="section-label md-typescale-label-large">${label}</div>
          <md-list aria-label=${label}>
            ${[...entities.values()].map(list => {
              const on = list.filter(d => d.enabled).length;
              const ph = list.map(d => placeholders.get(d.id)).find(Boolean);
              const shortForms = new Set(
                list
                  .filter(d => d.text.replace(/\s+/g, ' ') !== d.canonical)
                  .map(d => d.text),
              ).size;
              const detail = [
                `${list.length} place${list.length > 1 ? 's' : ''}`,
                ph ? `sent as [${ph}]` : 'kept as written',
                shortForms ? 'includes short forms' : '',
                list[0].source === 'manual' ? 'added by you' : '',
              ]
                .filter(Boolean)
                .join(' · ');
              return html`
                <md-list-item>
                  <md-checkbox slot="start" touch-target="wrapper" aria-label="Replace ${list[0].canonical}"
                    .checked=${live(on === list.length)} .indeterminate=${live(on > 0 && on < list.length)}
                    @change=${(e: Event) =>
                      this.toggle(
                        list.map(d => d.id),
                        (e.target as HTMLInputElement).checked,
                      )}></md-checkbox>
                  <div slot="headline">${list[0].canonical}</div>
                  <div slot="supporting-text">${detail}</div>
                </md-list-item>`;
            })}
          </md-list>`,
        )}
        <div class="card-body"></div>
      </md-outlined-card>`;
  }

  private worthALookCard(dets: Detection[]) {
    const left = unexplainedCapitals(this.text, dets).slice(0, 24);
    if (!left.length) return nothing;
    return html`
      <md-outlined-card>
        <div class="card-head">
          <h2 class="md-typescale-title-medium">Worth a look</h2>
          <p class="md-typescale-body-medium muted">Capitalized words that were not marked. Select one to replace it.</p>
        </div>
        <div class="card-body">
          <md-chip-set aria-label="Words that were not marked" style="padding:0">
            ${left.map(
              w => html`<md-assist-chip label=${w} @click=${() => this.addManual(w, 'other')}>
              ${icon('add', 'icon')}</md-assist-chip>`,
            )}
          </md-chip-set>
        </div>
      </md-outlined-card>`;
  }

  // ----- answer -----
  private answerView() {
    return html`
      <div class="single stack">
        <md-outlined-card>
          <md-tabs aria-label="Answer view" .activeTabIndex=${this.answerTab}
            @change=${(e: Event) => {
              this.answerTab = (
                e.target as unknown as {activeTabIndex: number}
              ).activeTabIndex;
            }}>
            <md-primary-tab>Answer</md-primary-tab>
            <md-primary-tab>What was sent</md-primary-tab>
          </md-tabs>
          ${
            this.answerTab === 0
              ? html`
            <div class="doc answer md-typescale-body-large">${restore(this.answerRaw, this.map)}</div>`
              : html`
            <div class="card-body">
              <div>
                <h3 class="md-typescale-label-large muted">Cleaned document and question sent for answering</h3>
                <div class="answer md-typescale-body-medium">${this.withPlaceholders(this.sent.doc)}</div>
              </div>
              <md-divider></md-divider>
              <div>
                <h3 class="md-typescale-label-large muted">Answer as the cloud AI wrote it</h3>
                <div class="answer md-typescale-body-medium">${this.withPlaceholders(this.answerRaw)}</div>
              </div>
            </div>`
          }
        </md-outlined-card>
        <div class="notice plain" role="status">
          ${icon('devices')}
          <div class="md-typescale-body-medium">Real names and numbers were put back on this device.
            Cloud cleanup received the approved preview; answering used its cleaned result. Check the answer before you rely on it.</div>
        </div>
        <div class="actions">
          <md-text-button @click=${this.startOver}>Start over</md-text-button>
          <md-filled-tonal-button @click=${() => {
            this.view = 'review';
          }}>Ask another question</md-filled-tonal-button>
        </div>
      </div>`;
  }

  // ----- dialogs -----
  private ruleDialogView() {
    const foia = this.ruleDialog === 'foia';
    const f =
      this.ruleDialog && !foia ? frameworkById(this.ruleDialog) : undefined;
    return html`
      <md-dialog ?open=${Boolean(f) || foia} @closed=${() => {
        this.ruleDialog = null;
      }}>
        <div slot="headline">${foia ? 'FOIA release (US)' : (f?.short ?? '')}</div>
        <div slot="content" class="dialog-list md-typescale-body-medium">
          ${
            foia
              ? html`
            <p>Prepares a record for release under the US Freedom of Information Act. Each withheld detail becomes a black box
              as long as the text it hides, labelled with its exemption at the place of the deletion, as the Act requires.</p>
            <p class="muted">Freedom of Information Act, <a href="https://www.law.cornell.edu/uscode/text/5/552" target="_blank" rel="noopener noreferrer">5 U.S.C. § 552(b)</a></p>
            <md-divider></md-divider>
            <div class="req"><div><span class="muted">(b)(6)</span> Personal details: names, contact details, IDs, accounts, health and other personal facts.</div></div>
            <md-divider></md-divider>
            <div class="req"><div><span class="muted">(b)(4)</span> Business details: organization names, business numbers and money amounts.</div></div>
            <md-divider></md-divider>
            <div class="req"><div><span class="muted">(b)(7)(C)</span> Added to personal details when you mark the record as a law enforcement record.</div></div>
            <md-divider></md-divider>
            <div class="req"><div class="muted">After Find private details, change the exemption for any data type or release it, then print or save
              the release as a PDF. FOIA release stays on this device. The defaults are a starting point, not a legal determination.</div></div>`
              : nothing
          }
          ${
            f
              ? html`
            <p>${f.summary}</p>
            <p class="muted">${f.name}, <a href=${f.url} target="_blank" rel="noopener noreferrer">${f.cite}</a></p>
            ${(f.requirements as Requirement[]).map(r => {
              const c = COVER[coverage(r)];
              return html`
                <md-divider></md-divider>
                <div class="req">
                  <div><span class="muted">${r.ref}</span> ${r.text}</div>
                  <div class="state md-typescale-label-large">${icon(c.icon)}${c.text}</div>
                  ${r.keep ? html`<div class="muted">The rule lets you keep ${KEEP[r.keep as keyof typeof KEEP].label}.</div>` : nothing}
                  ${r.gap ? html`<div class="muted">${r.gap}</div>` : nothing}
                </div>`;
            })}`
              : nothing
          }
        </div>
        <div slot="actions">
          <md-text-button @click=${() => {
            this.ruleDialog = null;
          }}>Close</md-text-button>
        </div>
      </md-dialog>`;
  }

  private saveFoia() {
    try {
      localStorage.setItem(
        FOIA_KEY,
        JSON.stringify({output: this.output, ...this.foia}),
      );
    } catch {
      /* ignore */
    }
  }
  private setOutput(output: 'ai' | 'foia') {
    if (this.output === output) return;
    this.output = output;
    this.copied = false;
    this.saveFoia();
  }
  private printRelease = () => {
    this.finishTypewriter();
    // Print a copy at the top of the page, so nothing else in the app takes
    // space on paper.
    requestAnimationFrame(() =>
      requestAnimationFrame(() => {
        const paper = this.querySelector('.doc.foia-paper');
        if (!paper) return;
        const root = document.createElement('div');
        root.id = 'print-root';
        root.append(paper.cloneNode(true));
        document.body.append(root);
        const done = () => {
          root.remove();
          removeEventListener('afterprint', done);
        };
        addEventListener('afterprint', done);
        window.print();
        setTimeout(done, 0);
      }),
    );
  };
  /** The release stamp agencies put at the top of a processed record. */
  private foiaStamp(dets: Detection[]) {
    const used = exemptionsUsed(dets, this.foia);
    return html`<div class="foia-stamp" aria-label=${used.length ? `Released in part. Exemptions ${used.join(', ')}` : 'Released in full'}>
      <span class="foia-stamp-title">${used.length ? 'Released in part' : 'Released in full'}</span>
      ${used.length ? html`<span class="foia-stamp-codes">${used.join('  ')}</span>` : nothing}
    </div>`;
  }
  /** The explanation of exemptions that accompanies a release. */
  private foiaLegend(dets: Detection[]) {
    const used = exemptionsUsed(dets, this.foia);
    if (!used.length) return nothing;
    return html`<div class="foia-legend">
      <strong>Exemptions applied (5 U.S.C. § 552(b))</strong>
      ${used.map(c => html`<div><span class="foia-legend-code">${c}</span> ${EXEMPTIONS.find(e => e.code === c)?.label ?? ''}</div>`)}
    </div>`;
  }
  /** One row per data type found: the exemption to cite, or release it. */
  private exemptionsCard(dets: Detection[]) {
    const kinds = new Map<string, {label: string; ids: string[]}>();
    for (const d of dets) {
      if (!d.defaultOn && !d.enabled) continue;
      const k = kinds.get(d.kind) ?? {label: d.label, ids: []};
      k.ids.push(d.id);
      kinds.set(d.kind, k);
    }
    const choices = [
      ...EXEMPTIONS.map(e => e.code).flatMap(c =>
        c === '(b)(6)' ? [c, '(b)(6), (b)(7)(C)'] : [c],
      ),
    ];
    const describe = (c: string) =>
      c === '(b)(6), (b)(7)(C)'
        ? 'Personal privacy, law enforcement record'
        : (EXEMPTIONS.find(e => e.code === c)?.label ?? '');
    const change = (kind: string, ids: string[], value: string) => {
      const was = this.foia.overrides[kind];
      const overrides = {...this.foia.overrides};
      if (value === defaultExemption(kind, this.foia.lawEnforcement)) {
        delete overrides[kind];
      } else {
        overrides[kind] = value;
      }
      this.foia = {...this.foia, overrides};
      if (value === RELEASE) this.toggle(ids, false);
      else if (was === RELEASE) this.toggle(ids, true);
      this.saveFoia();
    };
    return html`
      <md-outlined-card>
        <div class="card-body">
          <h2 class="md-typescale-title-medium">FOIA exemptions</h2>
          <p class="md-typescale-body-small muted">Each withholding is marked where it was made, as 5 U.S.C. § 552(b) requires. Change the exemption for a type, or release it.</p>
          <label class="foia-le">
            <md-checkbox .checked=${live(this.foia.lawEnforcement)}
              @change=${(e: Event) => {
                this.foia = {
                  ...this.foia,
                  lawEnforcement: (e.target as HTMLInputElement).checked,
                };
                this.saveFoia();
              }}></md-checkbox>
            <span class="md-typescale-body-medium">Law enforcement record<br><span class="md-typescale-body-small muted">Personal details also cite (b)(7)(C)</span></span>
          </label>
          ${
            kinds.size
              ? html`<div class="foia-rows">${[...kinds].map(([kind, k]) => {
                  const value =
                    this.foia.overrides[kind] ??
                    defaultExemption(kind, this.foia.lawEnforcement);
                  return html`
              <label class="foia-row">
                <span class="md-typescale-body-medium">${k.label} <span class="muted">(${k.ids.length})</span></span>
                <select .value=${live(value)} @change=${(e: Event) => change(kind, k.ids, (e.target as HTMLSelectElement).value)}>
                  ${choices.map(c => html`<option value=${c} ?selected=${c === value}>${c} ${describe(c)}</option>`)}
                  <option value=${RELEASE} ?selected=${value === RELEASE}>Release (do not withhold)</option>
                </select>
              </label>`;
                })}</div>`
              : html`<p class="md-typescale-body-medium">Nothing is withheld.</p>`
          }
        </div>
      </md-outlined-card>`;
  }

  private setDisplay(next: Partial<RedactobotApp['display']>) {
    this.display = {...this.display, ...next};
    const root = document.documentElement;
    if (this.display.theme === 'system') delete root.dataset.theme;
    else root.dataset.theme = this.display.theme;
    if (this.display.palette === 'cb') root.dataset.palette = 'cb';
    else delete root.dataset.palette;
    if (this.display.motion === 'reduced') {
      root.dataset.motion = 'reduced';
      this.finishTypewriter();
    } else {
      delete root.dataset.motion;
    }
    try {
      localStorage.setItem(DISPLAY_KEY, JSON.stringify(this.display));
    } catch {
      /* ignore */
    }
  }

  private displayDialogView() {
    type D = RedactobotApp['display'];
    const group = <K extends keyof D>(
      key: K,
      legend: string,
      options: Array<[D[K], string, string]>,
    ) => html`
      <fieldset class="display-group">
        <legend class="md-typescale-title-small">${legend}</legend>
        ${options.map(
          ([value, label, hint]) => html`
          <label class="display-option">
            <md-radio name=${key} .value=${String(value)} .checked=${live(this.display[key] === value)}
              @change=${() => this.setDisplay({[key]: value} as Partial<D>)}></md-radio>
            <span><span class="md-typescale-body-large">${label}</span>${hint ? html`<br><span class="md-typescale-body-small muted">${hint}</span>` : nothing}</span>
          </label>`,
        )}
      </fieldset>`;
    return html`
      <md-dialog ?open=${this.displayOpen} @closed=${() => {
        this.displayOpen = false;
      }}>
        <div slot="headline">Display</div>
        <div slot="content" class="dialog-list">
          ${group('theme', 'Theme', [
            [
              'system',
              'Match this computer',
              'Light or dark, as your system is set',
            ],
            ['light', 'Light', ''],
            ['dark', 'Dark', ''],
          ])}
          ${group('palette', 'Colours', [
            [
              'standard',
              'Standard',
              'Green for clean, orange to review, red for sensitive details',
            ],
            [
              'cb',
              'Colour-blind friendly',
              'Blue for clean, orange to review, purple with a dashed underline for sensitive details',
            ],
          ])}
          ${group('motion', 'Motion', [
            [
              'full',
              'Full',
              'Typing animation and the robot video while work runs',
            ],
            ['reduced', 'Reduced', 'No animation: results appear at once'],
          ])}
          <p class="md-typescale-body-small muted">Saved in this browser only.</p>
        </div>
        <div slot="actions"><md-text-button @click=${() => {
          this.displayOpen = false;
        }}>Done</md-text-button></div>
      </md-dialog>`;
  }

  private aboutDialogView() {
    return html`
      <md-dialog ?open=${this.aboutOpen} @closed=${() => {
        this.aboutOpen = false;
      }}>
        <div slot="headline">How this works</div>
        <div slot="content" class="dialog-list md-typescale-body-medium">
          <p><strong>1. Find.</strong> Numbers and contact details are found by fixed patterns. Names are found by
            an AI model that runs inside this browser. Your document is not sent anywhere for this.</p>
          <p><strong>2. Review.</strong> You see everything that was found and decide what is replaced.</p>
          <p><strong>3. Replace.</strong> Each detail becomes a placeholder such as [PERSON_1]. The list of which
            placeholder stands for which real value stays in this browser tab's memory and is never saved or sent.</p>
          <p><strong>4. Clean up and ask.</strong> The document and question pass a mandatory local identity check.
            After you approve the exact preview, cloud AI removes remaining sensitive facts and can answer using the cleaned result.</p>
          <p><strong>5. Restore.</strong> Real values are put back into the answer on this device.</p>
          <md-divider></md-divider>
          <p class="muted">Automatic checks can miss things, and this tool does not confirm that a document meets
            any rule. You are responsible for what you send. This is a technology demonstration: do not enter real
            sensitive data. <a href="/privacy.html">Privacy policy and terms of use</a></p>
          ${PROFESSIONAL_DUTIES.map(
            (d: {
              audience: string;
              summary: string;
              url: string;
              cite: string;
            }) => html`
            <p class="muted">${d.audience}: ${d.summary}
              <a href=${d.url} target="_blank" rel="noopener noreferrer">${d.cite}</a></p>`,
          )}
        </div>
        <div slot="actions">
          <md-text-button @click=${() => {
            this.aboutOpen = false;
          }}>Close</md-text-button>
        </div>
      </md-dialog>`;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'redactobot-app': RedactobotApp;
  }
}
