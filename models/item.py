from db import db

class ItemModel(db.Model):
    
    __tablename__ = "items"

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision = 2)) #para için yani decimal olarak görünsün

    store_id = db.Column(db.Integer,db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')#join gibi kendi ilişkilendiriyor

    def __init__(self,name,price,store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
    def json(self):
        return {'name':self.name,'price':self.price}

    @classmethod
    def find_by_name(cls,name):
       return cls.query.filter_by(name = name).first()

    
    def save_to_db(self):
        db.session.add(self)#self nesnenin kendisini temsil ettiği için objeyi böyle ekliypruz
        #aynı zamanda bu bize birden çok ekleme ve güncelleme seçeneği sunuyor

        db.session.commit()

    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        