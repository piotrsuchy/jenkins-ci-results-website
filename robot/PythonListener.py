import requests

class PythonListener:

    ROBOT_LISTENER_API_VERSION = 3

    def end_test(self, data, result):
        message = f"Test {data.name} ended with status: {result.status}"
        requests.post("http://127.0.0.1:5000/post_message", data={'message': message})
