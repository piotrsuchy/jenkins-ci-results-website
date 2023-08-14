from flask import Flask, request, render_template

app = Flask(__name__)

test_results = []

@app.route('/')
def index():
    return render_template('index.html', test_results=test_results)

@app.route('/post_message', methods=['POST'])
def post_message():
    message = request.form.get('message')
    name, status, timestamp = message.split(", ")
    test_results.append({
        'name': name.split(": ")[1],
        'status': status.split(": ")[1],
        'timestamp': timestamp.split(": ")[1]
    })
    return "Message received", 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
