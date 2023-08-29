import os, psycopg2, json
from psycopg2 import sql
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.config['DB_CONN'] = psycopg2.connect(
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT")
)

conn = app.config['DB_CONN']

# filling setups table with records from config json
def populate_setups_table():
    with open('setups_config.json') as f:
        config = json.load(f)

    conn = app.config['DB_CONN']
    cur = conn.cursor()

    # Check if table is empty
    cur.execute("SELECT COUNT(*) FROM setups;")
    count = cur.fetchone()[0]
    if count > 0:
        print("Setups table already populated, skipping initialization.")
        cur.close()
        return

    for pipeline in config['pipelines']:
        insert_query = sql.SQL("INSERT INTO setups (name, comment) VALUES (%s, %s);")
        cur.execute(insert_query, (pipeline['setup'], pipeline.get('comment', '')))

    conn.commit()
    cur.close()

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

@app.route('/post_test_results', methods=['POST'])
def post_test_results():
    data = request.get_json()

    conn = app.config['DB_CONN']
    cur = conn.cursor()

    insert_query = sql.SQL("INSERT INTO tests (name, duration) VALUES (%s, %s) RETURNING test_id;")
    cur.execute(insert_query, (data['test_name'], data['duration']))
    test_id = cur.fetchone()[0]

    conn.commit()
    cur.close()

    return {"message": "Test results written to database", "test_id": test_id}, 200

@app.route('/post_scope_results', methods=['POST'])
def post_scope_results():
    data = request.get_json()
    response = {}

    try:
        conn = app.config['DB_CONN']
        cur = conn.cursor()

        # Your updated SQL query and operations here
        insert_query = """INSERT INTO scopes (setup_id, name, duration)
                          VALUES (%s, %s, %s) RETURNING scope_id;"""

        # Then use this default setup_id in the SQL query
        cur.execute(insert_query, (data['setup_id'], data['name'], data['duration']))

        conn.commit()
        scope_id = cur.fetchone()[0]

        response['message'] = 'Scope results successfully written to database.'
        response['scope_id'] = scope_id
        response['status'] = 'success'
        response['code'] = 200

        cur.close()

    except Exception as e:
        conn.rollback()
        print(f"Database Error: {e}")

        response['message'] = 'An error occurred while writing to the database.'
        response['status'] = 'error'
        response['code'] = 500

    return jsonify(response), response['code']

if __name__ == '__main__':
    # for development purposes atm:
    conn = app.config['DB_CONN']
    cur = conn.cursor()
    cur.execute("TRUNCATE setups, scopes, tests, jenkinsinfo, failingtestcases RESTART IDENTITY;")  # Replace 'table_name' with your actual table name
    conn.commit()
    cur.close()

    populate_setups_table()
    app.run(port=5000, debug=True)

    