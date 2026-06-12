# -*- coding: utf-8 -*-

from odoo import fields, models


class BrandBrand(models.Model):
    _name = "brand.brand"
    _description = "Brand"

    name = fields.Char(string="Name",required=True)