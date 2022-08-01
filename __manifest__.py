# -*- coding: utf-8 -*-
{
    'name': 'Deepl Translator',
    'version': '15.0.1.0.0',
    'summary': 'Deepl Translator',
    'description': 'Deepl Translator',
    'category': 'All',
    'author': 'Bojan Anchev',
    'license': 'LGPL-3',
    'depends': ['web'],
    'assets': {
        'web._assets_common_scripts': [
            'simplify_deepl_translator/static/src/js/deepl.js'
        ]
    },
    'external_dependencies': {
        'python': ['deepl']
    },
}
