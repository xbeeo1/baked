# -*- coding: utf-8 -*-

from odoo import models, api


class PnlDashboard(models.Model):
    _name = 'pnl.dashboard'
    _description = 'P&L Dashboard Data Provider'

    @api.model
    def _get_pnl_report(self):
        """Locate the standard Profit and Loss report.

        Tries the standard external ID first, then falls back to
        searching by name.
        """

        report = self.env.ref(
            'account_reports.profit_and_loss',
            raise_if_not_found=False
        )

        if not report:
            report = self.env['account.report'].search(
                [('name', 'ilike', 'profit and loss')],
                limit=1
            )

        if not report:
            report = self.env['account.report'].search(
                [('name', 'ilike', 'profit')],
                limit=1
            )

        return report

    @api.model
    def get_pnl_data(
        self,
        date_from=None,
        date_to=None,
        company_id=None
    ):
        """Return Profit & Loss data for the dashboard."""

        # ---------------------------------------------------------
        # 1. Get Profit & Loss root report
        # ---------------------------------------------------------
        report = self._get_pnl_report()

        if not report:
            return {
                'error': (
                    'Profit and Loss report not found. '
                    'Please check that the Accounting Reports '
                    'module is installed.'
                ),
                'lines': [],
                'company': self.env.company.name,
                'currency': self.env.company.currency_id.symbol,
            }

        # ---------------------------------------------------------
        # 2. Get company
        # ---------------------------------------------------------
        company = (
            self.env['res.company'].browse(company_id)
            if company_id
            else self.env.company
        )

        # Make sure company record is valid
        if not company.exists():
            company = self.env.company

        # ---------------------------------------------------------
        # 3. Prepare report options
        # ---------------------------------------------------------
        options = report.get_options({
            'date': {
                'date_from': date_from,
                'date_to': date_to,
                'filter': 'custom',
                'mode': 'range',
            },
        })

        selected_report_id = options.get('report_id')

        if selected_report_id:
            selected_report = self.env['account.report'].browse(
                selected_report_id
            )

            if selected_report.exists():
                report = selected_report

        # ---------------------------------------------------------
        # 5. Get report lines
        # ---------------------------------------------------------
        lines = report._get_lines(options)

        # ---------------------------------------------------------
        # 6. Convert Odoo report lines into dashboard data
        # ---------------------------------------------------------
        result = []

        for line in lines:

            columns = []

            for col in line.get('columns', []):
                columns.append({
                    'name': col.get('name'),
                    'no_format': col.get('no_format'),
                })

            result.append({
                'id': line.get('id'),
                'name': line.get('name'),
                'level': line.get('level', 0),
                'columns': columns,

                'is_total': (
                    'total' in (line.get('class') or '')
                ),

                'unfoldable': line.get(
                    'unfoldable',
                    False
                ),
            })

        # ---------------------------------------------------------
        # 7. Return dashboard response
        # ---------------------------------------------------------
        return {
            'lines': result,
            'company': company.name,
            'currency': company.currency_id.symbol,
        }