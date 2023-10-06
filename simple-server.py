import psycopg2, json
from flask import Flask, request, render_template, jsonify

# Import utilities
from utils.db_utils import get_db_connection, tuple_to_dict, release_db_connection
from utils.jenkins_utils import fetch_data_for_setup
from progress_manager import ProgressManager

app = Flask(__name__)
progress_manager = ProgressManager()


# filling setups table with records from config json
def populate_setups_table():
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if table is empty
    cur.execute("SELECT COUNT(*) FROM setups;")
    count = cur.fetchone()[0]
    if count > 0:
        print("Setups table already populated, skipping initialization.")
        cur.close()
        release_db_connection(conn)
        return

    with open("setups_config.json") as f:
        config = json.load(f)

    for pipeline in config["pipelines"]:
        insert_query = psycopg2.sql.SQL(
            "INSERT INTO setups (name, comment) VALUES (%s, %s);"
        )
        cur.execute(insert_query, (pipeline["setup"], pipeline.get("comment", "")))

    conn.commit()
    cur.close()
    release_db_connection(conn)

test_results = []


@app.route("/")
def index():
    conn = get_db_connection()

    # Fetch setups from the database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM setups;")
    setups = [tuple_to_dict(row, cursor) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM scopes;")
    scopes_list = [tuple_to_dict(row, cursor) for row in cursor.fetchall()]

    # Create a dictionary with setup_id as key and its scopes as values
    scopes = {}
    for scope in scopes_list:
        if scope["setup_id"] in scopes:
            scopes[scope["setup_id"]].append(scope)
        else:
            scopes[scope["setup_id"]] = [scope]

    cursor.execute("SELECT * FROM tests;")
    tests_list = [tuple_to_dict(row, cursor) for row in cursor.fetchall()]

    # Create a dictionary with scope_id as key and its test as values
    tests = {}
    for test in tests_list:
        if test["scope_id"] in tests:
            tests[test["scope_id"]].append(test)
        else:
            tests[test["scope_id"]] = [test]

    cursor.close()
    release_db_connection(conn)

    return render_template("index.html", setups=setups, scopes=scopes, tests=tests)


@app.route("/post_message", methods=["POST"])
def post_message():
    message = request.form.get("message")
    progress = request.form.get("progress")
    suite_name, test_name, status, timestamp = message.split(", ")
    test_results.append(
        {
            "suite_name": suite_name.split(": ")[1],
            "test_name": test_name.split(": ")[1],
            "status": status.split(": ")[1],
            "timestamp": timestamp.split(": ")[1],
            "progress": progress,
        }
    )
    return "Message received", 200


@app.route("/post_test_results", methods=["POST"])
def post_test_results():
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()

    insert_query = psycopg2.sql.SQL(
        "INSERT INTO tests (name, start_time, scope_id) VALUES (%s, %s, %s) RETURNING test_id;"
    )
    cur.execute(insert_query, (data["test_name"], data["start_time"], data["scope_id"]))
    test_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    release_db_connection(conn)

    return {"message": "Test results written to database", "test_id": test_id}, 200


@app.route("/post_scope_results", methods=["POST"])
def post_scope_results():
    data = request.get_json()
    response = {}

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        insert_query = """INSERT INTO scopes (setup_id, name, start_time)
                          VALUES (%s, %s, %s) RETURNING scope_id;"""

        cur.execute(insert_query, (data["setup_id"], data["name"], data["start_time"]))

        conn.commit()
        scope_id = cur.fetchone()[0]

        response["message"] = "Scope results successfully written to database."
        response["scope_id"] = scope_id
        response["status"] = "success"
        response["code"] = 200

        cur.close()
        release_db_connection(conn)

    except Exception as e:
        conn.rollback()
        print(f"Database Error: {e}")

        response["message"] = "An error occurred while writing to the database."
        response["status"] = "error"
        response["code"] = 500

    return jsonify({
        "message": "Scope results successfully written to database.",
        "status": "success",
        "code": 200,
        "scope_id": scope_id
    }), 200


@app.route("/update_end_time", methods=["PUT"])
def update_end_time():
    data = request.get_json()
    table_name = data["table_name"]  
    
    # Check if provided table name is valid (you can expand this list as needed)
    if table_name not in ['tests', 'scopes']:
        return jsonify({"message": "Invalid table name", "status": "error", "code": 400}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        update_query = f"UPDATE {table_name} SET end_time = NOW(), status = %s WHERE {table_name[:-1]}_id = %s;"
        cur.execute(update_query, (data["status"], data["id"]))
        cur.execute(update_query, (data["status"], data["id"]))
        if cur.rowcount == 0:
            return jsonify({
                "message": f"No {table_name[:-1].capitalize()} found with provided ID or no update needed.",
                "status": "warning",
                "code": 404
            }), 404

        conn.commit()

        response = {
            "message": f"{table_name[:-1].capitalize()} end time updated successfully.",
            "status": "success",
            "code": 200
        }
    except Exception as e:
        conn.rollback()
        response = {
            "message": f"An error occurred: {e}",
            "status": "error",
            "code": 500
        }

    cur.close()
    release_db_connection(conn)
    return jsonify(response), response["code"]


@app.route("/current_test_data", methods=["GET"])
def current_test_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Use the new SQL Query
    cursor.execute("""
        WITH LatestScopes AS (
            SELECT
                s.setup_id,
                s.scope_id,
                s.name AS scope_name,
                s.start_time AS scope_start_time,
                s.status AS scope_status,
                ROW_NUMBER() OVER (PARTITION BY s.setup_id ORDER BY s.start_time DESC) as row_num
            FROM
                scopes s
        ),
        LatestTests AS (
            SELECT
                t.scope_id,
                t.name AS test_name,
                t.start_time AS test_start_time,
                t.status AS test_status,
                ROW_NUMBER() OVER (PARTITION BY t.scope_id ORDER BY t.start_time DESC) as row_num
            FROM
                tests t
        )
        SELECT
            ls.setup_id,
            ls.scope_name,
            ls.scope_start_time,
            ls.scope_status,
            lt.test_name,
            lt.test_start_time,
            lt.test_status
        FROM
            LatestScopes ls
        LEFT JOIN
            LatestTests lt ON ls.scope_id = lt.scope_id AND lt.row_num = 1
        WHERE
            ls.row_num = 1
            AND (ls.scope_status = 'running' OR lt.test_status = 'running');
    """)

    data = cursor.fetchall()
    results = [tuple_to_dict(t, cursor) for t in data]

    cursor.close()
    release_db_connection(conn)
    
    return jsonify(results)


@app.route('/update_progress/<string:setup_id>', methods=['POST'])
def update_progress(setup_id):
    data = request.json
    # print("Received data for update: ", data)
    progress_manager.update_progress(setup_id, data)
    return jsonify({"status": "success"})


@app.route('/get_progress_state/', methods=['GET'])
def get_progress_state():
    return jsonify(progress_manager.get_progress_state())

    
@app.route('/jenkins_data/<int:setup_id>')
def get_jenkins_data(setup_id):
    data = fetch_data_for_setup(setup_id)
    return jsonify(data)

    
if __name__ == "__main__":        
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SET timezone='UTC';")
    cur.execute(
        "TRUNCATE setups, scopes, tests, jenkinsinfo, failingtestcases RESTART IDENTITY;"
    )
    conn.commit()
    cur.close()
    release_db_connection(conn)

    populate_setups_table()
    app.run(port=5000, debug=True)