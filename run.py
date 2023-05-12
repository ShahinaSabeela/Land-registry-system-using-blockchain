from flask import Flask,request,render_template
from blockchain import blockchain


app = Flask(__name__)

bc=blockchain()

def addData(msg):
    bc.create_block("reg",msg)
    if bc.validate_blockchain():
        print("data added successfully")
        return "success"
    else:
        print("failed")
        return "failed"

@app.route('/')
def home():    
    return render_template('home.html',names=names,rolls=rolls,times=times,l=l,totalreg=totalreg(),datetoday2=datetoday2) 

@app.route('/viewAdds', methods=['GET', 'POST'])
def viewAdds():

    return render_template('viewAdds.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        hashed_password = generate_password_hash(password)

        c.execute('SELECT * FROM users WHERE username=?', (username,))
        if c.fetchone():
            return render_template('reg.html', error='Username already exists')

        c.execute('INSERT INTO users (roledb,username, password) VALUES (?, ?, ?)', (role, username, hashed_password))
        conn.commit()

        session['username'] = username
        return redirect('/profile')

    return render_template('reg.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE username=?', (username,))
        user = c.fetchone()

        if not user:
            return render_template('login.html', error='Invalid username or password')

        if not check_password_hash(user[2], password):
            return render_template('login.html', error='Invalid username or password')

        session['username'] = username
        return redirect('/profile')

    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():

    return render_template('profile.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():

    return render_template('registrar.html')

@app.route('/payment', methods=['GET', 'POST'])
def payment():

    return render_template('payment.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
