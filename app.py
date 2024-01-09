from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database
users = {
    "123": {"userid": "123", "name": "Alice", "email": "alice@example.com"},
    "456": {"userid": "456", "name": "Bob", "email": "bob@example.com"},
    # Add more user records as needed
}

@app.route('/account', methods=['GET'])
def account():
    userid = request.args.get('userid')
    user_data = users.get(userid)
    if user_data:
        return jsonify(user_data)
    else:
        return "User not found", 404

if __name__ == '__main__':
    app.run(debug=True)
