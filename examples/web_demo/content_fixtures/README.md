# Web Content Extraction Fixtures

Demo-only local fixtures for the `web_content` extraction path.

These files are fake public-page examples. They are used to show that the Web
tool surface can read local HTML fixtures, strip script/style noise, preserve
useful source text, and keep the output as review context.

Safety:

- No live network.
- No API key.
- No cookies.
- No login bypass.
- No paywall bypass.
- No private content scraping.
- No automatic evidence promotion.
- Human review required.

Fixture set:

- `project_page.html`: project-style page with title, overview, methods, and
  artifact notes.
- `paper_abstract.html`: paper-style page with abstract, contributions, and
  limitations.
- `noisy_navigation.html`: page with navigation, script, and style content that
  should not dominate extracted review text.
- `expected_extraction.md`: expected extraction behavior for human review.
