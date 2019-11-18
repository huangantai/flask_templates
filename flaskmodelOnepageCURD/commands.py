from app import db,manager
from faker import Faker
from models import Message

@manager.command
def hell():
    print("hello")

@manager.option('-c','--count',dest='count',default=20,help='Quantity of messages,default is 20.')
def forge(count):
    db.drop_all()
    db.create_all()

    faker=Faker()
    print('Working...')

    for i in range(int(count)):
        message=Message(name=faker.name(),body=faker.sentence(),
                        timestamp=faker.date_time_this_year())
        db.session.add(message)
    db.session.commit()
    print('Create %d fake messages' % int(count))
