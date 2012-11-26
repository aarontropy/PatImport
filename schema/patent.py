from sqlalchemy import Column, Integer, String, Boolean, Date, create_engine, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import ForeignKey

from PatImport.schema import Base
from PatImport.schema.entity import Inventor

DATABASE = 'Patent_Test'
USERNAME = 'sqlalchemy'
PASSWORD = 'sqlalchemy'




# Session = sessionmaker(bind=engine)
patent_inventor = Table('patent_inventor', Base.metadata,
	Column('patent_id', Integer, ForeignKey('patents.id')),
	Column('inventor_id', Integer, ForeignKey('inventors.id'))
)



class Patent(Base):
	__tablename__ = 'patents'

	id 					= Column(Integer, primary_key=True)
	docNumber			= Column(String(15))
	title 				= Column(String(500))
	application_number 	= Column(String(15))

	inventors = relationship('Inventor', secondary=patent_inventor, backref='patents')

	def __init__(self, number):
		self.number = number

	def __repr__(self):
		return "<Patent ('%s')>" % (self.number,)



#===============================================================================
# CLASSIFICATION SECTION
class BaseClassification(Base):
	__tablename__ = 'classifications'


	id 			= Column(Integer, primary_key=True)
	patent_id 	= Column(Integer, ForeignKey(Patent.id))
	text 		= Column(String(30))
	type 		= Column(String(15))

	__mapper_args__ = { 
		'polymorphic_identity': 'generic', 
		'polymorphic_on': type 
	}

	def __init__(self, text, patent):
		self.patent_id = patent 
		self.text = text

	def __repr__(self):
		return "<Classification (%s)>" % ( self.type, )


class InternationalClass(BaseClassification):
	__tablename__ = 'international_classes'
	__mapper_args__ = { 'polymorphic_identity': 'international' }

	id = Column(Integer, ForeignKey(BaseClassification.id), primary_key=True)

	def __init__(self, text, patent):
		super(self.__class__, self).__init__(text, patent)
	
class USClass(BaseClassification):
	__tablename__ = 'us_classes'
	__mapper_args__ = { 'polymorphic_identity': 'us' }

	id = Column(Integer, ForeignKey(BaseClassification.id), primary_key=True)
	main = Column(Boolean)

	def __init__(self, text, patent, main=False):
		self.main = main
		super(self.__class__, self).__init__(text, patent)

class FieldOfResearch(USClass):
	__tablename__ = 'us_fieldsofresearch'
	__mapper_args__ = { 'polymorphic_identity': 'us-for', }

	id = Column(Integer, ForeignKey(USClass.id), primary_key=True)

	def __init__(self, text, patent):
		super(self.__class__, self).__init__(text, patent, False)

#===============================================================================
# REFERENCE SECTION
class BaseReference(Base):
	__tablename__ = 'references'

	id 			= Column(Integer, primary_key=True)
	patent_id	= Column(Integer, ForeignKey(Patent.id))
	text 		= Column(String(255))
	type 		= Column(String(15))

	__mapper_args__ = { 
		'polymorphic_identity': 'generic', 
		'polymorphic_on': type 
	}

	def __init__(self, text, patent):
		self.patent_id = patent 
		self.text = text

	def __repr__(self):
		return "<Reference (%s)>" % ( self.type, )

class PublicationReference(BaseReference):
	__tablename__ = 'pub_references'
	__mapper_args__ = { 'polymorphic_identity': 'publication'}

	id = Column(Integer, ForeignKey(BaseReference.id), primary_key=True)
	docNumber 	= Column(String(20))
	country		= Column(String(10))
	kind		= Column(String(10))
	name		= Column(String(20))
	date 		= Column(Date)

	def __init__(self, text, patent):
		super(self.__class__, self).__init__(text, patent)

class ApplicationReference(BaseReference):
	__tablename__ = 'app_references'
	__mapper_args__ = { 'polymorphic_identity': 'application'}

	id = Column(Integer, ForeignKey(BaseReference.id), primary_key=True)
	docNumber 	= Column(String(20))
	country		= Column(String(10))
	date 		= Column(Date)

	def __init__(self, text, patent):
		super(self.__class__, self).__init__(text, patent)

class NonPatReference(BaseReference):
	__tablename__ = 'non_patent'
	__mapper_args__ = { 'polymorphic_identity': 'application'}

	id = Column(Integer, ForeignKey(BaseReference.id), primary_key=True)

	def __init__(self, text, patent):
		super(self.__class__, self).__init__(text, patent)




def create_schema():
	engine = create_engine('mysql://%(username)s:%(password)s@localhost/%(database)s' % {
		'username': USERNAME,
		'password': PASSWORD,
		'database': DATABASE
		} )
	Base.metadata.create_all(engine)

