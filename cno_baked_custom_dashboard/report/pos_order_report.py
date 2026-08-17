# -*- coding: utf-8 -*-

from functools import partial

from odoo import models, fields, api


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

    @api.model
    def get_top_vendors(self, date_from=False, date_to=False, limit=10):

        where = """
            pt.vendor_id IS NOT NULL
            AND po.state IN ('paid', 'done', 'invoiced')
        """

        params = []

        if date_from:
            where += " AND po.date_order >= %s"
            params.append(date_from)

        if date_to:
            # Next day tak le ja rahe hain taake To Date poori include ho
            where += " AND po.date_order < (%s::date + INTERVAL '1 day')"
            params.append(date_to)

        params.append(limit)

        query = f"""
            SELECT
                pt.vendor_id AS vendor_id,
                rp.name AS vendor_name,
                SUM(pol.qty) AS quantity,
                SUM(pol.price_subtotal_incl) AS revenue
            FROM pos_order_line pol
            JOIN pos_order po
                ON po.id = pol.order_id
            JOIN product_product pp
                ON pp.id = pol.product_id
            JOIN product_template pt
                ON pt.id = pp.product_tmpl_id
            JOIN res_partner rp
                ON rp.id = pt.vendor_id

            WHERE {where}

            GROUP BY
                pt.vendor_id,
                rp.name

            ORDER BY revenue DESC
            LIMIT %s
        """

        self.env.cr.execute(query, params)

        return self.env.cr.dictfetchall()
