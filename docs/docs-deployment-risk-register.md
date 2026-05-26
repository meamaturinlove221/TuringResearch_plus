# Docs Deployment Risk Register

Status: strategy risk register.

Round: 332.

This register covers public docs deployment preparation for v1.5. It does not
record deployed docs or a live URL.

| Risk | Impact | Mitigation | Gate |
| --- | --- | --- | --- |
| Private files enter docs source list | privacy leak | allowlist public docs and examples only | public source scan |
| Generated HTML includes secrets | credential leak | scan source and output before publication | secret scan |
| Fake/demo output reads as observed evidence | public overclaim | require fake/demo labels and human review | evidence wording scan |
| Unsupported experiment success claim appears | credibility and safety issue | keep negative boundary wording | claim safety scan |
| ARIS appears implemented | roadmap confusion | enforce ARIS deferred docs | ARIS deferral check |
| Nonexistent public URL is documented | misleading release artifact | no real URL until human deployment | URL review |
| Analytics are enabled by convenience | privacy regression | analytics disabled by default | config review |
| Static provider config stores tokens | secret exposure | no provider tokens in repo | config/secret scan |
| Docs build fetches live content | reproducibility and privacy risk | local static build only | build policy check |
| Deployment bypasses human review | unsafe publication | manual review checklist | release gate |

## Residual Risk

Docs deployment always has some publication risk because visibility changes the
blast radius of wording, examples, and generated pages. v1.5 reduces that risk
by stopping at readiness, not automatic deployment.
