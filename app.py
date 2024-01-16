from flask import Flask, request, render_template_string,  jsonify
import sqlite3

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

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = request.args.get('user_id')

    # Directly using SQL within the Flask route handler
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Mixing database logic with business logic and HTML generation
        new_email = request.form['email']
        cursor.execute(f"UPDATE users SET email = '{new_email}' WHERE id = {user_id}")
        conn.commit()

        return render_template_string("""
            <html>
                <body>
                    <p>Email updated successfully!</p>
                    <a href="/profile?user_id={{ user_id }}">Back to Profile</a>
                </body>
            </html>
        """, user_id=user_id)

    cursor.execute(f"SELECT email FROM users WHERE id = {user_id}")
    user_email = cursor.fetchone()[0]

    # HTML embedded in Python code
    return render_template_string(f"""
        <html>
            <body>
                <form method="POST" action="/profile?user_id={user_id}">
                    <label for="email">Email:</label>
                    <input type="text" id="email" name="email" value="{user_email}">
                    <input type="submit" value="Update">
                </form>
            </body>
        </html>
    """)


@app.route('/profile2')
def profile2():
    user_id = request.args.get('user_id')
    user_email = get_user_email(user_id)
    return render_template('profile.html', user_id=user_id, email=user_email)

@app.route('/update_email', methods=['POST'])
def update_email():
    user_id = request.form['user_id']
    new_email = request.form['email']
    update_user_email(user_id, new_email)
    return redirect(url_for('profile', user_id=user_id))

def get_user_email(user_id):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    email = cursor.fetchone()[0]
    conn.close()
    return email

def update_user_email(user_id, new_email):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
