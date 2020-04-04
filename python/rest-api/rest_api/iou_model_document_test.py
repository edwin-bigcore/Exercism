from iou_db import DB
from iou_model_document import Document

import unittest


class DocumentTest(unittest.TestCase):

    def test_create_one_record(self):
        db=DB(':memory:')
        db._reset_memory_data()
        expected = self.create_one(db)
        document = Document.read(db, expected['number'])[0]
        self.assertEqual(document.__dict__, expected)

    def test_update_record(self):
        db=DB(':memory:')
        db._reset_memory_data()
        expected = self.create_one(db)

        document = Document.read(db, expected['number'])[0]
        document.amount-= 15
        document.save()

        expected['amount']-= 15

        document = Document.read(db, expected['number'])[0]
        self.assertEqual(document.__dict__, expected)

    def test_create_several_records(self):
        db=DB(':memory:')
        db._reset_memory_data()
        expected=self.create_several(db)

        documents = [document.__dict__ for document in Document.read(db)]
        self.assertEqual(documents, expected)

    def create_one(self, db):
        ''' 1.- Create one record in database 
            2.- Returns the expected result
        '''

        Document(   db, 
                    lender   = 'l_name', 
                    borrower = 'b_name', 
                    amount   = 30
        ).save()

        return {
                'number'  : 1, 
                'lender'  : 'l_name', 
                'borrower': 'b_name', 
                'amount'  : 30
        }

    def create_several(self, db, number=3):
        ''' 1.- Create several records in database 
            2.- Returns the expected result
        '''

        expected = []

        for i in range(1, number+1):

            record = {
                'number'  : i,
                'lender'  : 'l_user{}'.format(i),
                'borrower': 'b_user{}'.format(i),
                'amount'  : i * 1.5,
            }

            Document( db, 
                    lender   = record['lender'], 
                    borrower = record['borrower'], 
                    amount   = record['amount']
            ).save()

            expected += [record]

        return expected

if __name__ == "__main__":
    unittest.main()