from requests import session
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create an SQLite database engine
engine = create_engine('sqlite:///migrations_test.db')

# Create a session class bound to the engine
Session = sessionmaker(bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Define the Restaurant class
class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Integer())

    # Relationship with the Review class
    reviews = relationship('Review', back_populates='restaurant')

    # Returns a collection of all reviews for the restaurant
    def restaurant_reviews(self):
        return self.reviews

    # Returns a collection of customers who reviewed the restaurant
    def restaurant_customers(self):
        return [review.customer for review in self.reviews]

    # Returns the fanciest restaurant using a class method
    @classmethod
    def restaurant_fanciest(cls, session):
        return session.query(cls).order_by(cls.price.desc()).first()

# Define the Customer class
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    # Relationship with the Review class
    reviews = relationship('Review', back_populates='customer')

    # Returns reviews left by the customer
    def customer_reviews(self):
        return [review for review in self.reviews]

    # Returns restaurants reviewed by the customer
    def customer_restaurants(self):
        return [review.restaurant for review in self.reviews]

    # Returns the full name of the customer
    def customer_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Returns the customer's favorite restaurant based on star rating
    def customer_favourite_restaurant(self):
        return session.query(Restaurant).join(Review).filter(Review.customer_id == self.id).order_by(desc(Review.star_rating)).first()

    # Adds a new review for the customer
    def customer_add_review(self, session, restaurant, rating):
        latest_review = Review(customer=self, restaurant=restaurant, star_rating=rating)
        session.add(latest_review)
        session.commit()

    # Deletes all reviews for a specific restaurant by the customer
    def customer_delete_reviews(self, restaurant):
        session.query(Review).filter(Review.customer_id == self.id, Review.restaurant_id == restaurant.id).delete()
        session.commit()

# Define the Review class
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    star_rating = Column(Integer())

    # Foreign keys to link reviews with restaurants and customers
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    # Relationships with the Restaurant and Customer classes
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')

    # Returns the customer instance for this review
    def review_customer(self):
        return self.customer

    # Returns the restaurant instance for this review
    def review_restaurant(self):
        return self.restaurant

    # Returns a formatted string for the full review
    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.first_name} {self.customer.last_name}: {str(self.star_rating)} stars."
