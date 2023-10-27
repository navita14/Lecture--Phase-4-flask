from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()
bcrypt = Bcrypt()


#db.int,string,float

class Pet(db.Model, SerializerMixin): #inherting from db.Model. must have this as it is inherting from db. everything inherting from db needs an id
    __tablename__ = 'pets' #what to name our table

    serialize_rules = ('-owner.pets',) #this is what to ignore so it doesnt loop

    id = db.Column(db.Integer(), primary_key=True) #no duplicate keys and keys increment
    name = db.Column(db.String(), nullable=False) #means no null values if false. true means null values allowed
    owner_id = db.Column(db.Integer(),db.ForeignKey('owners.id'))#referencing table name

    #attribute name owner below
    owner = db.relationship('Owner', back_populates='pets')#argument is the class, and the attribute, linking to the owner attributes

    @validates('name') #field key you are changing, can validate multiple attributes not just name
    def validate_name(self, key, new_name):
        if len(new_name) == 0:
            raise ValueError('name must be at least one char')
        else:
            return new_name #this value gets set as the name


    def __repr__(self):
        return f'<Pet {self.name}>'
    

class Owner(db.Model, SerializerMixin):
    __tablename__ = 'owners'

    serialize_rules = ('-pets.owner',)


    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)

    #attribute name pets below
    pets = db.relationship('Pet',back_populates='owner', cascade = 'all, delete-orphan') #cascade = deletes foreign key for parent instead of NULL and the children of the owner

    def __repr__(self):
        return f'<Owner {self.name}>'
    




class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String, nullable = False)
    _password_hash = db.Column(db.String)

    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, new_pass):
        pass_hash = bcrypt.generate_password_hash(new_pass.encode('utf-8')) #encrypting passsword and scrambling password into byte string or ascii instead of utf-8
        self._password_hash = pass_hash.decode('utf-8') #storing to a string instead of a byte string

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8')) # check if a password matches something in our db