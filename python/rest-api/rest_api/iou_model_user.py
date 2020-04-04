from iou_db import DB

class User(object):
    ''' User 
    '''
    def __init__(self, db, account=None, name=None, balance=0, **kwargs):
        self.__db = db
        self.__account = account
        self.name = name
        self.balance = balance

    def save(self):
        ''' Save User to database
        '''
        pass


    @staticmethod
    def read(db, account=None, name=None, balance=0 **kwargs):
        ''' Return users records
        '''
        pass

    @staticmethod
    def __create(db, name=None, balance=0 **kwargs):
        '''
        '''
        pass

    @staticmethod
    def __read(db, account=None, name=None, **kwargs):
        '''
        '''
        pass

    @staticmethod
    def __update(db, account, name=None, balance=0, **kwargs):
        '''
        '''



    @property
    def __dict__(self):
        return {
            'name': self.name,
            'balance': self.balance
        }
