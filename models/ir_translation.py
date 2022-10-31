# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import deepl
import logging

from .deepl_target_languages import DEEPL_TARGET_LANGUAGES
from .deepl_mapped_languages import DEEPL_MAPPED_LANGUAGES
from odoo import models, api, fields, _


class IrTranslation(models.Model):
    _inherit = 'ir.translation'

    translated_text = fields.Char(string='Preview Translated Text')
    product_exist = fields.Boolean(string='Exist', default=False)
    product_type = fields.Selection([
        ('product_template', 'Product'),
        ('product_product', 'Variant')
    ], string='Product Type')
    product_name = fields.Char(string='Product Name')
    product_field_name = fields.Char(string='Field Name', compute='get_field_name', store=True)

    def cron_deepl_product_translations(self):
        translations = self.env['ir.translation'].search([
            ('product_exist', '=', True),
            ('state', '!=', 'translated')
        ])
        for record in translations:
            record.deepl_translate()
            record.deepl_translate_save()

    @api.model
    def website_page_translation(self, block, iso_code):
        code = self.env['res.lang'].search([('iso_code', '=', iso_code)], limit=1).code
        code = code.split('_')[-1]
        languages = [(code, block)]
        word = block
        translation = self.get_deepl_translation(languages=languages, word=word)[0]
        return translation

    @api.depends('name')
    def get_field_name(self):
        for record in self:
            if record.name and ',' in record.name:
                name = record.name.split(',')
                field = self.env['ir.model.fields'].search([
                    ('name', '=', name[-1]),
                    ('model_id.model', '=', name[0])
                ], limit=1)
                if name[-1] == 'website_description':
                    record.product_field_name = 'Website Description'
                else:
                    record.product_field_name = field.field_description if field else False
            else:
                record.product_field_name = False

    def check_product_exist(self):
        for record in self:
            if record.name.startswith('product.template,'):
                exist = self.env['product.template'].sudo().search([
                    ('active', 'in', [False, True]),
                    ('id', '=', record.res_id)
                ])
                if not exist:
                    record.product_exist = record.product_type = record.product_name = False
                else:
                    record.product_exist, record.product_type, record.product_name = True, 'product_template', exist.name
            elif record.name.startswith('product.product,'):
                exist = self.env['product.product'].sudo().search([
                    ('active', 'in', [False, True]),
                    ('id', '=', record.res_id)
                ])
                if not exist:
                    record.product_exist = record.product_type = record.product_name = False
                else:
                    record.product_exist, record.product_type, record.product_name = True, 'product_product', exist.name
            else:
                record.product_exist = record.product_type = record.product_name = False

    @api.model
    def get_deepl_translation(self, languages, word):
        auth_key = self.env['ir.config_parameter'].sudo().get_param('deepl.auth.key')
        translator = deepl.Translator(auth_key)
        translations = []
        for lang in languages:
            if lang[0] in DEEPL_TARGET_LANGUAGES:
                try:
                    target_lang = lang[0]
                    if DEEPL_MAPPED_LANGUAGES.get(target_lang):
                        target_lang = DEEPL_MAPPED_LANGUAGES[target_lang]
                    translation = translator.translate_text(word, target_lang=target_lang, tag_handling='html')
                    translations.append(translation.text)
                except Exception as e:
                    logging.info(f'Error: {e}')
                    translations.append(lang[1])
            else:
                translations.append(lang[1])
        return translations

    def deepl_translate(self):
        word = self.src
        language = self.lang.split('_')[-1]
        languages = [(language, word)]
        translation = self.get_deepl_translation(languages, word)[0]
        self.write({'translated_text': translation})

    def deepl_translate_save(self):
        if self.translated_text:
            self.write({'value': self.translated_text})
            self.write({'translated_text': False})

    def translate_products(self):
        for record in self:
            record.deepl_translate()
            record.deepl_translate_save()

    @api.model
    def translate_fields_products(self):
        product_template = self.env['product.template'].sudo().search([('active', 'in', [False, True])])
        product_product = self.env['product.product'].sudo().search([('active', 'in', [False, True])])
        product_template_fields = self.env['ir.model.fields'].sudo().search([
            ('translate', '=', True),
            ('model_id.model', '=', 'product.template')
        ])
        product_product_fields = self.env['ir.model.fields'].sudo().search([
            ('translate', '=', True),
            ('model_id.model', '=', 'product.product')
        ])
        for field in product_product_fields:
            self.insert_missing_translation_for_products(field, product_product, 'product.product')
        for field in product_template_fields:
            self.insert_missing_translation_for_products(field, product_template, 'product.template')
        products = self.env['ir.translation'].search([
            ('name', 'ilike', 'product.template,')
        ])
        variants = self.env['ir.translation'].search([
            ('name', 'ilike', 'product.product,')
        ])
        products.check_product_exist()
        variants.check_product_exist()

    @api.model
    def insert_missing_translation_for_products(self, field, records, model_name):
        """ Insert missing translations for `field` on `records`. """
        records = records.with_context(lang=None)
        external_ids = records.get_external_id()  # if no xml_id, empty string
        if callable(field.translate):
            # insert missing translations for each term in src
            query = """ INSERT INTO ir_translation (lang, type, name, res_id, src, value, module, state)
                              SELECT l.code, 'model_terms', %(name)s, %(res_id)s, %(src)s, '', %(module)s, 'to_translate'
                              FROM res_lang l
                              WHERE l.active AND NOT EXISTS (
                                  SELECT 1 FROM ir_translation
                                  WHERE lang=l.code AND type='model' AND name=%(name)s AND res_id=%(res_id)s AND src=%(src)s
                              )
                              ON CONFLICT DO NOTHING;
                          """
            for record in records:
                module = external_ids[record.id].split('.')[0]
                src = record[field.name] or None
                for term in set(field.get_trans_terms(src)):
                    self._cr.execute(query, {
                        'name': "%s,%s" % (model_name, field.name),
                        'res_id': record.id,
                        'src': term,
                        'module': module
                    })
        else:
            # insert missing translations for src
            query = """ INSERT INTO ir_translation (lang, type, name, res_id, src, value, module, state)
                              SELECT l.code, 'model', %(name)s, %(res_id)s, %(src)s, '', %(module)s, 'to_translate'
                              FROM res_lang l
                              WHERE l.active AND NOT EXISTS (
                                  SELECT 1 FROM ir_translation
                                  WHERE lang=l.code AND type='model' AND name=%(name)s AND res_id=%(res_id)s
                              );

                              DELETE FROM ir_translation dup
                              WHERE type='model' AND name=%(name)s AND res_id=%(res_id)s
                                  AND dup.id NOT IN (SELECT MAX(t.id)
                                             FROM ir_translation t
                                             WHERE t.lang=dup.lang AND type='model' AND name=%(name)s AND res_id=%(res_id)s
                                  );

                              UPDATE ir_translation SET src=%(src)s
                              WHERE type='model' AND name=%(name)s AND res_id=%(res_id)s;
                          """
            for record in records:
                module = external_ids[record.id].split('.')[0]
                self._cr.execute(query, {
                    'name': "%s,%s" % (model_name, field.name),
                    'res_id': record.id,
                    'src': record[field.name] or None,
                    'module': module
                })
        self._modified_model(model_name)
