import sqlite3
import json

class IOUDatabase:
    ''' I Owe You Database 
    '''

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
        ''' Create an in-memory database 
        '''
        self.connection = sqlite3.connect(':memory:')
        self.connection.execute(self.create_users_table_string)
        self.connection.execute(self.create_documents_table_string)

    def c_users(self, users):
        ''' create user in database
            :param users: [{'name':'username', 'balance':'0.0'}]
        '''
        self.connection.executemany(
            "INSERT INTO users(name, balance) values (?,?)", 
            [ (user['name'], user['balance']) for user in users ] )

    def c_document(self, lender, borrower, amount):
        ''' create iou document in database
            :param lender: lender user name
            :param borrower: borrower user name
            :param amount: amount
        '''

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
        ''' Read user from database
            :param name: 'name1'
            :return: {'account':'1234', 'name':'name1', 'balance':'0.0'}
        '''

        query = '''
            SELECT account, name, balance FROM users
                WHERE account = ?
        '''

        record = self.connection.execute(query, (account,)).fetchone()

        return { 'account':record[0], 'name':record[1], 'balance':record[2] }

    def r_user_by_name(self, name=''):
        ''' Read user from database
            :param name: 'name1'
            :return: {'account':'1234', 'name':'name1', 'balance':'0.0'}
        '''

        query = '''
            SELECT account, name, balance FROM users
                WHERE name = ?
        '''

        record = self.connection.execute(query, (name,)).fetchone()

        return { 'account':record[0], 'name':record[1], 'balance':record[2] }

    def r_users(self, names):
        ''' Read users from database
            :param names: ['name1','name2']
            :return: [{'account':'1234', 'name':'name1', 'balance':'0.0'}]
        '''

        query = "SELECT account, name, balance FROM users"
        if names != []:
            query += ''' WHERE name IN ({}) ORDER BY name
                     '''.format(','.join('?'*len(names)))

        records = self.connection.execute(query, names).fetchall()
        return [{ 'account': record[0], 
                  'name'   : record[1], 
                  'balance': record[2] } for record in records]

    def r_account_iou(self, account, dc=dc['Debit']):
        ''' Reads account debits or credits
            :param account: account number
            :param dc: debit/credit indicator 
            :return: [{'account':'123', 'amount':'0.0'}]
        '''

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
        ''' Update a given user balance in the database
            :param account: user account number
            :param balance: new balance
        '''

        query = '''
            UPDATE users SET balance = ? 
                WHERE account = ?
        '''
        
        self.connection.execute(query, (balance, account))

class RestAPI:

    def __init__(self, database=None):
        ''' Rest API Initialization
            :param database: { 'users' : [{ ... }] }
        '''
        self.ioudb = IOUDatabase()
        self.create_data_from( database )

    def create_data_from(self, database=None):
        ''' Database Initialization
            :param database: { 'users' : [{ 'name': 'name1',
                                            'owes': [{
                                                'name2':'0.0'
                                            }],
                                            'owed_by': [{
                                                'name2':'0.0'
                                            }],
                                            'balance': '0.0'
                                }] 
                             }
        '''
        
        # Initialization
        users = []
        documents = []

        # Prepare database data
        for db in database['users']:
            users += [{'name':db['name'], 'balance':'0.0'}]
            for name, amount in db['owes'].items():
                documents += [{ 
                                 'lender'   : name, 
                                 'borrower' : db['name'], 
                                 'amount'   : amount 
                             }]

        # Create users
        self.ioudb.c_users( users )

        # Create documents
        for document in documents:
            self.ioudb.c_document( 
                document['lender'], document['borrower'], document['amount'] )

    def get(self, url, payload=None):
        """ GET METHOD 
        """
        result = {"users": []}
        if url == "/users": result = self.users(
                    json.loads(payload) if payload != None else result)
        return json.dumps(result)

    def post(self, url, payload=None):
        """ POST METHOD 
        """
        result = {"users": []}
        if   url == "/add" : result = self.add(json.loads(payload)) 
        elif url == "/iou" : result = self.iou(json.loads(payload))
        return json.dumps(result)

    def users(self, params):
        ''' Returs the requested users
            :param parmas: {'users': ['name1']}
            :return: { 'users' : [{ 'name': 'name1',
                                    'owes' : [{
                                        'name2':'0.0'
                                    }],
                                    'owed_by': [{
                                        'name2':'0.0'
                                    }],
                                    'balance': '0.0'
                                 }] 
                     }
        '''

        # Init
        result = {'users': []}

        # Read accounts
        accounts = self.ioudb.r_users( params['users'] )

        # Create output
        for account in accounts:
            # Read users iou information
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
        ''' Create a new user
            :param user: new user = {'user': 'name1'}
            :return: read user
        '''
        self.ioudb.c_users([{'name':user['user'], 'balance':'0.0'}])
        return self.users({'users': [user['user']]})['users'][0]

    def iou(self, document):
        ''' Create IOU document
            :param iou: {'lender': 'name1', 'borrower': 'name2', 'amount': '0.0'}
            :return: read lender and borrower users
        '''
        self.ioudb.c_document( 
                document['lender'], document['borrower'], document['amount'] )
        return self.users({'users': [document['lender'], document['borrower']]} )

    def iou_value_list(self, account, dc):
        ''' Reads the iou of an user and returns it in a list
            :param account: account number
            :param dc: debit/credit indicator 
            :return: [{'name1':'0.0'}]
        '''
        result = {}
        for iou in self.ioudb.r_account_iou(account, dc):
            result[self.ioudb.r_user(iou['account'])['name']] = iou['amount']

        return result
