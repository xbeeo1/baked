# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor')
    product_owner_id = fields.Many2one(comodel_name='res.partner', string='Product Owner')
    stream = fields.Char(string='Stream')
    brand = fields.Char(string='Brands')


