from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()

#db.int,string,float

class Pet(db.Model, SerializerMixin): #inherting from db.Model. must have this as it is inherting from db. everything inherting from db needs an id
    __tablename__ = 'pets' #what to name our table

    serialize_rules = ('-owner.pets',) #this is what to ignore so it doesnt loop

    id = db.Column(db.Integer(), primary_key=True) #no duplicate keys and keys increment
    name = db.Column(db.String(), nullable=False) #means no null values if false. true means null values allowed
    owner_id = db.Column(db.Integer(),db.ForeignKey('owners.id'))#referencing table name

    #attribute name owner below
    owner = db.relationship('Owner', back_populates='pets')#argument is the class, and the attribute, linking to the owner attributes

    def __repr__(self):
        return f'<Pet {self.name}>'
    

class Owner(db.Model, SerializerMixin):
    __tablename__ = 'owners'

    serialize_rules = ('-pets.owner',)


    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)

    #attribute name pets below
    pets = db.relationship('Pet',back_populates='owner')

    def __repr__(self):
        return f'<Owner {self.name}>'