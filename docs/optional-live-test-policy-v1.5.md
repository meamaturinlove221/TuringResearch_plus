# Optional Live Test Policy v1.5

Status: test policy locked.

Round: 344.

Live tests are opt-in and skipped by default. The default test suite must remain
credential-free, network-free, SSH-free, and safe to run on a local machine.

## Default Behavior

| Test type | Default result |
| --- | --- |
| fake Scholar tests | run |
| fake Web / Apify tests | run |
| fake SFTP transfer tests | run |
| live Scholar tests | skipped |
| live Web / Apify tests | skipped |
| live SFTP tests | skipped |

## Required Opt-in

Every live test must require:

```text
TURINGRESEARCH_ENABLE_LIVE_TESTS=1
```

Provider-specific tests must also require their own explicit flag and private
credential where applicable:

```text
TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=1
TURINGRESEARCH_ENABLE_WEB_LIVE=1
TURINGRESEARCH_ENABLE_APIFY_LIVE=1
SEMANTIC_SCHOLAR_API_KEY=<private local value>
APIFY_TOKEN=<private local value>
TURINGRESEARCH_SFTP_CREDENTIAL=<private local value>
```

These values must not appear in committed files.

## Test Assertions

Default tests should assert:

- live tests are skipped by default;
- fake tests require no API key;
- committed config has blank credential placeholders;
- no secrets are logged;
- live output is not treated as observed evidence;
- no remote commands are executed.

## CI Boundary

Public CI should run fake/default tests only unless a future private CI policy
explicitly opts into live tests with protected secrets. Public CI must not store
or print live credentials.
