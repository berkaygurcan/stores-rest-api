from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    #parser tanımlayıp istenmeyen argümanlar yollandıgında update edilmesini engelleyeceğiz
    parser = reqparse.RequestParser()#nesne oluşturduk
    parser.add_argument('price',
    type= float,
    required=True,
    help = "This field cannot be left blank!"
    )
    parser.add_argument('store_id',
    type= int,
    required=True,
    help = "Every item needs a store id."
    )



    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()#artık item nesne oldugu için obje metodu olan json kullanarak jsona cevirdik
        return {'message':'Item not found'},404

    


    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message':"An item with name '{}' already exists.".format(name)} , 400
            
        data = Item.parser.parse_args()#request.get_json() force = True you do not need content-tpye header.
        item = ItemModel(name,data['price'],data['store_id'])#data['price'],data['store_id'] = **data
        
        try:
             item.save_to_db()
        except:
            return {"message":"An error occured inserting the item."},500#internal server error

        return item.json(), 201

    
    
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':'Item deleted'}
    
    def put(self,name):
        
        data = Item.parser.parse_args()#gelen json paylodunu parselar sadece price adlı json alanı geçer diğerleri geçirilmeyip orada silinir ve biz ilerleyen safhada göremeyiz
        
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name,**data)#data['price'],data['store_id'] = **data

        else:
            item.price = data['price']
        
        item.save_to_db()

        return item.json()

    

    

class ItemList(Resource):
    def get(self):
        return {'items':[x.json() for x in ItemModel.query.all()]}
        


