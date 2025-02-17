from flask import Flask, render_template, request, redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return 'Email already exists. Please choose a different email.'
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['name'] = user.name
            session['email'] = user.email  
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid user')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if session['name']:
        user = User.query.filter_by(email=session['email']).first()
        

        return render_template('dashboard.html',user=user)
    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

    
# @app.route('/table')
# def table():
#     data = User.query.all()
#     for item in data:
#         print(item.name)

# Import your SQLAlchemy model

@app.route('/table')
def show_table():
    all_data = User.query.all()
    print(all_data)
    # data_list = []

    # for item in all_data:
    #     data_list.append(item)

    return render_template('table.html', data_list=all_data)

        
if __name__=='__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)
