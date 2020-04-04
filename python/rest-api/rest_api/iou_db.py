import sqlite3

class DB(object):
    ''' Database object 
    '''

    _drop_users_table_string = '''
        DROP TABLE IF EXISTS users
    '''

    _drop_documents_table_string = '''
        DROP TABLE IF EXISTS documents
    '''

    _create_users_table_string = ''' 
            CREATE TABLE IF NOT EXISTS users (
                account integer PRIMARY KEY, 
                name    text,
                balance real
            );
    '''

    _create_documents_table_string = ''' 
            CREATE TABLE IF NOT EXISTS documents (
                number   integer PRIMARY KEY, 
                lender   integer,
                borrower integer,
                amount   real NOT NULL
            );
    '''

    def __new__(cls, dbname=':memory:'):
        ''' Create only one instance per database 
        '''
        if not hasattr(cls, '_instances'): 
            DB._instances = {}
        if not dbname in DB._instances:
            DB._instances[dbname]=object.__new__(cls)
            DB._instances[dbname].dbname = dbname
            DB._instances[dbname].__connect()

        return DB._instances[dbname]

    def __connect(self, dbname=':memory:'):
        ''' 1.- Establish a database connection
            2.- Create tables if needed 
        '''
        self.conn = sqlite3.connect(self.dbname)
        self.conn.execute(self._create_users_table_string)
        self.conn.execute(self._create_documents_table_string)

    def _reset_memory_data(self):
        ''' Discard in memory database tables data 
        '''
        if self.dbname == ':memory:':
            self.conn.execute(self._drop_users_table_string)
            self.conn.execute(self._drop_documents_table_string)
            self.conn.execute(self._create_users_table_string)
            self.conn.execute(self._create_documents_table_string)

    def __del__(self):
        ''' Close db conecion
        '''
        self.conn.close()

    def __str__(self):
        ''' String representation 
        '''
        return '{0}({1})'.format(self.__class__.__name__, self.__dict__)
