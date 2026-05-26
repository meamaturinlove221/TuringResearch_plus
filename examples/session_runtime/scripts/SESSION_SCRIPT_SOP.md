# Session Shell Script Equivalent SOP



Status: review-only export.



These scripts are generated equivalents for manual review. They are not

executed by TuringResearch during export.



## Review Order



1. `preflight.sh`

2. `build-context-pack.sh`

3. `fake-transfer.sh`

4. `verify-return.sh`

5. `workflow-replay.sh`



## Safety Rules



- inspect every script before manual use;

- keep live steps commented unless a human explicitly reviews them;

- do not paste credentials into scripts;

- do not add destructive commands;

- do not add remote command execution;

- do not write Evidence Ledger entries automatically;



## Script Safety Summary



- `preflight.sh`: `pass`

- `build-context-pack.sh`: `pass`

- `fake-transfer.sh`: `pass`

- `verify-return.sh`: `pass`

- `workflow-replay.sh`: `pass`
