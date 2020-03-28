import sqlite3
import json

class IOUDatabase:
    dc = {'Debit':'D', 'Credit':'C'}

    create_users_table_string = ''' 
            CREATE TABLE users (
                account integer PRIMARY KEY, 
                name    text,
                balance real
            );
    '''

    create_documents_table_string = ''' 
            CREATE TABLE documents (
                number   integer PRIMARY KEY, 
                lender   integer,
                borrower integer,
                amount   real NOT NULL
            );
    '''

    def __init__(self):
        self.connection = sqlite3.connect(':memory:')
        self.connection.execute(self.create_users_table_string)
        self.connection.execute(self.create_documents_table_string)

    def c_users(self, users):
        self.connection.executemany(
            "INSERT INTO users(name, balance) values (?,?)", 
            [ (user['name'], user['balance']) for user in users ] )

    def c_document(self, lender, borrower, amount):

        #Read lender and borrower user data
        lender = self.r_user_by_name(lender)
        borrower = self.r_user_by_name(borrower)

        # Prepare new document data
        document = (lender['account'], borrower['account'], amount )

        # Create document in database
        query_create_document = '''
            INSERT INTO documents(lender, borrower, amount)
                           values(     ?,        ?,      ?)
        '''

        self.connection.execute(query_create_document, document)

        # Update lender balance
        self.u_user_balance(lender['account'], lender['balance'] + amount)
        # Update borrower balance
        self.u_user_balance(borrower['account'], borrower['balance'] - amount)

    def r_user(self, account=0):

        query = '''
            SELECT account, name, balance FROM users
                WHERE account = ?
        '''

        record = self.connection.execute(query, (account,)).fetchone()

        return { 'account':record[0], 'name':record[1], 'balance':record[2] }

    def r_user_by_name(self, name=''):

        query = '''
            SELECT account, name, balance FROM users
                WHERE name = ?
        '''

        record = self.connection.execute(query, (name,)).fetchone()

        return { 'account':record[0], 'name':record[1], 'balance':record[2] }

    def r_users(self, names):

        query = "SELECT account, name, balance FROM users"
        if names != []:
            query += ''' WHERE name IN ({}) ORDER BY name
                     '''.format(','.join('?'*len(names)))

        records = self.connection.execute(query, names).fetchall()
        return [{ 'account': record[0], 
                  'name'   : record[1], 
                  'balance': record[2] } for record in records]

    def r_account_iou(self, account, dc=dc['Debit']):

        # Select lender or borrower 
        if dc == self.dc['Debit']: 
            columns = 'main.borrower, main.lender'
            filter = 'borrower'
        else:                
            columns = 'main.lender, main.borrower'
            filter = 'lender'

        # Prepare query
        query = '''
            SELECT {}, SUM( main.amount ) as main_amount,
                       SUM( clrd.amount ) as clrd_amount
                FROM documents as main
                    LEFT JOIN documents as clrd 
                           ON clrd.borrower = main.lender
                          AND clrd.lender   = main.borrower
                WHERE main.{} = ?
                GROUP BY main.lender, main.borrower
        '''.format(columns, filter)

        # Read items
        records = self.connection.execute(query, (str(account),) ).fetchall()
        
        # Return iou records
        result = []
        for record in records:
            value = record[2] - ( record[3] or 0 )
            if value > 0:
                result += [{'account': record[1], 'amount' : value }]
        
        return result

    def u_user_balance(self, account, balance):

        query = '''
            UPDATE users SET balance = ? 
                WHERE account = ?
        '''
        
        self.connection.execute(query, (balance, account))

class RestAPI:

    def __init__(self, database=None):
        self.ioudb = IOUDatabase()
        self.create_data_from( database )

    def create_data_from(self, database=None):
        users = []
        documents = []

        for db in database['users']:
            users += [{'name':db['name'], 'balance':'0.0'}]
            for name, amount in db['owes'].items():
                documents += [{ 
                                 'lender'   : name, 
                                 'borrower' : db['name'], 
                                 'amount'   : amount 
                             }]

        self.ioudb.c_users( users )

        for document in documents:
            self.ioudb.c_document( 
                document['lender'], document['borrower'], document['amount'] )

    def get(self, url, payload=None):
        result = {"users": []}
        if url == "/users": result = self.users(
                    json.loads(payload) if payload != None else result)
        return json.dumps(result)

    def post(self, url, payload=None):
        result = {"users": []}
        if   url == "/add" : result = self.add(json.loads(payload)) 
        elif url == "/iou" : result = self.iou(json.loads(payload))
        return json.dumps(result)

    def users(self, params):

        result = {'users': []}

        accounts = self.ioudb.r_users( params['users'] )

        for account in accounts:
            result['users'] += [{ 'name'   : account['name'],
                                  'owes'   : self.iou_value_list( 
                                                    account['account'],
                                                    self.ioudb.dc["Debit"] ),
                                  'owed_by': self.iou_value_list( 
                                                    account['account'],
                                                    self.ioudb.dc["Credit"] ),
                                  'balance': account['balance']
            }]

        return result

    def add(self, user ):
        self.ioudb.c_users([{'name':user['user'], 'balance':'0.0'}])
        return self.users({'users': [user['user']]})['users'][0]

    def iou(self, document):
        self.ioudb.c_document( 
                document['lender'], document['borrower'], document['amount'] )
        return self.users({'users': [document['lender'], document['borrower']]} )

    def iou_value_list(self, account, dc):
        result = {}
        for iou in self.ioudb.r_account_iou(account, dc):
            result[self.ioudb.r_user(iou['account'])['name']] = iou['amount']

        return result
