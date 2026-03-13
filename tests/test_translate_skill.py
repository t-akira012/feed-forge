import os
import re

import pytest

SKILL_PATH = "skills/translate/SKILL.md"


class TestTranslateSkill:
    def setup_method(self):
        with open(SKILL_PATH) as f:
            self.content = f.read()

    def test_skill_file_exists(self):
        assert os.path.exists(SKILL_PATH)

    def test_has_frontmatter(self):
        assert self.content.startswith("---")
        assert self.content.count("---") >= 2

    def test_frontmatter_has_name(self):
        assert "name: translate" in self.content

    def test_has_input_section(self):
        assert "## 入力" in self.content

    def test_has_output_section(self):
        assert "## 出力" in self.content

    def test_preserves_original_fields(self):
        assert "_original" in self.content

    def test_no_content_modification_policy(self):
        assert "改変" in self.content or "修正" in self.content

    def test_no_scripts_directory(self):
        assert not os.path.exists("skills/translate/scripts")
