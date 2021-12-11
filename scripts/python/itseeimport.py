import os
import sys
import psycopg2
import xml.etree.ElementTree as ET

data_dir = '../../data/gal_positive'

connection = psycopg2.connect(user="ntg",
                              password="topsecret",
                              host="127.0.0.1",
                              port="5432",
                              database="gal_ph1")
cursor = connection.cursor()

cursor.execute('DELETE FROM passages')
connection.commit()

# manuscripts table once with all MSS
#1, 0, A and 2, 1, MT in first and second place

mss_insert_query = " INSERT INTO manuscripts (hsnr, hs) VALUES (%s, %s)"
cursor.execute('DELETE FROM manuscripts')
connection.commit()

cursor.execute('ALTER SEQUENCE manuscripts_ms_id_seq RESTART WITH 1')
connection.commit()

cursor.execute('DELETE FROM passages')
connection.commit()

cursor.execute('ALTER SEQUENCE passages_pass_id_seq RESTART WITH 1')
connection.commit()

cursor.execute(mss_insert_query, (0, 'A'))
cursor.execute(mss_insert_query, (1, 'MT'))
connection.commit()

def get_passage_data(ref, start, end):
    try:
        book, chapter, verse = ref.split('.')
    except ValueError:
        return None
    begadr = 90000000 + (int(chapter) * 100000) + (int(verse) * 1000) + start
    endadr = 90000000 + (int(chapter) * 100000) + (int(verse) * 1000) + end
    passage = '[{},{})'.format(begadr, endadr)
    return (9, begadr, endadr, passage, True, False, False, False)

def is_variant(app):
    labels = []
    for rdg in app.findall('.//{http://www.tei-c.org/ns/1.0}rdg'):
        if rdg.get('type') != 'subreading':
            labels.append(rdg.get('n'))
    real_readings = [x for x in labels if x not in ['zz', 'zu']]
    if len(real_readings) >= 2:
        return True
    return False

for file in [f for f in os.listdir(data_dir)
             if f[-4:] == '.xml' and f != 'basetext.xml']:

    tree = ET.parse(os.path.join(data_dir, file))
    root = tree.getroot()

    for app in root.findall('.//{http://www.tei-c.org/ns/1.0}app'):
        if is_variant(app):
            ref = app.get('n')
            start = int(app.get('from'))
            end = int(app.get('to'))
            # passages (once per app)
            passage_data = get_passage_data(ref, start, end)
            if passage_data is not None:
                # try:
                print(passage_data)
                cursor.execute("""INSERT INTO passages (bk_id, begadr, endadr,
                               passage, variant, spanning, spanned, fehlvers)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                               passage_data)
                connection.commit()

                # except psycopg2.errors.UniqueViolation:
                #     connection.rollback()
                #     print('failed')
                #     pass


            # readings (once per main reading) (fehlverse is I think for when there is no a text)

            # apparatus (once per witness)







# class Segment:
#
#     def __init__(self, book_num_in, chap_num_start_in, verse_num_start_in, word_start_in):
#         self.readings = {}
#         self.book_num = book_num_in
#         self.chapNumStart = chap_num_start_in
#         self.chapNumEnd = chap_num_start_in
#         self.verseNumStart = verse_num_start_in
#         self.verseNumEnd = verse_num_start_in
#         self.wordStart = word_start_in
#         self.wordEnd = word_start_in
#
#     # e.g., 50122034 = Acts.1.22 word 34
#     def get_start_address(self):
#         return (self.book_num * 10000000) + (self.chapNumStart * 100000) + (self.verseNumStart * 1000) + self.wordStart
#
#     # e.g., 50122038 = Acts.1.22 word 28
#     def get_end_address(self):
#         return (self.book_num * 10000000) + (self.chapNumEnd * 100000) + (self.verseNumEnd * 1000) + self.wordEnd
#
#     # e.g., "[50122034, 50122039)"
#     def get_address_range(self):
#         return "[%d, %d)" % (self.get_start_address(), self.get_end_address() + 1)
#
#     def add_reading(self, label, text):
#         r = Reading(label, text)
#         self.readings[label] = r
#         return r
#
#
# class Reading:
#
#     def __init__(self, label, text):
#         self.witnesses = []
#         self.label = label
#         self.text = text
#         # clear out text if label is 'zz'
#         # we usually have <lac> in the text here
#         if label == 'zz':
#             self.text = None
#
#     def add_witness(self, doc_id):
#         w = ReadingWitness(doc_id)
#         self.witnesses.append(w)
#         return w
#
#
# class ReadingWitness:
#
#     def __init__(self, doc_id):
#         self.doc_id = doc_id
#         self.label_suffix = ''
#         self.mss_text = None
#
#
# def main():
#     post_data = {
#         'segmentGroupID': 1,
#         'indexContent': '%s.%d.%d' % (book_name, chapter_num, verse_num),
#         'detail': 'extra'
#     }
#     req = requests.post('https://ntvmr.uni-muenster.de/community/vmr/api/variant/apparatus/get/', params=post_data)
#     xml = ET.XML(req.text)
#
#     mss = {0: 'A', 1: 'MT'}
#     segs = []
#
#     for segment in xml.iter('segment'):
#         print(segment.tag, segment.attrib)
#         add = False
#         # TODO: handle cross-boundary segments
#         words = segment.find('contextDescription').text.split('-')
#         seg = Segment(book_num, chapter_num, verse_num, int(words[0]))
#         if len(words) > 1:
#             seg.wordEnd = int(words[1])
#
#         for segmentReading in segment.iter('segmentReading'):
#             # if there is only a and zz it does not make it into the cbgm
#             if segmentReading.attrib['label'] not in ['a', 'zz']:
#                 add = True
#             rd = seg.add_reading(segmentReading.attrib['label'], segmentReading.attrib['reading'])
#             for witness in segmentReading.iter('witness'):
#                 doc_id = int(witness.attrib['docID']) * 10
#                 primary_name = witness.attrib['primaryName']
#                 siglum_suffix = witness.attrib['siglumSuffix']
#                 if siglum_suffix.find('S') != -1:
#                     doc_id += 1
#                     primary_name += 's'
#                 mss[doc_id] = primary_name
#                 w = rd.add_witness(doc_id)
#                 siglum_suffix.replace('S', '')
#                 if siglum_suffix:
#                     w.label_suffix = siglum_suffix
#                 tr = witness.find('transcription')
#                 if tr:
#                     w.mss_text = tr.text
#         if add is True:
#             segs.append(seg)
#         else:
#             print('ignoring this')
#
#     connection = psycopg2.connect(user="ntg",
#                                   password="topsecret",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database="gal_ph1")
#
#     # cursor.execute("DELETE FROM manuscripts")
#     # connection.commit()
#
#     mss_insert_query = " INSERT INTO manuscripts (hsnr, hs) VALUES (%s, %s)"
#
#     for doc_id in mss.keys():
#         data = (doc_id, mss[doc_id])
#         try:
#             cursor = connection.cursor()
#             cursor.execute(mss_insert_query, data)
#             connection.commit()
#         except psycopg2.errors.UniqueViolation:
#             connection.rollback()
#             pass
#
#     clear_segs = "DELETE FROM passages WHERE bk_id=%s and begadr=%s and endadr=%s"
#     clear_readings = "DELETE FROM readings WHERE pass_id IN (SELECT pass_id from passages WHERE bk_id=%s and begadr=%s and endadr=%s)"
#     clear_apparatus = "DELETE FROM apparatus WHERE pass_id IN (SELECT pass_id from passages WHERE bk_id=%s and begadr=%s and endadr=%s)"
#     clear_cliques = "SET ntg.user_id = 0; DELETE FROM cliques WHERE pass_id IN (SELECT pass_id from passages WHERE bk_id=%s and begadr=%s and endadr=%s)"
#     clear_locstem = "SET ntg.user_id = 0; DELETE FROM locstem WHERE pass_id IN (SELECT pass_id from passages WHERE bk_id=%s and begadr=%s and endadr=%s)"
#     seg_insert_query = "INSERT INTO passages (bk_id, begadr, endadr, passage)" \
#                        "values (%s, %s, %s, %s)"
#
#     for seg in segs:
#         delete_data = (seg.book_num, seg.get_start_address(), seg.get_end_address())
#         data = (seg.book_num, seg.get_start_address(), seg.get_end_address(), seg.get_address_range())
#         try:
#             cursor = connection.cursor()
#             cursor.execute(clear_locstem, delete_data)
#             cursor.execute(clear_cliques, delete_data)
#             cursor.execute(clear_apparatus, delete_data)
#             cursor.execute(clear_readings, delete_data)
#             cursor.execute(clear_segs, delete_data)
#             cursor.execute(seg_insert_query, data)
#             connection.commit()
#         except psycopg2.errors.UniqueViolation:
#             connection.rollback()
#             pass
#
#     clear_segment_locstem = "DELETE FROM locstem" \
#                             " WHERE pass_id=(select pass_id from passages where passage = %s)"
#     clear_segment_cliques = "DELETE FROM cliques" \
#                             " WHERE pass_id=(select pass_id from passages where passage = %s)"
#     reading_insert_query = "INSERT INTO readings (pass_id, labez, lesart)" \
#                            " values ((select pass_id from passages where passage = %s), %s, %s)"
#     clique_default_insert = "SET ntg.user_id = 0; INSERT INTO cliques(pass_id, labez)" \
#                             " values ((select pass_id from passages where passage = %s), %s)"
#     locstem_default_insert = "SET ntg.user_id = 0; INSERT INTO locstem(pass_id, labez, source_labez)" \
#                              " values ((select pass_id from passages where passage = %s), %s, %s)"
#     reading_update_query = "UPDATE readings set lesart=%s" \
#                            " where pass_id=(select pass_id from passages where passage = %s) and labez=%s"
#     for seg in segs:
#
#         # for now, clear out all the locstem and clique data if it exists when we import a segment
#         try:
#             cursor = connection.cursor()
#             data = (seg.get_address_range(),)
#             cursor.execute(clear_segment_locstem, data)
#             cursor.execute(clear_segment_cliques, data)
#             connection.commit()
#         except:
#             connection.rollback()
#             pass
#         for reading_label in seg.readings.keys():
#             reading = seg.readings[reading_label]
#             data = (seg.get_address_range(), reading.label, reading.text)
#             try:
#                 cursor = connection.cursor()
#                 print(reading_insert_query, data)
#                 cursor.execute(reading_insert_query, data)
#                 connection.commit()
#             except psycopg2.errors.UniqueViolation:
#                 connection.rollback()
#                 data = (reading.text, seg.get_address_range(), reading.label)
#                 try:
#                     cursor = connection.cursor()
#                     cursor.execute(reading_update_query, data)
#                     connection.commit()
#                 except psycopg2.errors.UniqueViolation:
#                     connection.rollback()
#                     pass
#
#             # Add the default clique
#             try:
#                 cursor = connection.cursor()
#                 data = (seg.get_address_range(), reading.label)
#                 print(clique_default_insert, data)
#                 cursor.execute(clique_default_insert, data)
#                 connection.commit()
#             except psycopg2.errors.UniqueViolation:
#                 connection.rollback()
#
#             # Add the default locstem
#             try:
#                 cursor = connection.cursor()
#                 if reading.label == 'a':
#                     data = (seg.get_address_range(), reading.label, '*')
#                 else:
#                     data = (seg.get_address_range(), reading.label, '?')
#                 print(locstem_default_insert, data)
#                 cursor.execute(locstem_default_insert, data)
#                 connection.commit()
#             except psycopg2.errors.UniqueViolation:
#                 connection.rollback()
#
#     clear_segment_witnesses = "DELETE FROM apparatus" \
#                               " WHERE pass_id=(select pass_id from passages where passage = %s)"
#
#     witness_insert_query = "INSERT INTO apparatus (ms_id, pass_id, labez, cbgm, labezsuf, lesart, origin)" \
#                            " values ((select ms_id from manuscripts where hsnr = %s)," \
#                            " (select pass_id from passages where passage = %s), %s, true, %s, %s, 'DEF')"
#     for seg in segs:
#         # let's start by clearing out all witnesses for this segment
#         print(seg.get_address_range())
#         try:
#             cursor = connection.cursor()
#             data = (seg.get_address_range(),)
#             cursor.execute(clear_segment_witnesses, data)
#             connection.commit()
#         except:
#             connection.rollback()
#             pass
#
#         for reading_label in seg.readings.keys():
#             print(reading_label)
#             reading = seg.readings[reading_label]
#             w_count = 0
#             for witness in reading.witnesses:
#                 data = (witness.doc_id, seg.get_address_range(), reading.label, witness.label_suffix, witness.mss_text)
#                 try:
#                     cursor = connection.cursor()
#                     cursor.execute(witness_insert_query, data)
#                     connection.commit()
#                     w_count += 1
#                 except psycopg2.errors.UniqueViolation:
#                     connection.rollback()
#                     pass
#             print('added %d witnesses' % w_count)
#
#
# if __name__ == '__main__':
#     main()
