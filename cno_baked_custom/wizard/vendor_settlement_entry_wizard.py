# -*- coding: utf-8 -*-

from odoo import models


class VendorSettlementEntryWizard(models.TransientModel):
    _name = "vendor.settlement.entry.wizard"
    _description = "Vendor Settlement Entry Wizard"

    def action_create(self):
        move_obj = self.env['account.move'].search([('vendor_settlement_entry','=',False),('move_type','=','in_invoice')])
        if move_obj:
            for move in move_obj:
                if not move.invoice_line_ids:
                    continue
                misc_journal = self.env['account.journal'].search([('type', '=', 'general')], limit=1)

                lines = []

                for line in move.invoice_line_ids:
                    product = line.product_id

                    credit_line = move.line_ids.filtered(lambda l: l.credit > 0.0)[:1]
                    if credit_line and product and product.account_credit_id and product.payable_suppl_2221001_id:
                        lines.append((0, 0, {
                            'account_id': product.payable_suppl_2221001_id.id,
                            'debit': line.price_subtotal,
                            'credit': 0.0,
                            'name': 'Revsl/' + move.name,
                        }))

                        lines.append((0, 0, {
                            'account_id': product.account_credit_id.id,
                            'debit': 0.0,
                            'credit': line.price_subtotal,
                            'name': product.name,
                        }))

                    # debit_line = move.line_ids.filtered(lambda l: l.debit > 0.0)[:1]
                    # if debit_line and product and product.account_debit_id and product.stock_hand_1125001_id:
                    #     lines.append((0, 0, {
                    #         'account_id': product.stock_hand_1125001_id.id,
                    #         'debit': 0.0,
                    #         'credit': line.price_subtotal,
                    #         'name': 'Revsl/' + move.name,
                    #     }))
                    #
                    #     lines.append((0, 0, {
                    #         'account_id': product.account_debit_id.id,
                    #         'debit': line.price_subtotal,
                    #         'credit': 0.0,
                    #         'name': product.name,
                    #     }))

                if lines:
                    move_obj = self.env['account.move'].create({
                        'ref': move.name,
                        'journal_id': misc_journal.id,
                        'move_type': 'entry',
                        'line_ids': lines,
                    })
                    move_obj.action_post()
                move.vendor_settlement_entry = True
