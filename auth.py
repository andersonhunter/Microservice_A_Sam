from flask import Flask, request
import json
import jwt
import requests


# Set the port for the server to receive data from the client
SERVER_PORT = 5001

# Set the route through which the client will call the auth server
SERVER_ROUTE = '/auth'

# Define user credentials for the auth program to check against
username = 'user'
password = 'Password3!'

# Define the encryption key for the JWT
key = 'change_me_please'


def login_auth(token):
    """
    Receives a JWT encoded using the HS256 algorithm.
    Decodes the token and verifies that the username and password match.
    The decoded token will be a dictionary in the form {'username': <username>, 'password': <password>}.
    Returns True if credentials are valid, and False otherwise
    """
    # Decode jwt object using hard-coded key
    decoded = jwt.decode(token, key, algorithms='HS256')

    # Index into decoded dictionary to get username and password
    u, p = decoded['username'], decoded['password']
    # print(f'User: {u}, Pass: {p}')

    # Authenticate username and password
    if u == username and p == password:
        return "True"
    return "False"


def main():
    app = Flask(__name__)

    @app.route(SERVER_ROUTE, methods=['POST'])
    def authorize():
        """
        Receives a JWT token.
        Passes the token to the auth function.
        Returns JSON stating True if login matches, and JSON stating False otherwise.
        """
        # Get the POSTed JSON data from the client
        response = request.get_json()
        # print(response)

        # Pull JWT from JSON data
        token = json.loads(response)["auth"]
        # print(token)

        # Authenticate login info and send result to client
        message = json.dumps({"auth": login_auth(token)})
        return message

    app.run(port=SERVER_PORT)


if __name__ == '__main__':
    main()

