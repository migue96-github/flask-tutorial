from flask import Flask, jsonify, request
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer

app = Flask(__name__)

DB_NAME = 'book.db'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, DB_NAME)}'

db = SQLAlchemy(app)


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
    return jsonify(data=[book.as_json() for book in books])


def _get_response(name: str, age: int):
    if age < 18:
        return jsonify(message='Should be 18 or older'), 401
    return jsonify(message=f'{name}, you are older than 18')


# Models
class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String, nullable=False)
    title = Column(String, nullable=False)

    def as_json(self):
        return {
            "id": self.id,
            "author": self.author,
            "title": self.title
        }

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
