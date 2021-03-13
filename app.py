from flask import Flask,request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from cryptography import *
import json
from flask_restful import Api, Resource


app = Flask(__name__)
SECRET_KEY = 'p9Bv<3Eid9%$i01'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dt_admin:dt2016@localhost/dreamteam_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Authors(db.Model):
    Email = db.Column(db.String(120),primary_key = True)
    password = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(120))
    #phone = db.Column(db.Integer)
    #address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    #state = db.Column(db.String(120))
    #country = db.Column(db.String(120))
    #pincode = db.Column(db.Integer)

    def __init__(self,Email,password,full_name,city):
        self.Email = Email
        self.password = password
        self.full_name = full_name
        #self.phone = phone
        #self.address = address
        self.city = city
        #self.state = state
        #self.country = country
        #self.pincode = pincode


db.create_all()

#class AuthorSchema(ModelSchema):
class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Authors
        #sqla_session = db.session


    Email = fields.String(required=True)
    password = fields.String(required=True)
    full_name =fields.String(required=True)
    #phone = fields.Number()
    #address = fields.String(required=True)
    city = fields.String(required=True)
    #state = fields.String(required=True)
    #country = fields.String(required=True)
    #pincode = fields.Number()

@app.route('/authors',methods = ['GET'])
def index():
    get_authors = Authors.query.all()
    author_schema = AuthorSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors": authors}))

@app.route('/authorspost', methods = ['POST'])
def create_author():
    new_post = Authors(
            Email= request.json['Email'],
            password = "",
            full_name=request.json['full_name'],
            city=request.json['city']
    )
    db.session.add(new_post)
    db.session.commit()
    author_schema = AuthorSchema(many=True)
    authors = author_schema.dump(new_post)
    return make_response(jsonify({"authors": authors}))


class author_email():
    full_name = None
    city = None
    test = "Test"

    def __init__(self, full_name,city):
        self.full_name = full_name
        self.city = city

@app.route('/authors/<Email>', methods=["GET"])
def get_author_by_email(Email):
    #get_author = Authors.query.get(Email)
    #author_schema = AuthorSchema(many=True)
    #authors = author_schema.dump(get_author)
    s = author_email('forsyth',Email)
    return make_response(jsonify(vars(s)))

#api.add_resource(PostResource, '/authors/Email')

@app.route('/authorsdel/<Email>', methods = ["DELETE"])
def delete_author_by_id(Email):
    get_author = Authors.query.get(Email)

    db.session.delete(get_author)
    db.session.commit()
    return make_response("",204)

if __name__ == '__main__':
    app.run(debug=True)
