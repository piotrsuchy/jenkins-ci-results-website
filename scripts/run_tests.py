import os
import sys
import subprocess


def run_robot_tests():
    # Determine the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Add the project's root directory to the PYTHONPATH
    project_root = os.path.join(script_dir, "..")
    if "PYTHONPATH" in os.environ:
        os.environ["PYTHONPATH"] += os.pathsep + project_root
    else:
        os.environ["PYTHONPATH"] = project_root

    # Set the current working directory to the script's directory
    os.chdir(script_dir)

    # Determine paths for test files and the listener
    test_file_path = os.path.join(project_root, "tests", "example_tests.robot")
    listener_file_path = os.path.join(project_root, "tests", "PythonListener.py")

    subprocess.run(
        ["robot", "--listener", listener_file_path, test_file_path], env=os.environ
    )


if __name__ == "__main__":
    run_robot_tests()
