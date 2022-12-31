from flask import Flask, jsonify, request
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from flask_marshmallow import Marshmallow

app = Flask(__name__)

DB_NAME = 'book.db'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, DB_NAME)}'

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/bye')
def bye_world():
    return 'Bye'


@app.route('/not_found')
def not_found():
    return jsonify(message='Not found'), 404


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    return _get_response(name, age)


@app.route('/parameters/<string:name>/<int:age>')
def url_parameters(name: str, age: int):
    return _get_response(name, age)


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_serializer = BookSchema(many=True)
    results = books_serializer.dump(books)
    return jsonify(data=results)


def _get_response(name: str, age: int):
    if age < 18:
        return jsonify(message='Should be 18 or older'), 401
    return jsonify(message=f'{name}, you are older than 18')

@app.route ('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exist. '),409
    else:
        first_name = request.form['first_name' ]
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully. '),201
    

@app.route('/Users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_serializer = UserSchema(many=True)
    results = users_serializer.dump(users)
    return jsonify(data=results)

'''
Create an end-point /login
Use method POST and receive as a form email and password
If user exists with the same password and email -> respond user authenticated
Else -> respond user not authenticated
'''

@app.route ('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    test = User.query.filter_by(email=email, password=password).first()
    if test:
        return jsonify(message='User has logged in. ')
    else:
        return jsonify(message= 'Username/Password is not correct. ')

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String, nullable=False)
    title = Column(String, nullable=False)


class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author')

class UserSchema(ma.Schema):
    class Meta:
        fields = ('first_name', 'last_name', 'id', 'email')


# Commands


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('DB Created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('DB Drop!')


@app.cli.command('db_seed')
def db_seed():
    book1 = Book(title='Book1', author='Manolo')
    book2 = Book(title='Book2', author='Filiberto')

    db.session.add(book1)
    db.session.add(book2)

    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
