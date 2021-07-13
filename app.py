from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os 

load_dotenv()

DATABASE = os.getenv('DATABASE')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

print (DATABASE)

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI']=f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/{DATABASE}"

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

    ## Method for Turning to Dictionary to send back as JSON
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


try:
    # con = psycopg2.connect(
    #     database=DATABASE,
    #     user=DATABASE_USERNAME,
    #     password=DATABASE_PASSWORD)

    # db = con.cursor()

    # GET: Fetch all posts from the database
    @app.route('/cities')
    def fetch_all_posts():
        all_posts = Post.query.all()
        print(all_posts)

        return {"posts": tuple(map(lambda p : p.as_dict(), all_posts))}

    # GET: Fetch posts by cityId from the database
    @app.route('/cities/<int:city_id>')
    def fetch_by_id(city_id=None):
        all_posts= Post.query.filter(city_id = city_id)

        return {"posts": tuple(map(lambda p : p.as_dict(), all_posts))}

    # POST: Create posts and add them to the database
    @app.route('/cities/<int:city_id>/create', methods=['POST'])
    def add_post(city_id, post_id):
        if request.method == 'POST':
            data = request.json()
            new_post = Post(post_id = post_id, city_id = city_id, zip_code = data["zip_code"], available_date = data["available_date"], contact_email = data["contact_email"], image = data["image"], twenty_hookup = data["twenty_hookup"], thirty_hookup = data["thirty_hookup"], fifty_hookup = data["fifty_hookup"], wifi = data["wifi"], water = data["water"])
            db.session.add(new_post)
            db.commit()
            return 'Form submitted'
        else:
            return 'Form submission failed'

    # DELETE: Delete post by postId from the database
    @app.route('/cities/<int:post_id>', methods=['DELETE'])
    def delete_by_post_id(post_id):
        post_id = request.json()
        post = Post.query.get(post_id)
        print(post_id['postId'])
        db.session.delete(post)
        db.session.commit()

        return 'Post Deleted'

    # PUT: Update post by postId from the database
    @app.route('/cities/<int:city_id>/posts/<int:post_id>/edit', methods=['PUT'])
    def update_by_post_id(city_id, post_id):
        data = request.json()
        post = Post.query.get(post_id).update
        db.session.commit()

        return 'Post Updated'

except:
    print('Error')


if __name__ == '__main__':
    app.debug = True
    app.run() 