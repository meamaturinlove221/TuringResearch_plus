# VGGT Case Study

Status: draft, public-safe, not promoted
Round: Optional 338.5
Date: 2026-05-25

## Overview

This split-ready draft describes how TulingResearch Plus uses local scan metadata to prepare a public-safe VGGT case study. It is a derived documentation package, not a data package.

The main TulingResearch Plus repository remains flagship. This split case is a small, reviewable artifact for explaining the VGGT dogfooding workflow and claim-safety boundaries.

## Evidence Summary

| Evidence area | Status | Public-safe summary |
| --- | --- | --- |
| Local scan summaries | observed | TulingResearch Plus generated scan summaries and a local evidence ledger. |
| VGGT report metadata | local-observed | The scan found lightweight report and manifest evidence for selected work streams. |
| Visual inventory metadata | local-observed | Visual evidence classes were inventoried without copying images or pointclouds. |
| SparseConv3D success | requires-human-review | The current evidence does not support a success claim. |
| Advisor approval | requires-human-review | No advisor approval is claimed. |
| Public release readiness | requires-human-review | This directory is a draft that needs human approval. |

## Public-Safe Narrative

TulingResearch Plus can serve as a workflow and evidence-control layer for a local VGGT research project. In this case, the system reads local scan summaries, converts them into a public-safe narrative, and blocks unsupported claims about experiment success, SparseConv3D backend status, advisor acceptance, and promotion.

## Exclusions

- No raw data.
- No SMPL-X model files.
- No private paths.
- No huge artifacts.
- No VGGT experiment archives.
- No unsupported success claims.

## Release Posture

This case is ready for human review, not public release. A maintainer must review the claim safety report and privacy report before any package is published or linked externally.
