# -*- coding: utf-8 -*-
{
    'name': 'Deepl Translator',
    'version': '15.0.1.0.0',
    'summary': 'Deepl Translator',
    'description': 'Deepl Translator',
    'category': 'All',
    'author': 'Simplify-ERP™',
    'website': 'https://simplify-erp.com',
    'license': 'LGPL-3',
    'depends': ['web'],
    'data': [
        'views/deepl_auth_key.xml'
    ],
    'assets': {
        'web._assets_common_scripts': [
            'simplify_deepl_translator/static/src/js/deepl.js'
        ],
        'web.assets_qweb': [
            'simplify_deepl_translator/static/src/xml/translate_dialog.xml'
        ]
    },
    'external_dependencies': {
        'python': ['deepl']
    },
}
