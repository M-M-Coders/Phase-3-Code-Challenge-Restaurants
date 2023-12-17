from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import Base, Restaurant, Customer, Review  

def seed_data(session):
    # Create some restaurants
    restaurant1 = Restaurant(name="Kempinski", price=4000)
    restaurant2 = Restaurant(name="Food court", price=2000)

    # Create some customers
    customer1 = Customer(first_name="Ecee", last_name="Chain")
    customer2 = Customer(first_name="Sam", last_name="Mwangi")

    # Create some reviews
    review1 = Review(star_rating=5, restaurant=restaurant1, customer=customer1)
    review2 = Review(star_rating=4, restaurant=restaurant2, customer=customer2)

    # Add instances to the session
    session.add_all([restaurant1, restaurant2, customer1, customer2, review1, review2])

    # Commit the changes to the database
    session.commit()

def query_data(session):
    # Query all restaurants
    all_restaurants = session.query(Restaurant).all()
    print("All Restaurants:")
    for restaurant in all_restaurants:
        print(f"{restaurant.name}, Price: {restaurant.price}")

    # Query all customers
    all_customers = session.query(Customer).all()
    print("\nAll Customers:")
    for customer in all_customers:
        print(f"{customer.customer_full_name()}")

    # Query all reviews
    all_reviews = session.query(Review).all()
    print("\nAll Reviews:")
    for review in all_reviews:
        print(review.full_review())

if __name__ == "__main__":
    # Create an SQLite in-memory database for testing
    engine = create_engine('sqlite:///migrations_test.db')
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)

    # Use a context manager for the session
    with Session() as session:
        # Call the seed_data function to populate the database
        seed_data(session)

        # Call the query_data function to retrieve and print data
        query_data(session)
