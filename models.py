from peewee import *

db = SqliteDatabase('db.sqlite')


class Company(Model):
    id = AutoField(primary_key= True)
    company_name = CharField(unique= True)
    password_hash = CharField()

    class Meta:
        database = db
        table_name = 'company'


class Product(Model):
    id = AutoField(primary_key= True)
    name = CharField(unique= True)
    price = IntegerField()
    category = CharField()
    company_id = ForeignKeyField(Company, backref="company")

    class Meta:
        database = db
        table_name = 'product'


def init_db():
    db.connect()
    db.create_tables([Product, Company])