# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class POsCustomDiscount(models.Model):
    _name = "pos.custom.discount"
    _description = "Pos Custom Discounts"
    _inherit = ["pos.load.mixin"]

    name = fields.Char(string="Name", required=1)
    discount_percent = fields.Float(string="Discount Percentage", required=1)
    description = fields.Text(string="Description")
    available_in_pos = fields.Many2many(
        'pos.config', string="Available In Pos")
    
    @api.model
    def _load_pos_data_fields(self, config_id):
        return ['name', 'discount_percent', 'description', 'available_in_pos']

    @api.constrains('discount_percent')
    def check_validation_discount_percent(self):
        """This is to validate discount percentage"""
        if self.discount_percent <= 0 or self.discount_percent > 100:
            raise ValidationError(
                "Discount percent must be between 0 and 100.")


class PosConfig(models.Model):
    _inherit = 'pos.config'

    discount_ids = fields.Many2many('pos.custom.discount')
    allow_custom_discount = fields.Boolean(
        'Allow Customize Discount', default=True)
    allow_security_pin = fields.Boolean('Allow Security Pin')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_discount_ids = fields.Many2many(
        related='pos_config_id.discount_ids', readonly=False)
    pos_allow_custom_discount = fields.Boolean(
        related='pos_config_id.allow_custom_discount', readonly=False)
    pos_allow_security_pin = fields.Boolean(
        related='pos_config_id.allow_security_pin', readonly=False)


class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        data = super()._load_pos_data_models(config_id)
        new_model_pos_custom_discount = 'pos.custom.discount'
        if new_model_pos_custom_discount not in data:
            data.append(new_model_pos_custom_discount)
        return data


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
    custom_discount_reason = fields.Text('Discount Reason')


    @api.model
    def _load_pos_data_fields(self, config_id):
        params = super()._load_pos_data_fields(config_id)
        params += ['custom_discount_reason']
        return params

