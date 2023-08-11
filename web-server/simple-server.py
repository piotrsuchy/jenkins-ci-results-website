from flask import Flask, request, render_template_string

app = Flask(__name__)
message = "No message received yet."

@app.route('/', methods=['GET'])
def index():
    return render_template_string("<h1>{{ message }}</h1>", message=message)

@app.route('/post_message', methods=['POST'])
def post_message():
    global message
    message = request.form.get('message')
    return "Message received", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
