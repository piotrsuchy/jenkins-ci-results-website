import requests


class PythonListener:
    ROBOT_LISTENER_API_VERSION = 3

    def end_test(self, data, result):
        timestamp = result.endtime
        message1 = f"Test Name: {data.name}, Status: {result.status}, Timestamp: {timestamp}"
        requests.post("http://127.0.0.1:5000/post_message", data={'message': message1})

