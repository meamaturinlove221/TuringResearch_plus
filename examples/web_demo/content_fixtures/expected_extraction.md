# Expected Extraction Behavior

The fixture workflow should:

- Extract the HTML title.
- Convert visible body text into compact plain text.
- Remove script and style content.
- Preserve method, artifact, contribution, and limitation notes.
- Keep output as review context.
- Avoid marking fake/demo content as verified evidence.

The fixture workflow should not:

- Fetch live pages.
- Store cookies.
- Bypass login or paywall controls.
- Treat fake citations as verified citations.
- Promote extracted text into observed evidence.
