# -*- coding: utf-8 -*-

from odoo import models,api,fields


class StockScrap(models.Model):
    _inherit = 'stock.scrap'


    @api.depends('move_ids', 'move_ids.move_line_ids.quantity', 'product_id')
    def _compute_scrap_qty(self):
        for scrap in self:
            scrap.scrap_qty = 1
            if scrap.move_ids:
                if scrap.move_ids[0].Qty > 0:
                    scrap.scrap_qty = scrap.move_ids[0].Qty
                else:
                    scrap.scrap_qty = scrap.move_ids[0].quantity