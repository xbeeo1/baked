# -*- coding: utf-8 -*-

from functools import partial

from odoo import models, fields


class ReportPosOrder(models.Model):
    _inherit = "report.pos.order"
    vendor_id = fields.Many2one(comodel_name=
        "res.partner",
        string="Vendor",
        readonly=True,
    )

    def _select(self):
        return super()._select() + ',pt.vendor_id AS vendor_id'

    def _group_by(self):
        return super()._group_by() + ',pt.vendor_id'
