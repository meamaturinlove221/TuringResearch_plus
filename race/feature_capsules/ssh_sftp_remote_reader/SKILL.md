---

name: turingresearch-ssh_sftp_remote_reader

description: Use for v0.4 planning around SSH / SFTP Remote Artifact Reader. This capsule is a design skeleton and does not execute tools.

---



# SSH / SFTP Remote Artifact Reader Skill Capsule



Status: capsule-local skeleton.



Use this capsule when planning or reviewing `artifact.sftp_read_optional` work. It recommends scope,

contracts, tests, and safety gates only.



## When to use



- The task is about `SSH / SFTP Remote Artifact Reader`.

- The user asks for v0.4 remote artifact, dashboard, paper digest, advisor export,

  or release hardening planning.



## Inputs



- v0.4 scope docs.

- Handoff bundle docs.

- Run ingest reports.

- VGGT Research Knowledge Pack.



## Outputs



- Scope notes.

- Test plan.

- Risk notes.

- Proposed contract updates.



## Safety



Do not run network operations, remote commands, Modal, VGGT, or sync actions from

this capsule. Do not save secrets or package raw data.
