import requests
import sys


class PythonListener:
    ROBOT_LISTENER_API_VERSION = 3
    def __init__(self, interval=10):
        self.interval = interval
        self.completed_tests = 0 
        
    def log_message(self, message):
        # Suppress all log messages
        pass


    def start_test(self, name, attributes):
        pass
    
    def end_test(self, data, result):
        timestamp = result.endtime
        suite_name = data.parent.name
        message1 = f"Suite Name: {suite_name}, Test Name: {data.name}, Status: {result.status}, Timestamp: {timestamp}"
        self.completed_tests += 1
        message2 = ''
        if self.completed_tests % self.interval == 0:
            message2 = '{self.completed_tests} test cases are done.\n'
        requests.post("http://127.0.0.1:5000/post_message", data={'message': message1, 'progress': message2})

    def end_suite(self, name, attributes):
        sys.stderr.write(f'Total test cases executed: {self.completed_tests}')