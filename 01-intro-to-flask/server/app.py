from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Pet, Owner

# 3. ✅ Initialize the App
app = Flask(__name__)  # initializa flask in a name. must be app. name space you are running code in. call this flask contructor we have app

    
    # Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' #how to connect to the database, how to find the file, where you want you db to live
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #not tracking modifications so db stays smaller. production should be true to track modifications
    
#Initializa database
db.init_app(app) #this attaches the sql db to flask, linking #importing db from models

 # 4. ✅ Migrate 
migrate = Migrate()
migrate.init_app(app , db) #migration framework linking to app so migration knows about flask app


# 6. ✅ Routes- define endpoints for web application. anything that comes after domain
@app.route('/') # will only accept get requests with toute
#when deploying convert react to one file and react roote route to react route
def root(): #name of function doesnt matter , view function
    print('hello world') # will print in the server log, client cannot see
    return make_response(jsonify({}), 200) # needs 2 things, data(json) to client and status code, data mainly json data back to the client, {} stands for json data
    #send a response object back


@app.route('/pets', methods = ['GET', 'POST'])
def get_all_pets():
    if request.method == 'GET':
        pets = Pet.query.all()
        body = [pet.to_dict() for pet in pets]
        return make_response(jsonify(body), 200)
    else: #POST
        pet_data = request.get_json() #gets json and turns it into a dictionary. pet data will be a dict

        #validate if name is 
        if 'name' not in pet_data:
            return {'message': "name is required"}, 403


        new_pet = Pet(name=pet_data.get('name'), owner_id=pet_data.get('owner.id'))
        db.session.add(new_pet)
        db.session.commit()

        return new_pet.to_dict(), 201

@app.route('/pets/<id>', methods = ['GET', 'DELETE', 'PATCH'])
def pets_by_id(id):

    #trying the code if not do something else or web sever will stop working. client will get an error
    # try:
    #     pet = Pet.query.filter(Pet.id ==id).first()
    # except:
    #     pass

    #IMPORT logging to send all response to a logged file, log all ithe import infor to a data file
    #stack tracer= when the error occured , and then tools to scrape logs to find certain errors like TRACEBACK 
    #or by date

    pet = Pet.query.filter(Pet.id ==id).first()

    if pet is None: #or if not pet is for empty object
            return {'message': 'pet not found'}, 404
    
    if request.method =='GET':#test in shell id =1 and then pet = Pet.query.filter(Pet.id ==id).one()  ->fido

        return make_response(jsonify(pet.to_dict()), 200)
        #can use custom serilaze rules by passing in 'rules' in to_dict
        #return make_response(jsonify(pet.to_dict(rules=('-owner',))), 200)
    elif request.method == 'DELETE':
        db.session.delete(pet)
        db.session.commit()
        return {}, 200
    elif request.method == 'POST':
        pet_data = request.get_json()

        # # option1 check if each field is in the request field
        # if 'name' is pet_data:
        #     pet_name = pet_data['name']
        # if 'owner_id' in pet_data['owner_id']


        #option2:
        for field in pet_data:
            setattr(pet, field, pet_data[field] )#what we are updating, the attribute we are updating 
        
        #add back to db
        db.session.add(pet)
        db.session.commit()

        return pet.to_dict(), 200

@app.route('/owners/<id>')
def owner_by_id(id):
    owner = Owner.query.filter(Owner.id ==id).one()
    #test in shell id =1 and then pet = Pet.query.filter(Pet.id ==id).one()  ->fido
    return make_response(jsonify(owner.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5000, debug=True) # need debug in development but not in production mocde




#is status code 500 then reroute it to another oops page