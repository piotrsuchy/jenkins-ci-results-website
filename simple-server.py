from flask import Flask, request, render_template

app = Flask(__name__)

test_results = []

@app.route('/')
def index():
    return render_template('index.html', test_results=test_results)

@app.route('/post_message', methods=['POST'])
def post_message():
    message = request.form.get('message')
    progress = request.form.get('progress')
    suite_name, test_name, status, timestamp = message.split(", ")
    test_results.append({
        'suite_name': suite_name.split(": ")[1],
        'test_name': test_name.split(": ")[1],
        'status': status.split(": ")[1],
        'timestamp': timestamp.split(": ")[1],
        'progress': progress
    })
    return "Message received", 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
