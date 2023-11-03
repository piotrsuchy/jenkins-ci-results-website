import psycopg2
from flask import Blueprint, request, jsonify
from flask import current_app

# Import utilities
from ..utils.db_utils import get_db_connection, tuple_to_dict, release_db_connection
from ..utils.general_utils import format_datetime_for_frontend

api = Blueprint('api', __name__)


@api.route("/post_test_results", methods=["POST"])
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


@api.route("/post_scope_results", methods=["POST"])
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


@api.route("/update_end_time", methods=["PUT"])
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


@api.route("/current_test_data", methods=["GET"])
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
            AND (ls.scope_status = 'startup' OR ls.scope_status = 'running' OR ls.scope_status = 'teardown' OR lt.test_status = 'running');
    """)

    data = cursor.fetchall()
    results = [tuple_to_dict(t, cursor) for t in data]
    # current_app.logger(f"results {results}")

    cursor.close()
    release_db_connection(conn)
    
    return jsonify(results)


@api.route('/update_progress/<string:setup_id>', methods=['POST'])
def update_progress(setup_id):
    data = request.json
    # print("Received data for update: ", data)
    current_app.progress_manager.update_progress(setup_id, data)
    return jsonify({"status": "success"})


@api.route('/get_progress_state/', methods=['GET'])
def get_progress_state():
    return jsonify(current_app.progress_manager.get_progress_state())


@api.route('/get_start_times/<setup_id>', methods=['GET'])
def get_start_times(setup_id):
    setup_start_time = current_app.setup_duration.get_setup_start_time(setup_id)
    teardown_start_time = current_app.teardown_duration.get_teardown_start_time(setup_id)

    if type(setup_start_time) is not None:
        current_app.logger.error(f"FOUND A START TIME THAT ISN't NONE")
        current_app.logger.error(setup_start_time)
        current_app.logger.error(type(teardown_start_time))

    # formatted_setup_start_time = format_datetime_for_frontend(setup_start_time)
    # formatted_teardown_start_time = format_datetime_for_frontend(teardown_start_time)

    return jsonify({
        'setup_start_time': setup_start_time,
        'teardown_start_time': teardown_start_time
    })


@api.route('/update_setup_start_time', methods=['POST'])
def update_setup_start_time():
    data = request.get_json()
    setup_id = data.get('setup_id')
    start_time = data.get('start_time')
    if setup_id and start_time:
        current_app.setup_duration.update_setup_start_time(setup_id, start_time)
        return jsonify({"message": "Setup start time updated successfully"}), 200
    return jsonify({"error": "Invalid data"}), 400


@api.route('/update_teardown_start_time', methods=['POST'])
def update_teardown_start_time():
    data = request.get_json()
    setup_id = data.get('setup_id')
    start_time = data.get('start_time')
    if setup_id and start_time:
        current_app.teardown_duration.update_teardown_start_time(setup_id, start_time)
        return jsonify({"message": "Teardown start time updated successfully"}), 200
    return jsonify({"error": "Invalid data"}), 400


@api.route("/last_test_end_time", methods=["GET"])
def last_test_end_time():
    suite_id = request.args.get('suite_id')
    if not suite_id:
        return jsonify({'error': 'suite_id is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            end_time
        FROM
            tests
        WHERE
            suite_id = %s
        ORDER BY
            end_time DESC
        LIMIT 1
    """, (suite_id,))

    data = cursor.fetchone()
    end_time = data[0] if data else None

    cursor.close()
    release_db_connection(conn)
    
    return jsonify({'end_time': end_time})


@api.route('/update_scope_status', methods=['PUT'])
def update_scope_status():
    data = request.json
    scope_id = data.get('scope_id')
    status = data.get('status')

    if not scope_id or not status:
        return jsonify({"error": "Missing required parameters"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Scopes SET status = %s WHERE scope_id = %s", (status, scope_id))
    conn.commit()
    release_db_connection(conn)

    return jsonify({"message": "Scope status updated successfully"})
