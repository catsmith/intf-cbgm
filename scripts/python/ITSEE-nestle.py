import xml.etree.ElementTree as ET
import psycopg2

data_file = '../../data/gal_positive/basetext.xml'

tree = ET.parse(data_file)
root = tree.getroot()

connection = psycopg2.connect(user="ntg",
                              password="topsecret",
                              host="127.0.0.1",
                              port="5432",
                              database="gal_ph1")
cursor = connection.cursor()

delete_query = 'DELETE FROM nestle'
cursor.execute(delete_query)
connection.commit()

cursor.execute('ALTER SEQUENCE nestle_id_seq RESTART WITH 1')
connection.commit()

insert_query = 'INSERT INTO nestle (begadr, endadr, passage, lemma) VALUES (%s, %s, %s, %s)'

book = 9

index = 2
for word in root.findall('.//{http://www.tei-c.org/ns/1.0}div[@type="incipit"]//{http://www.tei-c.org/ns/1.0}w'):
    lemma = word.get('lemma').replace('’', '')
    begadr = 90000000 + index
    endadr = begadr
    passage = '[{},{})'.format(begadr, begadr + 1)
    try:
        cursor.execute(insert_query, (begadr, endadr, passage, lemma))
        connection.commit()
    except psycopg2.errors.UniqueViolation:
        connection.rollback()
        pass
    index += 2

for ab in root.findall('.//{http://www.tei-c.org/ns/1.0}div[@type="chapter"]/{http://www.tei-c.org/ns/1.0}ab'):
    index = 2
    name, chapter, verse = ab.get('n').split('.')
    for word in ab.findall('.//{http://www.tei-c.org/ns/1.0}w'):
        lemma = word.get('lemma').replace('’', '')
        begadr = 90000000 + (int(chapter) * 100000) + (int(verse) * 1000) + index
        endadr = begadr
        passage = '[{},{})'.format(begadr, begadr + 1)
        try:
            cursor.execute(insert_query, (begadr, endadr, passage, lemma))
            connection.commit()
        except psycopg2.errors.UniqueViolation:
            connection.rollback()
            pass
        index += 2

# this is how the explicit is done for Mark - I don't know if it is correct I am just copying.
lemma = '&om;'
begadr = 90000000 + ((int(chapter) + 1) * 100000) + 2
endadr = begadr
passage = '[{},{})'.format(begadr, begadr + 1)
try:
    cursor.execute(insert_query, (begadr, endadr, passage, lemma))
    connection.commit()
except psycopg2.errors.UniqueViolation:
    connection.rollback()
    pass
