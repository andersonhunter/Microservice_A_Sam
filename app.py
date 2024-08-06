from flask import Flask, render_template, request
import os
import jwt
import requests
import json

# Configuration

app = Flask(__name__)


# Routes

@app.route('/')
def test():
    return render_template('test.html')


@app.route('/login', methods=['GET', 'POST'])
def auth():
    # Encode username and password as JWT
    key = 'change_me_please'
    u, p = request.form.get('username'), request.form.get('password')
    print(f'Entered username: {u}, Given password: {p}')
    encoded = jwt.encode({'username': u, 'password': p}, key, algorithm='HS256')
    jwt_dict = {"auth": encoded}
    print(f'Sending {jwt_dict} to auth server')
    login = requests.post('http://127.0.0.1:5001/auth', json=json.dumps(jwt_dict)).json()['auth']
    print(f'Auth server sent back: {login}')
    if login == "True":
        print("User login accepted")
        return render_template('success.html')
    if login == "False":
        print("User login rejected")
        return render_template('failure.html')


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port)
