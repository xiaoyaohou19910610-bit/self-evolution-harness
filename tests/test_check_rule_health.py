import unittest
from pathlib import Path

from tools.check_rule_health import check_manifest


FIXTURES = Path(__file__).parent / "fixtures" / "rule_health"


class RuleHealthTests(unittest.TestCase):
    def codes(self, manifest_name):
        return {finding.code for finding in check_manifest(FIXTURES / manifest_name)}

    def test_clean_fixture_passes(self):
        self.assertEqual(set(), self.codes("manifest-clean.json"))

    def test_missing_negative_scope_is_reported(self):
        self.assertIn("missing-negative-scope", self.codes("manifest-missing-scope.json"))

    def test_duplicate_bullet_is_reported(self):
        self.assertIn("duplicate-rule", self.codes("manifest-duplicate.json"))

    def test_contradictory_and_unknown_skills_are_reported(self):
        codes = self.codes("manifest-bad-cases.json")
        self.assertIn("contradictory-case", codes)
        self.assertIn("unknown-skill", codes)


if __name__ == "__main__":
    unittest.main()
