from sqlalchemy import Column, Integer, String, Date, create_engine, Table
from sqlalchemy.schema import ForeignKey

from PatImport.schema import Base, Entity, Judge, Patent, ChoiceType

litigation_defendants = Table('litigation_defendants', Base.metadata,
	Column('litigation_id', Integer, ForeignKey('litigation.id')),
	Column('entity_id', Integer, ForeignKey(Entity.id))
)

litigation_plaintiffs = Table('litigation_plaintiffs', Base.metadata,
	Column('litigation_id', Integer, ForeignKey('litigation.id')),
	Column('entity_id', Integer, ForeignKey(Entity.id))
)

litigation_patentes = Table('litigation_patents', Base.metadata,
	Column('litigation_id', Integer, ForeignKey('litigation.id')),
	Column('patent_id', Integer, ForeignKey(Patent.id))
)

ROLE_CHOICES = (
	('defendant', 'Defendant'),
	('plaintiff', 'Plaintiff')
)

class Litigation(Base):
	__tablename__ = 'litigation'

	id = Column(Integer, primary_key=True)
	title 	= Column(String(150))
	caseno	= Column(String(20))
	court	= Column(String(10))
	filed	= Column(Date)
	judge 	= Column(Integer, ForeignKey(Judge.id), backref='cases')

	defendants = relationship('Entity', secondary=litigation_defendants, backref='defense_cases')
	plaintiffs = relationship('Entity', secondary=litigation_plaintiffs, backref='plaintiff_cases')

	patents = relationship('Patent', secondary=litigation_patents, backref='cases')


