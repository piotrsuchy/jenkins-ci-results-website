import os
import subprocess

def run_robot_tests():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_path = os.path.join(script_dir, '..', 'tests', 'example_tests.robot')
    listener_file_path = os.path.join(script_dir, '..', 'tests', 'PythonListener.py')
    subprocess.run(["robot", "--listener", listener_file_path, test_file_path])

if __name__ == "__main__":
    run_robot_tests()
