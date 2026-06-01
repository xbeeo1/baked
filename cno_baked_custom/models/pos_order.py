# -*- coding: utf-8 -*-


from odoo import fields, models,tools,api, _


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _generate_pos_order_invoice(self):
        move = super()._generate_pos_order_invoice()

        for order in self:
            if order.account_move:
                misc_journal = self.env['account.journal'].search([('type', '=', 'general')], limit=1)
                lines = []
                for line in order.account_move.line_ids:
                    if line.product_id:
                        credit_value = line.credit
                        debit_value = line.debit
                        if credit_value > 0.0 and line.account_id.id == line.product_id.commission_based_sale.id:
                            lines.append((0, 0, {
                                'account_id': line.product_id.commission_based_sale.id,
                                'debit': credit_value,
                                'credit': 0.0,
                                'name': 'Revsl/' + move.name,
                                'partner_id': None,
                            }))

                            lines.append((0, 0, {
                                'account_id': line.product_id.payable_to_supplier_cr.id,
                                'debit': 0.0,
                                'credit': credit_value,
                                'name': line.product_id.name,
                                'partner_id': None,
                            }))
                        if debit_value > 0.0 and line.account_id.id == line.product_id.cost_of_goods_cr.id:
                            lines.append((0, 0, {
                                'account_id': line.product_id.cost_of_goods_cr.id,
                                'debit': 0.0,
                                'credit': debit_value,
                                'name': 'Revsl/' + move.name,
                                'partner_id': None,
                            }))

                            lines.append((0, 0, {
                                'account_id': line.product_id.commission_cgs.id,
                                'debit': debit_value,
                                'credit': 0.0,
                                'name': line.product_id.name,
                                'partner_id': None,
                            }))
                    if line.tax_line_id:
                        credit_value = line.credit
                        debit_value = line.debit
                        if credit_value > 0.0:

                            lines.append((0, 0, {
                                'account_id': line.account_id.id,
                                'debit': credit_value,
                                'credit': 0.0,
                                'name':  line.name,
                                'partner_id': None,
                            }))
                            for orderline in self.lines.filtered(
                                    lambda lineorder: any(
                                        tax.name == line.name
                                        for tax in lineorder.tax_ids_after_fiscal_position
                                    )
                                ):
                                lines.append((0, 0, {
                                    'account_id': orderline.product_id.payable_to_supplier_cr.id,
                                    'debit': 0.0,
                                    'credit': orderline.price_subtotal_incl - orderline.price_subtotal,
                                    'name': orderline.product_id.name,
                                    'partner_id': None,
                                }))
                        if debit_value > 0.0:

                            lines.append((0, 0, {
                                'account_id': line.account_id.id,
                                'debit': 0.0,
                                'credit': debit_value,
                                'name':  line.name,
                                'partner_id': None,
                            }))
                            for orderline in self.lines.filtered(
                                    lambda lineorder: any(
                                        tax.name == line.name
                                        for tax in lineorder.tax_ids_after_fiscal_position
                                    )
                                ):

                                lines.append((0, 0, {
                                    'account_id': orderline.product_id.payable_to_supplier_cr.id,
                                    'debit': orderline.price_subtotal_incl - orderline.price_subtotal,
                                    'credit': 0.0,
                                    'name': orderline.product_id.name,
                                    'partner_id': None,
                                }))

                if lines:
                    move_obj = self.env['account.move'].create({
                        'ref': move.name,
                        'journal_id': misc_journal.id,
                        'move_type': 'entry',
                        'line_ids': lines,
                    })
                    move_obj.action_post()





        return move
