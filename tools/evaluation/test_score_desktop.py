# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Contract tests for coverage arithmetic and label handling, using fictional data."""

import contextlib
import csv
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from score_desktop import score


class DesktopScoring(unittest.TestCase):
    def run_fixture(
        self, text, annotations, spans, import_error=False, cloud_cleanup=False
    ):
        with tempfile.TemporaryDirectory(
            prefix="client-safe-scorer-"
        ) as directory:
            base = Path(directory).resolve()
            corpus, run = base / "source", base / "run"
            corpus.mkdir()
            (run / "local").mkdir(parents=True)
            (run / "nano").mkdir()
            (corpus / "fixture.txt").write_text(text, encoding="utf-8")
            with (run / "answerkey.csv").open(
                "w", encoding="utf-8", newline=""
            ) as output:
                writer = csv.writer(output)
                writer.writerow(
                    ["file", "pii_type", "text", "start_char", "end_char"]
                )
                for kind, value in annotations:
                    writer.writerow(
                        [
                            "fixture.txt",
                            kind,
                            value,
                            text.index(value),
                            text.index(value) + len(value),
                        ]
                    )
            manifest = {
                "corpus": str(corpus),
                "answerkeySha256": hashlib.sha256(
                    (run / "answerkey.csv").read_bytes()
                ).hexdigest(),
                "files": [{"name": "fixture.txt", "index": 0}],
            }
            if import_error:
                manifest["files"][0]["importError"] = "Unsupported format"
            (run / "manifest.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            utf16 = lambda value: len(value.encode("utf-16-le")) // 2
            detections = [
                {
                    "text": value,
                    "start": utf16(text[: text.index(value)]),
                    "end": utf16(text[: text.index(value) + len(value)]),
                    "kind": kind,
                    "enabled": True,
                }
                for kind, value in spans
            ]
            (run / "local" / "0.json").write_text(
                json.dumps(
                    {"text": text, "findings": detections, "elapsedMs": 2}
                ),
                encoding="utf-8",
            )
            if cloud_cleanup:
                (run / "nano" / "0.json").write_text(
                    json.dumps(
                        {
                            "report": {
                                "complete": True,
                                "findings": [
                                    {**d, "bucket": "cloud-cleanup"}
                                    for d in detections
                                ],
                            },
                            "elapsedMs": 2,
                            "gate": "eligible",
                        }
                    ),
                    encoding="utf-8",
                )
            with contextlib.redirect_stdout(io.StringIO()):
                result = score(run)
            return result

    def test_labels_full_value_and_partial_unicode_name_are_distinct(self):
        result = self.run_fixture(
            "Chart # 12345. A😀 B. 5555555555554444.",
            [
                ("MRN", "Chart # 12345"),
                ("NAME", "A😀 B"),
                ("CREDIT_CARD", "5555555555554444"),
            ],
            [
                ("record", "12345"),
                ("person", "A😀"),
                ("card", "5555555555554444"),
            ],
        )
        local = result["results"]["local"]
        self.assertEqual(result["key_offset_errors"], [])
        self.assertEqual(local["totals"]["full"], 2)
        self.assertEqual(local["totals"]["partial"], 1)
        self.assertEqual(local["categories"]["MRN"]["strict_phrase_full"], 0)
        self.assertEqual(local["categories"]["MRN"]["category_correct"], 1)
        self.assertEqual(
            local["documents"].get("zero_residual_annotated_identifiers", 0), 0
        )
        self.assertEqual(result["results"]["nano"]["documents"]["pending"], 1)

    def test_a_label_is_not_a_license_to_ignore_an_identifier_prefix(self):
        result = self.run_fixture(
            "MRN12345.", [("MRN", "MRN12345")], [("record", "12345")]
        )
        self.assertEqual(
            result["results"]["local"]["categories"]["MRN"]["partial"], 1
        )

    def test_complete_removal_does_not_imply_correct_category(self):
        result = self.run_fixture(
            "Chart # 12345.", [("MRN", "Chart # 12345")], [("person", "12345")]
        )
        category = result["results"]["local"]["categories"]["MRN"]
        self.assertEqual(category["full"], 1)
        self.assertEqual(category["category_correct"], 0)

    def test_import_failures_count_against_coverage(self):
        result = self.run_fixture(
            "Chart # 12345.", [("MRN", "Chart # 12345")], [], import_error=True
        )
        for mode in ("local", "nano"):
            category = result["results"][mode]["categories"]["MRN"]
            self.assertEqual(category["total"], 1)
            self.assertEqual(category["import_lost"], 1)
            self.assertEqual(category["full_removal_percent"], 0)

    def test_a_cloud_cleanup_finding_is_not_a_local_identity_removal(self):
        result = self.run_fixture(
            "Avery Rowan.",
            [("NAME", "Avery Rowan")],
            [("health", "Avery Rowan")],
            cloud_cleanup=True,
        )
        nano = result["results"]["nano"]
        self.assertEqual(nano["categories"]["NAME"]["full"], 1)
        self.assertEqual(
            nano["categories"]["NAME"]["mandatory_identity_full"], 0
        )
        self.assertEqual(
            nano["documents"]["eligible_with_residual_identifier"], 1
        )


if __name__ == "__main__":
    unittest.main()
