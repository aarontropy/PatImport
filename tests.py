from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

import csv
import os

FILEPATH = os.path.join( os.path.dirname(os.path.realpath(__file__)), 'testdata', 'csv')

from PatImport import schema

def ImportPatent():
	db = schema.engine()
	db.echo = True

	Session = sessionmaker(bind=db)
	session = Session()

	# PATENT
	f = open( os.path.join(FILEPATH, 'patents.csv'), 'r' ) 
	reader = csv.reader(f)
	headers = reader.next()
	p = schema.Patent()
	p.docNumber = '7201580'
	p.title = 'Inexpensive computer-aided learning methods and apparatus for learners'
	p.application_number = '10/692,274'
	f.close

	session.add(p)
	session.commit()

	session.delete(p)
	session.flush()


if __name__ == "__main__":
	# ImportPatent()
	print os.path.join(FILEPATH, 'test.sd')