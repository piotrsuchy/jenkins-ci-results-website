*** Settings ***
Library           BuiltIn

*** Keywords ***
Add
    [Arguments]    ${a}    ${b}
    ${result}=    Evaluate    ${a} + ${b}
    [Return]      ${result}

Subtract
    [Arguments]    ${a}    ${b}
    ${result}=    Evaluate    ${a} - ${b}
    [Return]      ${result}

Multiply
    [Arguments]    ${a}    ${b}
    ${result}=    Evaluate    ${a} * ${b}
    [Return]      ${result}

Divide
    [Arguments]    ${a}    ${b}
    ${result}=    Evaluate    ${a} / ${b}
    [Return]      ${result}


*** Test Cases ***
Test Case 1
    [Documentation]    A simple addition test
    ${result}=    Add    5    5
    Should Be Equal As Numbers    ${result}    10

Test Case 2
    ${result}=    Subtract    10    3
    Should Be Equal As Numbers    ${result}    7

Test Case 3
    ${result}=    Multiply    2    4
    Should Be Equal As Numbers    ${result}    8

Test Case 4
    ${result}=    Divide    9    3
    Should Be Equal As Numbers    ${result}    3

Test Case 5
    ${result}=    Add    15    15
    Should Be Equal As Numbers    ${result}    30

Test Case 6
    ${result}=    Subtract    20    10
    Should Be Equal As Numbers    ${result}    10

Test Case 7
    ${result}=    Multiply    3    5
    Should Be Equal As Numbers    ${result}    15

Test Case 8
    ${result}=    Divide    18    6
    Should Be Equal As Numbers    ${result}    3

Test Case 9
    ${result}=    Add    6    4
    Should Be Equal As Numbers    ${result}    10

Test Case 10
    ${result}=    Subtract    10    5
    Should Be Equal As Numbers    ${result}    5
