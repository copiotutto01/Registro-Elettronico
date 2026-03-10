from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from jose import jwt
from jose.exceptions import JWTError
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from db_wrapper import DatabaseWrapper
from functools import wraps

app = Flask(__name__)
CORS(app)


# Keycloak config
KEYCLOAK_URL = "https://legendary-xylophone-r4j7wpjp979w3x4q4-8080.app.github.dev"
KEYCLOAK_REALM = "Registo"
KEYCLOAK_CLIENT_ID = "frontend"

# Scarica la chiave pubblica del realm

def get_keycloak_jwks():
    url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def jwk_to_pem(jwk):
    # Solo per chiavi RSA
    n = int.from_bytes(base64.urlsafe_b64decode(jwk['n'] + '=='), 'big')
    e = int.from_bytes(base64.urlsafe_b64decode(jwk['e'] + '=='), 'big')
    pubkey = rsa.RSAPublicNumbers(e, n).public_key(default_backend())
    pem = pubkey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem

JWKS = get_keycloak_jwks()

db = DatabaseWrapper()


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token_header = request.headers.get('Authorization')
        print("[DEBUG] Authorization header:", token_header)
        if not token_header:
            print("[DEBUG] Token is missing in header")
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token_parts = token_header.split(" ")
            if len(token_parts) != 2 or token_parts[0] != "Bearer":
                print("[DEBUG] Authorization header malformato:", token_header)
                return jsonify({'message': 'Malformed Authorization header'}), 401
            token = token_parts[1]
            print("[DEBUG] JWT token:", token)
            jwks = get_keycloak_jwks()
            unverified_header = jwt.get_unverified_header(token)
            print("[DEBUG] JWT header:", unverified_header)
            kid = unverified_header.get('kid')
            key = None
            alg = None
            for jwk in jwks['keys']:
                if jwk['kid'] == kid:
                    key = jwk_to_pem(jwk)
                    alg = jwk['alg']
                    break
            if not key:
                print("[DEBUG] Public key not found for token (kid):", kid)
                return jsonify({'message': 'Public key not found for token'}), 401
            try:
                payload = jwt.decode(
                    token,
                    key,
                    algorithms=[alg],
                    audience=KEYCLOAK_CLIENT_ID,
                    options={"verify_aud": True, "verify_exp": True}
                )
                print("[DEBUG] Token payload:", payload)
                request.user = payload
            except Exception as decode_error:
                print(f"[DEBUG] Token decode error: {decode_error}")
                return jsonify({'message': 'Token is invalid', 'error': str(decode_error)}), 401
        except JWTError as e:
            print(f"[DEBUG] JWTError: {e}")
            return jsonify({'message': 'Token is invalid', 'error': str(e)}), 401
        except Exception as e:
            print(f"[DEBUG] Generic token validation error: {e}")
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
        
        note = data.get('note')
        db.insert_vote(student_name, subject, vote, note)
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
    app.run(host='0.0.0.0', port=5002, debug=True)
