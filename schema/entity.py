from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import ForeignKey

from PatImport.schema import Base

class Entity(Base):
	__tablename__ = 'entities'

	id 		= Column(Integer, primary_key=True)
	type 	= Column(String(50))
	name 	= Column(String(150))

	__mapper_args__ = {
		'polymorphic_identity': 'entity',
		'polymorphic_on': type
	}

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<Entity (%(name)s)>" % { 'name': self.name, }

#===============================================================================
# PEOPLE
class Person(Entity):
	__tablename__ = 'persons'
	__mapper_args__ = {	'polymorphic_identity': 'person' }

	id = Column(Integer, ForeignKey(Entity.id), primary_key=True)
	first_name = Column(String(50))
	middle_name = Column(String(50))
	last_name = Column(String(50))

	def __init__(self, full_name):
		super(self.__class__, self).__init__(full_name)


class Inventor(Person):
	__tablename__ = 'inventors'
	__mapper_args__ = { 'polymorphic_identity': 'inventor'}

	id 	= Column(Integer, ForeignKey(Person.id), primary_key=True)
	
	def __init__(self, full_name):
		super(self.__class__, self).__init__(full_name)


class Judge(Person):
	__tablename__ = 'judges'
	__mapper_args__ = { 'polymorphic_identity': 'judge'}

	id = Column(Integer, ForeignKey(Person.id), primary_key=True)
	cases = relationship("Litigation", backref="judge")

class Company(Entity):
	__tablename__ = 'companies'
	__mapper_args__ =  {'polymorphic_identity': 'corporate'}

	id = Column(Integer, ForeignKey(Entity.id), primary_key=True)
	incorp_type = Column(String(10))

	def __init__(self, name):
		super(self.__class__, self).__init__(name)

class Lawfirm(Company):
	__tablename__ = 'lawfirms'
	__mapper_args__ =  {'polymorphic_identity': 'lawfirm'}

	id = Column(Integer, ForeignKey(Company.id), primary_key=True)

	def __init__(self, name):
		super(self.__class__, self).__init__(name)
