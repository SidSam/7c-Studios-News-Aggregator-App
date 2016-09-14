from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class News(Base):
	__tablename__ = 'news'

	id = Column(Integer, primary_key = True)
	title = Column(String(20), nullable = False)
	description = Column(String(50), nullable = False)
	url = Column(String(40), nullable = False)
	imageurl = Column(String(50))
	
	@property
	def serialize(self):
		return {
		'id': self.id,
		'title': self.title,
		'description': self.description,
		'url': self.url,
		'imageurl': self.imageurl
		}

engine = create_engine('sqlite:///news.db')

Base.metadata.create_all(engine)


