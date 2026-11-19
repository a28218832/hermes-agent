"""Branch F（E2 hard rule, 2026-11-19）：inline pkill -f 自指攔截的規格。

來源：071/076/078 session 三次自殺事故（pattern 出現在 wrapper 的 cmdline 裡）。
對應外部規格：~/projects/20261118_hard_rules/specs/test_central.py::E2HermesSide。
"""
import unittest

from cron.lifecycle_guard import contains_self_referential_pkill


class BranchFBlocks(unittest.TestCase):
    def test_blocks_inline_pkill_f(self):
        self.assertTrue(contains_self_referential_pkill("pkill -f ff_dbg"))

    def test_blocks_combined_short_flag(self):
        self.assertTrue(contains_self_referential_pkill("pkill -fx dbg"))

    def test_blocks_long_full_flag(self):
        self.assertTrue(contains_self_referential_pkill("pkill --full dbg"))

    def test_blocks_inside_chain(self):
        self.assertTrue(contains_self_referential_pkill("echo hi; pkill -f foo"))

    def test_blocks_multiline(self):
        self.assertTrue(contains_self_referential_pkill("ls\necho x\npkill -f ffmpeg_debug"))


class BranchFAllows(unittest.TestCase):
    def test_allows_pidfile_form(self):
        self.assertFalse(contains_self_referential_pkill("pkill -F /run/service.pid"))

    def test_allows_name_pkill(self):
        self.assertFalse(contains_self_referential_pkill("pkill firefox"))

    def test_allows_pgrep(self):
        # pgrep -f 自-match 只是回報誤報，不致命——不擋（已知 quirk）
        self.assertFalse(contains_self_referential_pkill("pgrep -f foo | wc -l"))

    def test_allows_plain_commands(self):
        self.assertFalse(contains_self_referential_pkill("ls -la /tmp && grep -f pattern file"))


if __name__ == "__main__":
    unittest.main()
