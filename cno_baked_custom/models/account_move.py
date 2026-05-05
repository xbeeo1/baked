# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)

        for move in moves:
            if move.move_type != 'in_invoice':
                continue

            if not move.invoice_line_ids:
                continue

            misc_journal = self.env['account.journal'].search([('type', '=', 'general')], limit=1)

            lines = []

            for line in move.invoice_line_ids:
                product = line.product_id

                if not product or not product.account_credit_id:
                    continue

                amount = line.price_subtotal  # ya price_total agar tax include chahiye

                # 🔹 Debit (Payable ya credit wali line se)
                credit_line = move.line_ids.filtered(lambda l: l.credit > 0.0)[:1]
                if not credit_line:
                    continue

                payable_account = credit_line.account_id

                # 🔹 2 lines per product
                lines.append((0, 0, {
                    'account_id': payable_account.id,
                    'debit': amount,
                    'credit': 0.0,
                    'name': move.name,
                    'partner_id': move.partner_id.id,
                }))

                lines.append((0, 0, {
                    'account_id': product.account_credit_id.id,
                    'debit': 0.0,
                    'credit': amount,
                    'name': product.name,
                    'partner_id': move.partner_id.id,
                }))

            if lines:
                move_dict = {
                    'ref': move.name,
                    'journal_id': misc_journal.id,
                    'move_type': 'entry',
                    'line_ids': lines,
                }

                self.env['account.move'].create(move_dict)

        return moves
