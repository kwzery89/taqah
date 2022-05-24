# -*- coding: utf-8 -*-

{
    "name": "e-Invoice KSA | tax invoice | report | qrcode | ZATCA | vat  | electronic | einvoice | e-invoice sa | accounting | tax  | Zakat, Tax and Customs Authority | invoice ",
    "version": "1.2",
    "depends": [
        'base', 'sale', 'account',
    ],
    "author": "Genius Valley",
    "category": "Accounting",
    "website": "https://genius-valley.com/",
    "support": "odoo@gvitt.com",
    "images": ["static/description/assets/main_screenshot.gif","static/description/assets/main_screenshot.png", "static/description/assets/ghits_desktop_inv.jpg",
               "static/description/assets/ghits_labtop1.jpg"],
    "price": "0",
    "license": "OPL-1",
    "currency": "USD",
    "summary": "e-Invoice in Kingdom of Saudi Arabia KSA | tax invoice | vat  | electronic | e invoice | accounting | tax | free | ksa | sa |Zakat, Tax and Customs Authority | الفاتورة الضريبية | الفوترة  الالكترونية |   هيئة الزكاة والضريبة والجمارك",
    "description": """
    e-Invoice in Kingdom of Saudi Arabia
    and prepare tax invoice to be ready for the second phase.
    Zakat, Tax and Customs Authority
    الفوترة الإلكترونية - الفاتورة الضريبية - المملكة العربية السعودية
    المرحلة الاولي -  مرحلة الاصدار 
    هيئة الزكاة والضريبة والجمارك

    Issues --------------------------------
        If QR code not appear v13 upgrade reportlab or use next command
                >>  pip uninstall reportlab
                >>  pip install reportlab
                
    Versions History --------------------
    
    * version 1.2 : 10-Oct-2021
        Initial version compatible with odoo 13, tax invoice report, QR code
   

    
    """
    ,
    "data": [

        "view/partner.xml",
        "report/base_document_layout.xml",
        "report/account_move.xml",

    ],
    "installable": True,
    "auto_install": True,
    "application": True,
}
