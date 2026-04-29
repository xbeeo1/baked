# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    expiry_date = fields.Date(string='Expiry Date')
    cost_allocation = fields.Float(string='Cost Allocation %')
    cost_account_id = fields.Many2one(comodel_name='account.account', string='Cost Account')
    Qty = fields.Float(string='Qty')
    scrap_id = fields.Many2one(comodel_name='stock.scrap', string='Scrap')
    allocation_state = fields.Selection([('draft','Draft'),('done','Done')], default='draft', string='Allocation Status')

    picking_code = fields.Selection(
        related='picking_type_id.code',
        store=True
    )

    scrap_created = fields.Boolean(default=False)

    def action_create_scrap(self):
        self.ensure_one()

        if self.Qty <= 0:
            raise UserError("Qty should be greater than 0!")
        scrap = self.env['stock.scrap'].create({
            'product_id': self.product_id.id,
            'scrap_qty': self.Qty,
            'product_uom_id': self.product_uom.id,
            'location_id': self.location_id.id,
            'origin': self.origin or self.name,
            'picking_id': False,
        })

        self.scrap_created = True
        self.scrap_id = scrap.id

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.scrap',
            'view_mode': 'form',
            'res_id': scrap.id,
            'target': 'current',
        }

    def action_allocate_cost(self):
        """Allocate cost: create journal entry for this move"""
        self.ensure_one()

        if self.account_move_id and self.account_move_id.state != 'cancel':
            raise UserError("Cost already allocated! Cancel the journal entry first.")

        if self.cost_allocation <= 0:
            raise UserError("Cost Allocation should be greater than 0!")

        if not self.cost_account_id:
            raise UserError("Cost Account not defined on this move!")

        # Dr = cost_account, Cr = product property_account_expense_id
        if not self.product_id.property_account_expense_id:
            raise UserError(f"Product {self.product_id.name} has no expense account set!")

        misc_journal = self.env['account.journal'].search([('type', '=', 'general')], limit=1)

        move_dict = {
            'ref': self.scrap_id.name,
            'journal_id': misc_journal.id,

        }


        lines = [
            (0, 0, {
                'account_id': self.cost_account_id.id,
                'debit': (self.Qty * self.product_id.standard_price) * (self.cost_allocation/100),
                'credit': 0.0,
                'name': self.scrap_id.name,
            }),
            (0, 0, {
                'account_id': self.product_id.property_account_expense_id.id,
                'debit': 0.0,
                'credit': (self.Qty * self.product_id.standard_price or 0)* (self.cost_allocation/100),
                'name': self.scrap_id.name,
            }),
        ]


        move_dict['line_ids'] = lines
        move = self.env['account.move'].create(move_dict)
        self.allocation_state = 'done'
        self.account_move_id = move.id
