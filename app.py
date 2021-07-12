from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os 
# import psycopg2

load_dotenv()

DATABASE = os.getenv('DATABASE')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')


app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://(`DATABASE_USERNAME`):(`DATABASE_PASSWORD`)@localhost/(`DATABASE`)'
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Colorado2021@localhost/flask_van_cities'
db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__='posts'
    post_id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer)
    zip_code = db.Column(db.String)
    available_date = db.Column(db.String)
    contact_email = db.Column(db.String)
    image = db.Column(db.String)
    twenty_hookup = db.Column(db.Boolean)
    thirty_hookup = db.Column(db.Boolean)
    fifty_hookup = db.Column(db.Boolean)
    wifi = db.Column(db.Boolean)
    water = db.Column(db.Boolean)

    def __init__(self, contact_email, city_id, zip_code, available_date, image, twenty_hookup, thirty_hookup, fifty_hookup, wifi, water):
        self.contact_email = contact_email
        self.city_id = city_id
        self.zip_code =zip_code 
        self.available_date = available_date
        self.image = image
        self.twenty_hookup = twenty_hookup
        self.thirty_hookup = thirty_hookup
        self.fifty_hookup = fifty_hookup
        self.wifi = wifi
        self.water = water

    def __repr__(self):
        return '<Email %>' % self.contact_email

# @app.before_first_request
# def create_table():
#     db.create_all()

    
# @app.route('/')
# def index():
#     return '<h1>Hello!</h1>'


try:
    # con = psycopg2.connect(
    #     database=DATABASE,
    #     user=DATABASE_USERNAME,
    #     password=DATABASE_PASSWORD)

    # cur = con.cursor()

    # GET: Fetch all posts from the database
    @app.route('/cities')
    def fetch_all_posts():
        db.execute('SELECT * FROM posts')
        rows = db.fetchall()
        print(rows)

        return jsonify(rows)

    # GET: Fetch posts by cityId from the database
    @app.route('/cities/<int:city_id>')
    def fetch_by_id(city_id=None):
        db.execute(f'SELECT * FROM posts WHERE city_id = {city_id}')
        rows = db.fetchall()
        print(rows)

        return jsonify(rows)

    # POST: Create posts and add them to the database
    @app.route('/cities/<int:city_id>/create', methods=['GET', 'POST'])
    def add_post():
        if request.method == 'POST':
            data = request.form.to_dict()
            print(data)
            db.execute("INSERT INTO posts (post_id, city_id, zip_code, available_date, contact_email, image, twenty_hookup, thirty_hookup, fifty_hookup, wifi, water ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (f"{data['post_id']}", f"{data['city_id']}", data['zip_code'], f"{data['available_date']}",
                         f"{data['contact_email']}", f"{data['image']}", f"{data['twenty_hookup']}", data['thirty_hookup'], data['fifty_hookup'], data['wifi'], data['water']))
            db.commit()
            return 'Form submitted'
        else:
            return 'Form submission failed'

    # DELETE: Delete movie by movieId from the database
    @app.route('/cities/<int:city_id>', methods=['GET', 'DELETE'])
    def delete_by_post_id():
        post_id = request.form.to_dict()
        print(post_id['postId'])
        db.execute(
            f"DELETE FROM posts WHERE post_id = {post_id['postId']} RETURNING city_id")
        db.commit()

        return 'Post Deleted'

    # PUT: Update post by postId from the database
    @app.route('/cities/<int:city_id>/posts/<int:post_id>/edit', methods=['GET', 'PUT'])
    def update_by_post_id():

        db.execute(
            'UPDATE posts SET city_id = `/<int:city_id>/` WHERE post_id = <int:post_id>')
        db.commit()

        return 'Post Updated'

except:
    print('Error')


if __name__ == '__main__':
    app.debug = True
    app.run() 