# JENKINS CI RESULTS WEBSITE

This project is a prototype of a web server that will contain live-results for automated tests on CI setups.
The tests are being automatically run in Robot Framework.

## My starting requirements for the web server

Information we need is:

- setup IP or job name (like AT, ST etc.) - will be taken from jenkins parameters
- build being tested - robot framework listener
- test suite being tested - robot framework listener
- progress (which TC is being tested out of how many) - robot framework listener
- results - could be taken from either one 

## Summary of the project, requirements from others

Live view of the setups, visualised altogether on one page
Content:
- setup name
- which scope is being run
- jenkins info (last few runs, queue, status, stats and duration of tests)
- list of failing test cases
- karczoch link to logs
- pass or fail depending on number of failing tests (>= 80% pass is a passing run)