# Trusted Local Demo Plugin

This fixture is demo-only. It is a local plugin manifest used to test trusted
local plugin loading.

It does not contain executable plugin code, dynamic entrypoints, credentials,
raw data, private paths, or model payloads.

Expected behavior:

- manifest loads from local path;
- plugin validation passes;
- built-in demo trust policy allows metadata loading;
- extension safety gate runs;
- capabilities remain disabled by default.
