from flask import Blueprint, render_template, jsonify

# Import utilities
from ..utils.db_utils import get_db_connection, tuple_to_dict, release_db_connection
from ..utils.jenkins_utils import fetch_data_for_setup
from ..progress_manager import ProgressManager

web = Blueprint('web', __name__)


@web.route("/")
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

    
@web.route('/jenkins_data/<int:setup_id>')
def get_jenkins_data(setup_id):
    data = fetch_data_for_setup(setup_id)
    return jsonify(data)