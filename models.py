from peewee import *

db = SqliteDatabase('db.sqlite')


class Product(Model):
    id = AutoField(primary_key= True)
    name = CharField(unique= True)
    price = IntegerField()
    category = CharField()

    class Meta:
        database = db
        table_name = 'product'

def init_db():
    db.connect()
    db.create_tables([Product])
