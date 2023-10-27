# my_test.robot
*** Settings ***
Library           MyKeywords.py

*** Test Cases ***
Test Logging Keyword Execution Time
    Log Keyword Execution Time    Sleep    2s
