from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, User, BikeSpecs
 
engine = create_engine('sqlite:///motorbikes.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#Bike1
bike1 = BikeSpecs(bike_name = "Kawasaki Ninja 300", description = "With 296cc of fuel-injected, adrenaline-rush-inducing performance and effortless handling characteristics, the Ninja 300 torches the competition across the", price = "$50",bike_class = "Sport")

session.add(bike1)
session.commit()


bike2 = BikeSpecs(bike_name = "Honda CBR500", description = "If you're looking for a streetbike that is the perfect combination of size, performance, versatility and price, Honda's CBR500R is exactly where you want to be.", price = "$50", bike_class = "Sport")

session.add(bike2)
session.commit()


bike3 = BikeSpecs(bike_name = "Honda CBR 125R", description = "It is hard to imagine, but back in 2004 the Honda CBR125R was an absolute sensation. While the likes of the Aprilia RS125 were screaming around the UK's ..", price = "$50",bike_class = "Sport")

session.add(bike3)
session.commit()

print "added all bikes!"
