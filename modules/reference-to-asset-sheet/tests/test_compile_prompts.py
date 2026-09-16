import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("compile_prompts", ROOT / "scripts" / "compile_prompts.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CompilePromptsTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / "examples" / "butterfly-mail-plan.json").read_text(encoding="utf-8"))

    def test_example_compiles_all_sheets(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan_path = Path(tmp) / "plan.json"
            plan_path.write_text(json.dumps(self.plan, ensure_ascii=False), encoding="utf-8")
            outputs = MODULE.compile_files(plan_path)
            self.assertEqual(len(outputs), 2)
            prompt = outputs[0].read_text(encoding="utf-8")
            self.assertIn("3列×2行", prompt)
            self.assertIn("[large-butterfly]", prompt)
            self.assertIn(self.plan["style"], prompt)

    def test_rejects_duplicate_assignment(self):
        plan = copy.deepcopy(self.plan)
        plan["sheets"][1]["asset_ids"].append("yellow-star")
        with self.assertRaisesRegex(ValueError, "assigned more than once"):
            MODULE.validate(plan)

    def test_rejects_overfilled_sheet(self):
        plan = copy.deepcopy(self.plan)
        plan["sheets"][1]["columns"] = 1
        plan["sheets"][1]["rows"] = 1
        with self.assertRaisesRegex(ValueError, "exceeds"):
            MODULE.validate(plan)


if __name__ == "__main__":
    unittest.main()
