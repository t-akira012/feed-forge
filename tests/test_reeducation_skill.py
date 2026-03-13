import os
import re

import pytest

SKILL_PATH = "skills/ideological-re-education/SKILL.md"


class TestReeducationSkill:
    def setup_method(self):
        with open(SKILL_PATH) as f:
            self.content = f.read()

    def test_skill_file_exists(self):
        assert os.path.exists(SKILL_PATH)

    def test_has_frontmatter(self):
        assert self.content.startswith("---")
        assert self.content.count("---") >= 2

    def test_frontmatter_has_name(self):
        assert "name: ideological-re-education" in self.content

    def test_has_rlhf_warning_field(self):
        assert "rlhf_warning" in self.content

    def test_has_rlhf_caution_field(self):
        assert "rlhf_caution" in self.content

    def test_no_translation_modification(self):
        assert "翻訳文の修正は一切行わない" in self.content or "翻訳文の修正は行わない" in self.content

    def test_has_detection_criteria(self):
        assert "意味の追加" in self.content
        assert "意味の省略" in self.content
        assert "トーンの変化" in self.content

    def test_has_annotation_examples(self):
        assert "```json" in self.content

    def test_has_fiction_expression_policy(self):
        assert "架空の未成年の性表現" in self.content

    def test_has_csam_fiction_distinction(self):
        assert "CSAM" in self.content
        assert "フィクション" in self.content

    def test_has_constitution_article_21(self):
        assert "日本国憲法21条" in self.content

    def test_no_scripts_directory(self):
        assert not os.path.exists("skills/ideological-re-education/scripts")
