# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        record = super().create(vals)
        self.env['ir.translation'].translate_fields_products()
        return record

    def unlink(self):
        self.env['ir.translation'].search([
            ('res_id', 'in', self.ids),
            ('name', 'ilike', 'product.template,')
        ]).unlink()
        res = super().unlink()
        return res

    def translate_products_deepl(self):
        translations = self.env['ir.translation'].search([
            ('product_exist', '=', True),
            ('res_id', 'in', self.env.context['active_ids']),
            ('name', '=like', 'product.template,%')
        ])
        for record in translations:
            record.deepl_translate()
            record.deepl_translate_save()


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        record = super().create(vals)
        self.env['ir.translation'].translate_fields_products()
        return record

    def unlink(self):
        self.env['ir.translation'].search([
            ('res_id', 'in', self.ids),
            ('name', 'ilike', 'product.product,')
        ]).unlink()
        res = super().unlink()
        return res

    def translate_products_deepl(self):
        translations = self.env['ir.translation'].search([
            ('product_exist', '=', True),
            ('res_id', 'in', self.env.context['active_ids']),
            ('name', '=like', 'product.product,%')
        ])
        for record in translations:
            record.deepl_translate()
            record.deepl_translate_save()
