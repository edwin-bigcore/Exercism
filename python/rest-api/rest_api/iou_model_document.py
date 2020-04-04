from iou_db import DB

class Document(object):
    ''' I Owe You Document 
    '''

    dc = {'Debit':'D', 'Credit':'C'}

    def __init__(self, db, number=None, lender=None, borrower=None, amount=None, **kwargs):
        self.__db = db
        self.__number = number
        self.lender = lender
        self.borrower = borrower
        self.amount = amount

    def save(self):
        ''' Save IOU Document to database
        '''
        if self.__number==None:
            self.__number=Document.__create(self.__db, **self.__dict__)
        else:
            self.__number=Document.__update(self.__db, **self.__dict__)

    @staticmethod
    def read(db, number=None, lender=None, borrower=None, **kwargs):
        ''' Return iou records
        '''
        return [ Document(db, **record) 
                 for record in Document.__read(db, number, lender, borrower)]

    @staticmethod
    def __create(db, lender, borrower, amount=0, **kwargs):
        ''' Create IOU Document in database
        '''
        query = ''' 
            INSERT INTO documents(lender, borrower, amount)
                           values(     ?,        ?,      ?)
        '''
        cursor = db.conn.cursor()
        cursor.execute(query, (lender, borrower, amount) )
        return cursor.lastrowid

    @staticmethod
    def __read(db, number=None, lender=None, borrower=None, **kwargs):
        ''' Read IOU Document From database
        '''
        params={} 
        if number:   params['number']=str(number)
        if lender:   params['lender']=lender
        if borrower: params['borrower']=borrower

        where = ''
        if params != {}:
            filter = ' and '.join( ['{} = ?'.format(k) for k in params ] )
            where = 'WHERE {}'.format(filter)

        query = ''' 
            SELECT number, lender, borrower, amount FROM documents {}
        '''.format(where)

        result = db.conn.execute(query, list(params.values()) )

        records = [{ 
                'number': record[0], 
                'lender': record[1],
                'borrower': record[2],
                'amount': record[3]
        } for record in result.fetchall() ]

        return records

    @staticmethod
    def __update(db, number, lender=None, borrower=None, amount=0, **kwargs):
        ''' Update IOU Document in database
        '''
        query = ''' 
            UPDATE documents
                SET lender   = ?,
                    borrower = ?,
                    amount   = ?
                WHERE number = ?
        '''
        db.conn.execute(query, (lender, borrower, str(amount), str(number)))

    @property
    def __dict__(self):
        return {
            'number': self.__number,
            'lender': self.lender,
            'borrower': self.borrower,
            'amount': self.amount
        }
