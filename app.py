from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Colorado2021@localhost/flask_van_cities'
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

@app.route('/')
def index():
    return '<h1>Hello!</h1>'

if __name__ == '__main__':
    app.debug = True
    app.run() 