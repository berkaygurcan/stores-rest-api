import os
from flask import Flask 
from flask_restful import  Api 
from flask_jwt import JWT 

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')#heroku env içinde database url değişkeninde database url mevcut
#bağlandıgımız zaman os ile database url sorup alacağız ama local de kodu calıstırıp kaldırmak istersek(test,geliştirme için) database url bulunmadıgı içi
#default olarak ikinci parametre gelecektir.yani localde calısabiliriz sql lite ile 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False #flaskın özelligin kapatıp sql alc'nin kendi içindekine izin verdik sanırsam
app.secret_key = "jose"
api = Api(app)

#@app.before_first_request run.py oluşturuldu heroku içi burası hata alıyordu
#def create_tables():
 #   db.create_all()

jwt = JWT(app,authenticate,identity)#/auth

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister,'/register')



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port = 5000 , debug = True)
