from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

ENGINE = create_engine("sqlite:///drawpad.db", echo=True)
session = scoped_session(sessionmaker(bind=ENGINE, 
	autocommit=False, 
	autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

def create_db():
    '''Creates a new database when called'''
    Base.metadata.create_all(ENGINE)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    password = Column(String(64))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
    	return "User id = %d, username = %s, password = %s" % (
        	self.id, self.username, self.password)


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    img_name = Column(String(200), nullable=False)
    img_data = Column(String(200), nullable=False)

    user = relationship('User', backref=backref('images'))

    def __repr__(self):
        return "Image_id=%r User_id=%r Image_name=%s" % (
            self.id, self.user_id, self.img_name)


def get_user_by_username(username):
    """returns a user by username from database"""
    username = session.query(User).filter(User.username == username).first()
    return username

def save_user_to_db(username, password):
    new_user = User(username=username, password=password)
    session.add(new_user)
    return session.commit()

def save_image_to_db(user_id, img_name, img_data):
    new_image = Image(user_id=user_id, img_name=img_name, img_data=img_data)
    session.add(new_image)
    return session.commit()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
	main()