# -*- coding: utf-8 -*-

from odoo import fields, models


class CostCentre(models.Model):
    _name = "cost.centre"
    _description = "Cost Centre"

    name = fields.Char(string="Name",required=True)