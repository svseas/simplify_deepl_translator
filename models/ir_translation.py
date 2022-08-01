# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import deepl

from odoo import models, api, fields, _


class IrTranslation(models.Model):
    _inherit = 'ir.translation'

    @api.model
    def get_deepl_translation(self, languages, word):
        auth_key = self.env['ir.config_parameter'].sudo().get_param('deepl.auth.key')
        translator = deepl.Translator(auth_key)
        translations = []
        for lang in languages:
            try:
                translation = translator.translate_text(word, target_lang=lang[0])
                translations.append(translation.text)
            except:
                translations.append(lang[1])
        return translations
