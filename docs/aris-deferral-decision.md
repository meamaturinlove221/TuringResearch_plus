# ARIS Deferral Decision

Status: deferred from v1.2.

Round: 233.

ARIS is a strong future reference, but it does not enter the current v1.2
mainline.

## Decision

Decision: `DEFER ARIS FROM v1.2`.

v1.2 remains focused on original reference parity:

- Neocortica-Session parity;
- Neocortica-Scholar parity;
- Neocortica-Web parity;
- yogsoth-ai campaign / vault / ontology parity;
- MCP config parity;
- skill SOP parity;
- upstream strict diff;
- public demo refresh;
- full regression.

## Why Not v1.2

ARIS-style capabilities are valuable, but they carry higher stability and safety
risk than the current parity work:

- cross-model review loops can create opaque authority chains;
- meta-optimize can silently tune behavior without clear review boundaries;
- proof-checker surfaces can overstate correctness;
- paper-claim-audit and paper-writing automation can blur review aid versus
final claim generation;
- direct adoption would distract from reference parity and risk breaking the
currently runnable mainline.

## Timeline

- v1.2: original reference parity first.
- v1.3: ARIS study roadmap and safety design.
- v1.4: consider absorbing a small number of mature ARIS-inspired capabilities
  if design, tests, and safety review are complete.

## Binding Rules For v1.2

- Do not implement ARIS cross-model review loop.
- Do not implement ARIS meta-optimize.
- Do not implement ARIS proof-checker.
- Do not implement ARIS paper-writing automation.
- Do not replace human review with model review.
- Do not mark ARIS study items as implemented.
- Do not weaken fake/demo and observed-evidence boundaries.

## Relation To Paper Writing Beta

The existing paper writing beta remains a review-only scaffold. ARIS-inspired
paper-claim audit and paper resubmit ideas may inform v1.3 study, but they must
not turn v1.2 paper beta into final paper automation.
