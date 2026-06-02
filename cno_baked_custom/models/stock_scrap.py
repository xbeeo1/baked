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

    def unlink(self):
        related_records = self.env['stock.move'].search([
            ('scrap_id', 'in', self.ids)
        ])
        result = super().unlink()
        for record in related_records:
            record.write({
                'scrap_created': False,
                'scrap_id': False,
                'allocation_state': 'draft',
            })

        return result

    def action_validate(self):
        res = super().action_validate()
        misc_journal = self.env['account.journal'].search([('type', '=', 'general')], limit=1)
        lines = []
        for scrap in self:
            po_obj= self.env['purchase.order'].search([('name', '=', scrap.origin)], limit=1)
            pol_obj= self.env['purchase.order.line'].search([('order_id', '=', po_obj.id),('product_id','=',scrap.product_id.id)], limit=1)
            if scrap.product_id.expiration_per > 0:
                if scrap.product_id.cost_of_goods_exp_adjustment and scrap.product_id.inventory_vendor_exp_Adjustment_cr and scrap.product_id.commission_exp_adjustment:
                    amount = (scrap.scrap_qty * pol_obj.price_unit) *(scrap.product_id.expiration_per/100)
                    lines.append((0, 0, {
                        'account_id': scrap.product_id.cost_of_goods_exp_adjustment.id,
                        'debit': amount,
                        'credit': 0.0,
                        'name': scrap.product_id.name,
                        'partner_id': scrap.product_id.vendor_id.id,
                    }))
                    lines.append((0, 0, {
                        'account_id': scrap.product_id.commission_exp_adjustment.id,
                        'debit': amount,
                        'credit': 0.0,
                        'name': scrap.product_id.name,
                        'partner_id': scrap.product_id.vendor_id.id,
                    }))
                    lines.append((0, 0, {
                        'account_id': scrap.product_id.inventory_vendor_exp_Adjustment_cr.id,
                        'debit': 0.0,
                        'credit': amount*2,
                        'name': scrap.product_id.name,
                        'partner_id': scrap.product_id.vendor_id.id,
                    }))
            else:
                if scrap.product_id.cost_of_goods_exp_adjustment.id and scrap.product_id.inventory_vendor_exp_Adjustment_cr.id:
                    lines.append((0, 0, {
                        'account_id': scrap.product_id.cost_of_goods_exp_adjustment.id,
                        'debit': scrap.scrap_qty * pol_obj.price_unit,
                        'credit': 0.0,
                        'name': scrap.product_id.name,
                        'partner_id': scrap.product_id.vendor_id.id,
                    }))

                    lines.append((0, 0, {
                        'account_id': scrap.product_id.inventory_vendor_exp_Adjustment_cr.id,
                        'debit': 0.0,
                        'credit': scrap.scrap_qty * pol_obj.price_unit,
                        'name': scrap.product_id.name,
                        'partner_id': scrap.product_id.vendor_id.id,
                    }))

            if lines:
                move_obj = self.env['account.move'].create({
                    'ref': scrap.name,
                    'journal_id': misc_journal.id,
                    'move_type': 'entry',
                    'line_ids': lines,
                })
                move_obj.action_post()
            related_records = self.env['stock.move'].search([
                ('scrap_id', '=', scrap.id)
            ])
            if related_records:
                for record in related_records:
                    record.write({
                        'allocation_state': 'done',
                    })

        return res


