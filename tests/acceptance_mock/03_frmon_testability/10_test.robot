*** Settings ***
Library           BuiltIn
Library           OperatingSystem
Suite Setup 	  Run Keywords	Log 	Suite Setup started 	AND 	Sleep 	10s
Suite Teardown	  Run Keywords 	Log 	Suite Teardown started 	AND 	Sleep	 15s

*** Test Cases ***
Long Test Case 10_1
    Sleep    10
    Log    This is Long Test Case 1

Long Test Case 10_2
    Sleep    10
    Log    This is Long Test Case 2


