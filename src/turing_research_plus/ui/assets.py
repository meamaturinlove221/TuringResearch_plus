"""Static CSS assets for the lightweight dashboard."""


DEFAULT_CSS = """
:root {
  color-scheme: light;
  --bg: #f7f8fa;
  --panel: #ffffff;
  --text: #1f2937;
  --muted: #5b6472;
  --line: #d7dce3;
  --accent: #006b5f;
  --warn: #9f5b00;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  background: var(--bg);
  color: var(--text);
}
header {
  padding: 24px 32px;
  border-bottom: 1px solid var(--line);
  background: var(--panel);
}
main {
  max-width: 1180px;
  margin: 0 auto;
  padding: 24px;
}
section {
  padding: 18px 0;
  border-bottom: 1px solid var(--line);
}
h1, h2, h3 { margin: 0 0 12px; }
p, li { line-height: 1.5; }
pre {
  white-space: pre-wrap;
  background: #eef1f4;
  padding: 12px;
  border-radius: 6px;
  overflow-wrap: anywhere;
}
.meta {
  color: var(--muted);
  font-size: 0.92rem;
}
.badge {
  display: inline-block;
  border: 1px solid var(--line);
  border-left: 4px solid var(--accent);
  padding: 4px 8px;
  margin: 0 6px 6px 0;
  background: #fbfcfd;
}
.warning { border-left-color: var(--warn); }
footer {
  padding: 18px 32px;
  color: var(--muted);
  border-top: 1px solid var(--line);
}
"""
