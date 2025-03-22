# -*- coding: utf-8 -*-
{
    'name': "gestion_documents_stage",

    'summary': "Module pour gérer les documents de stage",

    'description': """
       Ce module permet aux étudiants de soumettre leurs documents de stage 
        et aux responsables de les valider et signer.
    """,

    'author': "Assiya BELKHEIRI",
    'website': "https://www.ensao.ump.ac.ma",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/request_stage.xml',
          'security/groups.xml',
          'views/menu.xml',
          'security/ir.model.access.csv',
         'views/views.xml',
         'views/templates.xml',
    ],
    'application': True,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

