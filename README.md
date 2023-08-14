# JENKINS CI RESULTS WEBSITE

This project is a prototype of a web server that will contain live-results for automated tests on CI setups.
The tests are being automatically run in Robot Framework.

## Requirements for the web server

Information we need is:

- setup IP or job name (like AT, ST etc.)
- build being tested
- test suite being tested
- progress (which TC is being tested out of how many)
- results

We could get the information based on:

- jenkins
- directly from the setups using debug.log, which can read tests status (might need to download openSSH on Win10)
