# -*- coding: utf-8 -*-
{
    "name": "CNO POS Custom",

    'version': '19.0.0.0',

    'summary': """CNO POS Custom""",

    'description': """CNO POS Custom""",

    'category': 'POS',

    'author': "Musadiq Fiaz",

    'website': 'https://selectasol.com',

    "depends": ['point_of_sale','mrp'],

    "data": [
        'views/views.xml',
        'views/pos_payment_method.xml',
    ],

    'assets': {
            'point_of_sale._assets_pos': [
                'cno_pos_custom/static/src/**/*',

                    ],
                },


}

