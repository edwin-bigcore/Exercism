from iou_db import DB
from iou_model_document import Document


db=DB(':memory:')

Document(   db, 
        lender   = 'l_name', 
        borrower = 'b_name', 
        amount   = 30
).save()

expected = {
    'number'  : 1, 
    'lender'  : 'l_name', 
    'borrower': 'b_name', 
    'amount'  : 30
}

print('exp: ', expected)

document = Document.read(db, expected['number'])[0]
document.amount-= 15
print('amount: ', document.amount)
document.save()
print('amount: ', document.amount)

expected['amount']-= 15

document = Document.read(db, expected['number'])[0]

print('doc: ', document.__dict__)
print('exp: ', expected)