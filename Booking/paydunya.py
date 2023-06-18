import paydunya
from paydunya import InvoiceItem, Store

# runtime configs
PAYDUNYA_ACCESS_TOKENS = {
    'PAYDUNYA-MASTER-KEY': "test_public_jHPqdpTtsuPfMdCELJQCH6kEHGm",
    'PAYDUNYA-PRIVATE-KEY': "test_private_fx3VK4nxqQN0OopYYsUv9aEdunz",
    'PAYDUNYA-TOKEN': "Iw3azhgFM5dSgDNG3ZaK"
}
# defaults to False
paydunya.debug = True
# set the access/api keys
paydunya.api_keys = PAYDUNYA_ACCESS_TOKENS

# Invoice
store = Store(name='Magasin Chez Sandra')
items = [
    InvoiceItem(
        name="Clavier DELL",
        quantity=2,
        unit_price="3000",
        total_price="6000",
        description="Best Keyboard of the 2015 year"
    ),
    InvoiceItem(
        name="Ordinateur Lenovo L440",
        quantity=1,
        unit_price="400000",
        total_price="400000",
        description="Powerful and slim"
    ),
]
invoice = paydunya.Invoice(store)
invoice.add_items(items)
# taxes are (key,value) pairs
invoice.add_taxes([("Other TAX", 5000), ("TVA (18%)", 700)])
invoice.add_custom_data([
    ("first_name", "Alioune"),
    ("last_name", "Badara"),
    ("cart_id", 97628),
    ("coupon", "NOEL"),
])

# you can also pass the items, taxes, custom to the `create` method
successful, response = invoice.create()
if successful:
    print(response)

# confirm invoice
invoice.confirm('YOUR_INVOICE_TOKEN')


# PSR
opr_data = {
    'account_alias': 'EMAIL_OU_NUMERO_DU_CLIENT_PAYDUNYA',
    'description': 'Hello World',
    'total_amount': 6500
}
store = paydunya.Store(name='Magasin Chez Sandra')
opr = paydunya.OPR(opr_data, store)
# You can also pass the data to the `create` function
successful, response = opr.create()
if successful:
   print(response)
status, _ = opr.charge({
    'token': Iw3azhgFM5dSgDNG3ZaK,
    'confirm_token': Iw3azhgFM5dSgDNG3ZaK
})

# Direct Pay
account_alias =  "ahmedlaye2001@gmail.com"
amount =  6500
# toggle debug switch to True
direct_pay = paydunya.DirectPay(account_alias, amount)
status, response = direct_pay.process()