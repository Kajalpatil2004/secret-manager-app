import os
from flask import Flask, render_template, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

# Load or generate encryption key (for demo; use env var or vault in production)
KEY_FILE = 'secret.key'

def get_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
        return key

fernet = Fernet(get_key())

SECRETS_FILE = 'secrets.db'

def load_secrets():
    secrets = {}
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(':', 1)
                if len(parts) == 2:
                    secrets[parts[0]] = parts[1]
    return secrets

def save_secrets(secrets):
    with open(SECRETS_FILE, 'w') as f:
        for k, v in secrets.items():
            f.write(f"{k}:{v}\n")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/secret', methods=['POST'])
def add_secret():
    name = request.form.get('name')
    value = request.form.get('value')
    if not name or not value:
        return jsonify({"error": "Both name and value are required"}), 400
    secrets = load_secrets()
    secrets[name] = fernet.encrypt(value.encode()).decode()
    save_secrets(secrets)
    return jsonify({"status": "success"})

@app.route('/secret/<name>', methods=['GET'])
def get_secret(name):
    secrets = load_secrets()
    enc = secrets.get(name)
    if not enc:
        return jsonify({"error": "Secret not found"}), 404
    try:
        secret_value = fernet.decrypt(enc.encode()).decode()
    except Exception as e:
        return jsonify({"error": "Decryption failed"}), 500
    return jsonify({"secret": secret_value})

@app.route('/secret/<name>', methods=['DELETE'])
def delete_secret(name):
    secrets = load_secrets()
    if name in secrets:
        del secrets[name]
        save_secrets(secrets)
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Secret not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
