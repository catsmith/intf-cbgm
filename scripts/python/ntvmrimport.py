import requests
import xml.etree.ElementTree as ET
import psycopg2
from psycopg2 import Error

bookName = 'Mat'
bookNum = 1
chapterNum = 1
verseNum = 2


class Segment:

    def __init__(self, bookNumIn, chapNumStartIn, verseNumStartIn, wordStartIn):
        self.readings = {}
        self.bookNum = bookNumIn
        self.chapNumStart = chapNumStartIn
        self.chapNumEnd = chapNumStartIn
        self.verseNumStart = verseNumStartIn
        self.verseNumEnd = verseNumStartIn
        self.wordStart = wordStartIn
        self.wordEnd = wordStartIn

    # e.g., 50122034 = Acts.1.22 word 34
    def get_start_address(self):
        return (self.bookNum * 10000000) + (self.chapNumStart * 100000) + (self.verseNumStart * 1000) + self.wordStart

    # e.g., 50122038 = Acts.1.22 word 28
    def get_end_address(self):
        return (self.bookNum * 10000000) + (self.chapNumEnd * 100000) + (self.verseNumEnd * 1000) + self.wordEnd

    # e.g., "[50122034, 50122039)"
    def get_address_range(self):
        return "[%d, %d)" % (self.get_start_address(), self.get_end_address() + 1)

    def add_reading(self, label, text):
        r = Reading(label, text)
        self.readings[label] = r
        return r


class Reading:

    def __init__(self, label, text):
        self.witnesses = []
        self.label = label
        self.text = text
        # clear out text if label is 'zz'
        # we usually have <lac> in the text here
        if label == 'zz':
            self.text = None

    def add_witness(self, doc_id):
        w = ReadingWitness(doc_id)
        self.witnesses.append(w)
        return w


class ReadingWitness:

    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.label_suffix = ''
        self.mss_text = None


postData = {'segmentGroupID': 1, 'indexContent': '%s.%d.%d' % (bookName, chapterNum, verseNum), 'detail': 'extra'}
req = requests.post('https://ntvmr.uni-muenster.de/community/vmr/api/variant/apparatus/get/', params=postData)
xml = ET.XML(req.text)

mss = {0: 'A', 1: 'MT'}
segs = []

for segment in xml.iter('segment'):
    print(segment.tag, segment.attrib)

    # TODO: handle cross-boundary segments
    words = segment.find('contextDescription').text.split('-')
    seg = Segment(bookNum, chapterNum, verseNum, int(words[0]))
    if len(words) > 1:
        seg.wordEnd = int(words[1])

    for segmentReading in segment.iter('segmentReading'):
        rd = seg.add_reading(segmentReading.attrib['label'], segmentReading.attrib['reading'])
        for witness in segmentReading.iter('witness'):
            docID = int(witness.attrib['docID']) * 10
            primaryName = witness.attrib['primaryName']
            siglumSuffix = witness.attrib['siglumSuffix']
            if siglumSuffix.find('S') != -1:
                docID += 1
                primaryName += 's'
            mss[docID] = primaryName
            w = rd.add_witness(docID)
            siglumSuffix.replace('S', '')
            if siglumSuffix:
                w.label_suffix = siglumSuffix
            tr = witness.find('transcription')
            if tr:
                w.mss_text = tr.text

    segs.append(seg)

connection = psycopg2.connect(user="ntg",
                              password="topsecret",
                              host="127.0.0.1",
                              port="5432",
                              database="acts_ph4")

# cursor.execute("DELETE FROM manuscripts")
# connection.commit()

mss_insert_query = " INSERT INTO manuscripts (hsnr, hs) VALUES (%s, %s)"

for docID in mss.keys():
    data = (docID, mss[docID])
    try:
        cursor = connection.cursor()
        cursor.execute(mss_insert_query, data)
        connection.commit()
    except psycopg2.errors.UniqueViolation:
        connection.rollback()
        pass

seg_insert_query = "INSERT INTO passages (bk_id, begadr, endadr, passage)" \
                   "values (%s, %s, %s, %s)"

for seg in segs:
    data = (seg.bookNum, seg.get_start_address(), seg.get_end_address(), seg.get_address_range())
    try:
        cursor = connection.cursor()
        cursor.execute(seg_insert_query, data)
        connection.commit()
    except psycopg2.errors.UniqueViolation:
        connection.rollback()
        pass

clear_segment_locstem = "DELETE FROM locstem" \
                        " WHERE pass_id=(select pass_id from passages where passage = %s)"
clear_segment_cliques = "DELETE FROM cliques" \
                        " WHERE pass_id=(select pass_id from passages where passage = %s)"
reading_insert_query = "INSERT INTO readings (pass_id, labez, lesart)" \
                       " values ((select pass_id from passages where passage = %s), %s, %s)"
clique_default_insert = "SET ntg.user_id = 0; INSERT INTO cliques(pass_id, labez)" \
                         " values ((select pass_id from passages where passage = %s), %s)"
locstem_default_insert = "SET ntg.user_id = 0; INSERT INTO locstem(pass_id, labez, source_labez)" \
                               " values ((select pass_id from passages where passage = %s), %s, %s)"
reading_update_query = "UPDATE readings set lesart=%s" \
                       " where pass_id=(select pass_id from passages where passage = %s) and labez=%s"
for seg in segs:

    # for now, clear out all the locstem and clique data if it exists when we import a segment
    try:
        cursor = connection.cursor()
        data = (seg.get_address_range(),)
        cursor.execute(clear_segment_locstem, data)
        cursor.execute(clear_segment_cliques, data)
        connection.commit()
    except:
        connection.rollback()
        pass
    for reading_label in seg.readings.keys():
        reading = seg.readings[reading_label]
        data = (seg.get_address_range(), reading.label, reading.text)
        try:
            cursor = connection.cursor()
            print(reading_insert_query, data)
            cursor.execute(reading_insert_query, data)
            connection.commit()
        except psycopg2.errors.UniqueViolation:
            connection.rollback()
            data = (reading.text, seg.get_address_range(), reading.label)
            try:
                cursor = connection.cursor()
                cursor.execute(reading_update_query, data)
                connection.commit()
            except psycopg2.errors.UniqueViolation:
                connection.rollback()
                pass

# Add the default clique
        try:
            cursor = connection.cursor()
            data = (seg.get_address_range(), reading.label)
            print(clique_default_insert, data)
            cursor.execute(clique_default_insert, data)
            connection.commit()
        except psycopg2.errors.UniqueViolation:
            connection.rollback()

# Add the default locstem
        try:
            cursor = connection.cursor()
            if reading.label == 'a':
                data = (seg.get_address_range(), reading.label, '*')
            else:
                data = (seg.get_address_range(), reading.label, '?')
            print(locstem_default_insert, data)
            cursor.execute(locstem_default_insert, data)
            connection.commit()
        except psycopg2.errors.UniqueViolation:
            connection.rollback()

clear_segment_witnesses = "DELETE FROM apparatus" \
                          " WHERE pass_id=(select pass_id from passages where passage = %s)"

witness_insert_query = "INSERT INTO apparatus (ms_id, pass_id, labez, cbgm, labezsuf, lesart, origin)" \
                       " values ((select ms_id from manuscripts where hsnr = %s)," \
                       " (select pass_id from passages where passage = %s), %s, true, %s, %s, 'DEF')"
for seg in segs:
    # let's start by clearing out all witnesses for this segment
    print(seg.get_address_range())
    try:
        cursor = connection.cursor()
        data = (seg.get_address_range(),)
        cursor.execute(clear_segment_witnesses, data)
        connection.commit()
    except:
        connection.rollback()
        pass

    for reading_label in seg.readings.keys():
        print(reading_label)
        reading = seg.readings[reading_label]
        w_count = 0
        for witness in reading.witnesses:
            data = (witness.doc_id, seg.get_address_range(), reading.label, witness.label_suffix, witness.mss_text)
            try:
                cursor = connection.cursor()
                cursor.execute(witness_insert_query, data)
                connection.commit()
                w_count += 1
            except psycopg2.errors.UniqueViolation:
                connection.rollback()
                pass
        print('added %d witnesses' % w_count)
