import os

from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' Replacing with PostgreSQL
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'flaskdb')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.age}', '{self.color}')"

# Create the database and tables
with app.app_context():
    db.create_all()
    print("Database and tables created.")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('username')
        age = request.form.get('age')
        color = request.form.get('color')

        new_user = User(name=name, age=age, color=color)
        db.session.add(new_user)
        db.session.commit()
        print(f"User {name} added to the database.")

        return render_template('greetings.html', name=name, age=age, color=color)
    
    return render_template('form.html')

@app.route('/users')
def users():
    all_users = User.query.all()
    # if not all_users:
    #     return "No users found."
    return render_template('users.html', users=all_users)

@app.route('/about')
def about():
    return "This is the about page."

@app.route('/hello/<name>')
def hello_name(name):
    return f"Hello, {name}!"

# API route to get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'name': user.name, 'age': user.age, 'color': user.color} for user in users]
    return jsonify(user_list)

# API route to add a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or 'name' not in data or 'age' not in data or 'color' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'Missing required fields'}), 400
    

    new_user = User(name=data['name'], age=data['age'], color=data['color'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!',
                    'user':{
                        'id': new_user.id,
                        'name': new_user.name,
                        'age': new_user.age,
                        'color': new_user.color
                        }
                    }
                    ), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
