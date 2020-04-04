#!/usr/bin/env python3.8
import json

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
