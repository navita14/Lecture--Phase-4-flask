from app import app
from models import db, Pet, Owner

with app.app_context():
    #delete everything from all tables
    Pet.query.delete()
    Owner.query.delete()


    o1= Owner(name='joe')
    o2 = Owner(name='anne')

    db.session.add_all([o1,o2])


    # p1 = Pet(name='fido', owner_id=o1.id)
    # p2 = Pet(name='rex', owner_id=o1.id)
    # p3 = Pet(name='fluffy', owner_id=o2.id)

    p1 = Pet(name='fido', owner=o1)
    p2 = Pet(name='rex', owner=o1)
    p3 = Pet(name='fluffy', owner=o2)

    db.session.add_all([p1,p2,p3])

    db.session.commit()