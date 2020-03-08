from db import db

class StoreModel(db.Model):
    
    __tablename__ = "stores"

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')
    #many-to-one relationship

    def __init__(self,name):
        self.name = name

    def json(self):
        return {'name':self.name,'items':[item.json() for item in self.items.all()]}
   
    #layz dynamic diyerek nesne oluştururken item tablosuna bakılıp itemlerin doldurulması yada oluşturulması işlemi 
    #çok store oldugunda bizi yorabilir ondan dolayı return ederken .all() diyerek item tablosundaki 
    #eşleşen itemleri alıp atayıp o an işlemi görüyoruz diye anladım.
   
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
        