import os
import subprocess
import tempfile

import pytest

SCRIPT = "skills/pandoc-render/scripts/render.py"
CSS = "styles/newspaper_style.css"


class TestPandocRender:
    def test_script_exists(self):
        assert os.path.exists(SCRIPT)

    def test_css_exists(self):
        assert os.path.exists(CSS)

    def test_renders_html(self):
        with tempfile.TemporaryDirectory() as d:
            md_path = os.path.join(d, "test.md")
            html_path = os.path.join(d, "test.html")
            with open(md_path, "w") as f:
                f.write("# Test\n\n## Section\n\n### [Article](https://example.com)\nSummary text.\n")
            r = subprocess.run(
                ["python", SCRIPT, md_path, html_path],
                capture_output=True, text=True
            )
            assert r.returncode == 0, r.stderr
            assert os.path.exists(html_path)

    def test_html_contains_css(self):
        with tempfile.TemporaryDirectory() as d:
            md_path = os.path.join(d, "test.md")
            html_path = os.path.join(d, "test.html")
            with open(md_path, "w") as f:
                f.write("# Test\n")
            subprocess.run(["python", SCRIPT, md_path, html_path], capture_output=True)
            with open(html_path) as f:
                html = f.read()
            assert "<style>" in html or "newspaper_style" in html

    def test_html_has_title_link(self):
        with tempfile.TemporaryDirectory() as d:
            md_path = os.path.join(d, "test.md")
            html_path = os.path.join(d, "test.html")
            with open(md_path, "w") as f:
                f.write("### [My Article](https://example.com/article)\nDesc.\n")
            subprocess.run(["python", SCRIPT, md_path, html_path], capture_output=True)
            with open(html_path) as f:
                html = f.read()
            assert 'href="https://example.com/article"' in html
            assert "My" in html and "Article" in html

    def test_creates_output_dir(self):
        with tempfile.TemporaryDirectory() as d:
            md_path = os.path.join(d, "test.md")
            html_path = os.path.join(d, "sub", "dir", "test.html")
            with open(md_path, "w") as f:
                f.write("# Test\n")
            r = subprocess.run(
                ["python", SCRIPT, md_path, html_path],
                capture_output=True, text=True
            )
            assert r.returncode == 0
            assert os.path.exists(html_path)
