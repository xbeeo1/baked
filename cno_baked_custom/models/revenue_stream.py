# -*- coding: utf-8 -*-

from odoo import fields, models


class RevenueStream(models.Model):
    _name = "revenue.stream"
    _description = "Revenue Stream"

    name = fields.Char(string="Name",required=True)