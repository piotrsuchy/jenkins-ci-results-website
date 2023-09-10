import psycopg2, json
from flask import Flask, request, render_template, jsonify

# Import utilities
from utils.db_utils import get_db_connection, tuple_to_dict, release_db_connection

app = Flask(__name__)


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

    cursor.close()
    release_db_connection(conn)

    return render_template("index.html", setups=setups, scopes=scopes)


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
        "INSERT INTO tests (name, duration) VALUES (%s, %s) RETURNING test_id;"
    )
    cur.execute(insert_query, (data["test_name"], data["duration"]))
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
        insert_query = """INSERT INTO scopes (setup_id, name, duration)
                          VALUES (%s, %s, %s) RETURNING scope_id;"""

        cur.execute(insert_query, (data["setup_id"], data["name"], data["duration"]))

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

    return jsonify(response), response["code"]


if __name__ == "__main__":
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "TRUNCATE setups, scopes, tests, jenkinsinfo, failingtestcases RESTART IDENTITY;"
    )
    conn.commit()
    cur.close()
    release_db_connection(conn)

    populate_setups_table()
    app.run(port=5000, debug=True)
