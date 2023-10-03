# Navigate to the "tests" directory relative to the script location
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location -Path "$scriptPath/../tests"

# Run the robot command
robot -r NONE -l NONE -o NONE --listener PythonListener.py example_tests.robot

# Navigate back to the original directory
Set-Location -Path $scriptPath
