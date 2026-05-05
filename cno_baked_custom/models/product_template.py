# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor')
    product_owner_id = fields.Many2one(comodel_name='res.partner', string='Product Owner')
    stream = fields.Char(string='Stream')
    brand = fields.Char(string='Brands')
    account_debit_id = fields.Many2one(comodel_name='account.account', string='Account Debit')
    account_credit_id = fields.Many2one(comodel_name='account.account', string='Account Credit')
    commission_per = fields.Float(string='Commission %')


