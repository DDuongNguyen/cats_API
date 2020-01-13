from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy 
# from flask_migrate import migrate
import os


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////cat.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db= SQLAlchemy(app)
# migrate = Mi

def validation(data,method):
    if(method == Combine or ReverseCombine or Anagram):
        if len(data)==2:
            return 200 
        else:
            return 300
CATS = [{
    "Momo":{
        "age": 5,
        "breed": "short hair",
        "sex": "F",
        "chonk_level": 10,
     },
    "Popo":{
        "age": 10,
        "breed": "siamese",
        "sex": "M",
        "chonk_level": 3,
     }
}]

# momo = Cats(age= 5,
#             breed= "short hair",
#             sex= "F",
#             chonk_level= 10,)

# popo = Cats(age= 10,
#             breed= "siamese",
#             sex= "M",
#             chonk_level= 5,)

class Cats(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    age= db.Column(db.Integer)
    breed= db.Column(db.String(50))
    sex= db.Column(db.String(10))
    chonk_level= db.Column(db.Integer)

    def __repr__(self):
        # return 'duong'
        return f'chonkiness:{self.chonk_level}'
        # return f'<Cat age:{str(self.age)},breed:{self.breed},sex{self.sex},chonkiness:{str(self.chonk_level)}'

class Combine(Resource):
    def post(self):
        postData = request.get_json()
        status_code= validation(postData,'Combine')
        if status_code == 200:
            test= postData.keys()
            cat1= list(postData.keys())[0]
            cat2= list(postData.keys())[-1]
            name1=postData[cat1]
            name2=postData[cat2]
            name3= name1 + name2
            return name3
        else:
            return{'status code':status_code, 'message': 'yo only 2 vairables allowed'}

class ReverseCombine(Resource):
    def post(self):
        data= request.get_json()
        status_code= validation(data, 'ReverseCombine')
        if status_code == 200:
            test = data.keys()
            cat1 = list(data.keys())[0]
            cat2 = list(data.keys())[-1]
            name1 = data[cat1]
            name2 = data[cat2]
            name3= name1+name2
            name3l = name3[::-1]
            return name3l
        else:
            return{'status code':status_code, 'message': 'yo only 2 vairables allowed'}

class Anagram(Resource):
    def post(self):
        data=request.get_json()
        status_code= validation(data, 'Anagram')
        if status_code == 200:
            word1 = list(data.values())[0]
            word2 = list(data.values())[-1]
            rw2= word2[::-1]
            if word1==rw2:
                return {'message':"das an anagram"}
            else:
                return {'message': "das not an anagram"}
        else:
            return{'status code':status_code, 'message': 'yo only 2 vairables allowed'}
                


api.add_resource(Combine, '/combine')
api.add_resource(ReverseCombine, '/rcombine')
api.add_resource(Anagram, '/anagram')

if __name__ == '__main__':
    app.run(debug=True)

