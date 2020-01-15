from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import os
import requests
import json
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cat.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def validation(data, method):
    if(method == Combine or ReverseCombine or Anagram):
        if len(data) == 2:
            return 200
        else:
            return 300


# momo = Cat(age= 5,
#             breed= "short hair",
#             sex= "F",
#             chonk_level= 10,)

class Cat(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    breed = db.Column(db.String(50))
    sex = db.Column(db.String(10))
    chonk_level = db.Column(db.Integer)
    image_url = db.Column(db.String(1000))

    def __repr__(self):
        return f" name: {self.name}, age: {self.age}, breed: {self.breed}, sex: {self.sex}, chonkiness:{self.chonk_level}, url:{self.image_url}"

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "breed": self.breed,
            "sex": self.sex,
            "chonk_level": self.chonk_level,
            "image_url": self.image_url
        }




class Feline(Resource):
    def get(self, id):
        cat = Cat.query.filter_by(id=id).first()
        return cat.json()

    def put(self, id):
        update_data = request.get_json()
        # if update_data['age']:
        #     # check logic
        #     return {"error":"the gage"}, 400

        newCat = Cat.query.get(id).json()

        newCat.update(update_data)
        dbcat= Cat.query.get(id)


        dbcat.name = newCat['name']
        dbcat.age = newCat['age']
        dbcat.sex = newCat['sex']
        dbcat.breed = newCat['breed']
        dbcat.chonk_level = newCat['chonk_level']
        dbcat.image_url = newCat['image_url']

        db.session.commit()

        return [{"status": "succesfully updated, heres yo new cat"},dbcat.json()]

    def delete(self, id):
        cat = Cat.query.get(id)
        if cat:
            db.session.delete(cat)
            db.session.commit()
            return {"message": "Yo u got it deleted"}
        else:
            return {"error": "Can't find yo cat man"}, 404


class FelineList(Resource):
    def get(self):
        arr = []
        all_cat = Cat.query.all()
        return [cat.json() for cat in all_cat]

    def post(self):
        data = request.get_json()
        name= data['name']
        age = data['age']
        breed = data['breed']
        sex = data['sex']
        chonk_level = data['chonk_level']
        APIresponse = requests.get('https://api.thecatapi.com/v1/images/search').json()
        image_url = APIresponse[0]['url']
        newCat = Cat(name=name, age=age, breed=breed, sex=sex, chonk_level=chonk_level, image_url=image_url)
        db.session.add(newCat)
        db.session.commit()
        return [{"status_code": 200}, newCat.json()]


class Combine(Resource):
    def post(self):
        postData = request.get_json()
        status_code = validation(postData, 'Combine')
        if status_code == 200:
            test = postData.keys()
            cat1 = list(postData.keys())[0]
            cat2 = list(postData.keys())[-1]
            name1 = postData[cat1]
            name2 = postData[cat2]
            name3 = name1 + name2
            return name3
        else:
            return{'status code': status_code, 'message': 'yo only 2 vairables allowed'}


class ReverseCombine(Resource):
    def post(self):
        data = request.get_json()
        status_code = validation(data, 'ReverseCombine')
        if status_code == 200:
            test = data.keys()
            cat1 = list(data.keys())[0]
            cat2 = list(data.keys())[-1]
            name1 = data[cat1]
            name2 = data[cat2]
            name3 = name1+name2
            name3l = name3[::-1]
            return name3l
        else:
            return{'status code': status_code, 'message': 'yo only 2 vairables allowed'}


class Anagram(Resource):
    def post(self):
        data = request.get_json()
        status_code = validation(data, 'Anagram')
        if status_code == 200:
            word1 = list(data.values())[0]
            word2 = list(data.values())[-1]
            rw2 = word2[::-1]
            if word1 == rw2:
                return {'message': "das an anagram"}
            else:
                return {'message': "das not an anagram"}
        else:
            return{'status code': status_code, 'message': 'yo only 2 vairables allowed'}


api.add_resource(Combine, '/combine')
api.add_resource(ReverseCombine, '/rcombine')
api.add_resource(Anagram, '/anagram')


api.add_resource(FelineList, '/felinelist')
api.add_resource(Feline, '/feline/<id>')

if __name__ == '__main__':
    app.run(debug=True)
