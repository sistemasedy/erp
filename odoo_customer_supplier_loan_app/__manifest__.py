# -*- coding: utf-8 -*-
{
    'name': 'Loan Management for Customer and Supplier',
    "author": "Edge Technologies",
    'version': '16.0.1.0',
    'summary': 'Customer loan management supplier loan management partner loan installments vender loan management vendor credit loan interest for loan installment customer loan portal loan processing fee approve loan request customer disburse loan emi for customer emi',
    'description': """
        Customer loan management supplier loan management partner loan management for customer and supplier loan management for supplier and customer
        Customer and supplier loan management manages following things. apply loans as loan requests and send loan requests to approve
        Loan installments calculates based on the configuration. loan accounting with journal entries and journal item.
        Option to loans to disburse after the approval based loan proof manged different loan types with loan policie
        Loan managed with loan proofs and required documents list.  
        Different access as loan user and manager who can able to place create loan request.
        Only loan manager can able to  approve loan request. create disburse accounting journal entry form loan
        Calculate interest receivable from  loan entry. managed loan installments.
        caculate interest for loan installment entry. pay loan by installment which creates accounting journal entry. print loan report.
        Customer loans in portal - my account page. loan processing fees charges. odoo loan management. manager can add loan proofs/required documents list for loan.installment amount journal entries  manager can approve loan request
Odoo loan management
Vender loan management
Credit loan management
Vendor loan management
Vendor credit loan
EMI for customer
EMI for supplier 
EMI for vendor 
Loan app
Manage customer loan
Manage customer credit
Manage supplier loan 
Loan supplier
Loan vendor 
Loan client

  

        
""",
    "license" : "OPL-1",
    'depends': ['sale_management','account','base','purchase','stock'],
    'data': [
            'security/loan_management_group.xml',
            'security/ir.model.access.csv',
            'views/loan_proof_view.xml',
            'views/loan_type_view.xml',
            'views/loan_policies_view.xml',
            'views/loan_request_view.xml',
            'views/loan_installment_view.xml',
            'views/partner_views.xml',
            'views/account_payment_view.xml',
    ],
    'live_test_url':'https://youtu.be/1rDd1dxqemg',
    "images":['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'price': 45,
    'currency': "EUR",
    'category': 'Sales',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
