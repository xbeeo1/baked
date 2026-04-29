# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductVariantInherit(models.Model):
    _inherit = 'product.product'

    vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor',related='product_tmpl_id.vendor_id', store=True)
    product_owner_id = fields.Many2one(comodel_name='res.partner', string='Product Owner',related='product_tmpl_id.product_owner_id', store=True)
    stream = fields.Char(string='Stream',related='product_tmpl_id.stream', store=True)
    brand = fields.Char(string='Brands',related='product_tmpl_id.brand', store=True)

