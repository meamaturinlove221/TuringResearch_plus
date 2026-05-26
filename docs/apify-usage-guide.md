# Apify Usage Guide

Status: v1.2 usage guide.

Round: 238.

Apify support is optional live infrastructure for public web workflows. It is
disabled by default and is not required for quickstart, public demos, CI, or
fake/default tests.

## Default Mode

The default guide keeps:

- `default_live_enabled: false`;
- `TURINGRESEARCH_ENABLE_LIVE_TESTS=0`;
- `TURINGRESEARCH_ENABLE_APIFY_LIVE=0`;
- token env name: `APIFY_TOKEN`;
- no cookie storage;
- no paywall bypass;
- no private content fetch;
- human review required.

## No-key Behavior

If live mode is requested without a private `APIFY_TOKEN`, the adapter returns a
typed missing-token result. That is a graceful skip, not a public test failure.

## Private Local Use

Maintainers may configure an Apify token in a private local environment for
manual testing. The token must not be committed, copied into fixtures, or shown
in logs.

## Safety Boundary

Apify must not be used to bypass login, bypass paywalls, fetch private content,
store cookies, or create verified research claims automatically.
