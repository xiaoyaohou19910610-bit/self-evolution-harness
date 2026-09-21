import shutil
import unittest
import uuid
from pathlib import Path

from tools.bootstrap import bootstrap


class BootstrapTests(unittest.TestCase):
    def test_creates_expected_files_and_skips_them_on_second_run(self):
        test_temp_root = Path(__file__).parent / ".tmp"
        test_temp_root.mkdir(exist_ok=True)
        root = test_temp_root / str(uuid.uuid4())
        root.mkdir()
        try:
            project = root / "project"
            skills = root / "skills"

            first = bootstrap(project, skills)
            self.assertTrue((project / "AGENTS.md").is_file())
            self.assertTrue((project / "memory" / "progress.md").is_file())
            self.assertTrue((skills / "self-evolution-project" / "SKILL.md").is_file())
            self.assertEqual(8, len(first.created))

            agents = project / "AGENTS.md"
            agents.write_text("custom project rules\n", encoding="utf-8")
            second = bootstrap(project, skills)

            self.assertEqual("custom project rules\n", agents.read_text(encoding="utf-8"))
            self.assertEqual(0, len(second.created))
            self.assertEqual(8, len(second.skipped))
        finally:
            shutil.rmtree(root)


if __name__ == "__main__":
    unittest.main()
