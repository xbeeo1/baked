# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor')
    product_owner_id = fields.Many2one(comodel_name='res.partner', string='Product Owner')
    stream = fields.Char(string='Stream')
    brand = fields.Char(string='Brands')
    payable_suppl_2221001_id = fields.Many2one(comodel_name='account.account', string='2221001 Payable to Supplier (Dr.)')
    stock_hand_1125001_id = fields.Many2one(comodel_name='account.account', string='1125001 Stock in Hand (Cr.)')
    account_debit_id = fields.Many2one(comodel_name='account.account', string='2223002 Inventory held on b/f Vendors (Dr.)')
    account_credit_id = fields.Many2one(comodel_name='account.account', string='2223006 Commission based Vendor C/A (Cr.)')
    commission_based_sale = fields.Many2one(comodel_name='account.account', string='3111001 Commission Based Sale (Dr.)')
    commission_asset_cr = fields.Many2one(comodel_name='account.account', string='1125001 Stock In Hand (Dr.)')
    commission_cgs = fields.Many2one(comodel_name='account.account', string='2223006 Commission based Vendor C/A (Dr.)')
    payable_to_supplier_cr = fields.Many2one(comodel_name='account.account', string='2221001 Payable to Supplier (Cr.)')
    inventory_vendor_cr = fields.Many2one(comodel_name='account.account', string='2223002 Inventory held on b/f Vendors (Cr.)')
    cost_of_goods_cr = fields.Many2one(comodel_name='account.account', string='4111003 Cost of Goods Sold (Cr.)')
    commission_income = fields.Many2one(comodel_name='account.account', string='Commission Income-3111001')
    commission_tax = fields.Many2one(comodel_name='account.account', string='Commission Tax-3111001')
    commission_per = fields.Float(string='Commission %')


