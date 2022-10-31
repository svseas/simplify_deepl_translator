# -*- coding: utf-8 -*-
{
    'name': 'Deepl Translator',
    'version': '15.0.1.4.0',
    'summary': 'Deepl Translator',
    'description': 'Deepl Translator',
    'category': 'All',
    'author': 'Simplify-ERP™',
    'website': 'https://simplify-erp.com',
    'license': 'LGPL-3',
    'depends': ['web', 'sale_management', 'website'],
    'data': [
        'views/cron.xml',
        'views/deepl_auth_key.xml',
        'views/product_translations.xml'
    ],
    'assets': {
        'web._assets_common_scripts': [
            'simplify_deepl_translator/static/src/js/deepl.js'
        ],
        'website.assets_editor': [
            'simplify_deepl_translator/static/src/js/website_translator.js'
        ]
    },
    'external_dependencies': {
        'python': ['deepl']
    },
}
