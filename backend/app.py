from flask import Flask, request, jsonify
from flask_cors import CORS
from keycloak import KeycloakOpenID
from db_wrapper import DatabaseWrapper
from functools import wraps

app = Flask(__name__)
CORS(app)

# Keycloak configuration
keycloak_openid = KeycloakOpenID(
    server_url="https://expert-disco-v6x6wrjvpp992x54r-8080.app.github.dev",
    client_id="frontend",
    realm_name="Registro",
)

db = DatabaseWrapper()

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(" ")[1]  # Bearer token
            token_info = keycloak_openid.introspect(token)
            if not token_info['active']:
                return jsonify({'message': 'Token is invalid'}), 401
            request.user = token_info
        except Exception as e:
            print(f"Token validation error: {e}")
            return jsonify({'message': 'Token is invalid', 'error': str(e)}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if role not in request.user.get('realm_access', {}).get('roles', []):
                return jsonify({'message': f'Insufficient permissions. Required role: {role}'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/votes', methods=['POST'], endpoint='insert_vote')
@token_required
@role_required('docente')
def insert_vote():
    try:
        data = request.get_json()
        student_name = data.get('student_name')
        subject = data.get('subject')
        vote = data.get('vote')
        
        if not student_name or not subject or vote is None:
            return jsonify({'message': 'Missing required fields'}), 400
        
        db.insert_vote(student_name, subject, vote)
        return jsonify({'message': 'Vote inserted successfully'}), 201
    except Exception as e:
        print(f"Error inserting vote: {e}")
        return jsonify({'message': 'Error inserting vote', 'error': str(e)}), 500

@app.route('/votes', methods=['GET'], endpoint='get_all_votes')
@token_required
@role_required('docente')
def get_all_votes():
    try:
        votes = db.get_all_votes()
        return jsonify(votes), 200
    except Exception as e:
        print(f"Error fetching votes: {e}")
        return jsonify({'message': 'Error fetching votes', 'error': str(e)}), 500

@app.route('/my-votes', methods=['GET'], endpoint='get_my_votes')
@token_required
@role_required('studente')
def get_my_votes():
    try:
        student_name = request.user.get('preferred_username')
        if not student_name:
            return jsonify({'message': 'Student name not found in token'}), 400
        votes = db.get_votes_by_student(student_name)
        return jsonify(votes), 200
    except Exception as e:
        print(f"Error fetching student votes: {e}")
        return jsonify({'message': 'Error fetching your votes', 'error': str(e)}), 500

@app.route('/subjects', methods=['GET'], endpoint='get_subjects')
@token_required
def get_subjects():
    try:
        subjects = db.get_subjects()
        return jsonify(subjects), 200
    except Exception as e:
        print(f"Error fetching subjects: {e}")
        return jsonify({'message': 'Error fetching subjects', 'error': str(e)}), 500

@app.route('/students', methods=['GET'], endpoint='get_students')
@token_required
@role_required('docente')
def get_students():
    try:
        students = db.get_students()
        return jsonify(students), 200
    except Exception as e:
        print(f"Error fetching students: {e}")
        return jsonify({'message': 'Error fetching students', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
