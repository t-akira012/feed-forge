import os, subprocess, sys, tempfile

CSS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "styles", "newspaper_style.css")


def render(md_path, html_path):
    os.makedirs(os.path.dirname(os.path.abspath(html_path)), exist_ok=True)
    css = os.path.abspath(CSS_PATH)
    # --standalone with --css (no --embed-resources) keeps remote image URLs intact
    # CSS is included as a <link> reference; we inline it via --include-in-header instead
    with open(css) as f:
        css_content = f.read()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as tmp:
        tmp.write(f"<style>\n{css_content}\n</style>\n")
        tmp_path = tmp.name
    try:
        subprocess.run(
            ["pandoc", md_path, "-o", html_path, "--standalone",
             "--include-in-header", tmp_path,
             "--metadata", "title=Daily Digest"],
            check=True,
        )
    finally:
        os.unlink(tmp_path)


def main():
    md_path = sys.argv[1]
    html_path = sys.argv[2]
    render(md_path, html_path)


if __name__ == "__main__":
    main()
