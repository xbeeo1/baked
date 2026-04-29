import base64
import io
import os
from odoo import models
from datetime import timedelta
from odoo.exceptions import UserError

dirname = os.path.dirname(__file__)


class SaleAnalysisXlsx(models.AbstractModel):
    _name = 'report.cno_baked_report.sale_analysis_report_id_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, report):
        sheet = workbook.add_worksheet('Sale Analysis Report')
        center = workbook.add_format({'align': 'center'})
        center_left = workbook.add_format({'align': 'left'})
        center_right = workbook.add_format({'align': 'right'})
        bold = workbook.add_format({'bold': True, 'align': 'center'})
        bold_left = workbook.add_format({'bold': True, 'align': 'left'})
        bold_right = workbook.add_format({'bold': True, 'align': 'right'})
        date_style_1 = workbook.add_format(
            {'text_wrap': True, 'num_format': 'dd-mm-yyyy', 'align': 'center', 'font_size': 10, 'bold': True, })
        date_style = workbook.add_format(
            {'num_format': 'dd-mm-yyyy', 'align': 'center', })
        format3_colored = workbook.add_format(
            {'align': 'center', 'bg_color': '#87CEEB', 'bold': True, 'font_color': 'white'})
        format3_colored_left = workbook.add_format(
            {'align': 'left', 'bg_color': '#87CEEB', 'bold': True, 'font_color': 'white'})
        format3_colored_right = workbook.add_format(
            {'align': 'right', 'bg_color': '#87CEEB', 'bold': True, 'font_color': 'white'})

        res_company = self.env.user.company_id
        sheet.set_column('A:V', 20)

        r = 1
        co = 0
        row = 3

        # Formatting the date from and to
        f_date = ((report.date_from) + timedelta(hours=5)).strftime("%d-%m-%Y %H:%M:%S")
        t_date = ((report.date_to) + timedelta(hours=5)).strftime("%d-%m-%Y %H:%M:%S")



        sheet.merge_range(r, co, r, co + 6, 'Sale Analysis Report', bold)
        r += 1
        sheet.merge_range(r, co, r, co + 6, f'Date From:  {f_date}  Date To:  {t_date}', date_style_1)

        # Query pos.orders within the specified date range
        pos_orders = self.env['pos.order'].search([
            ('date_order', '>=', report.date_from),
            ('date_order', '<=', report.date_to) # Filter paid orders (optional)
        ])

        if not pos_orders:
            raise UserError("No POS orders found in the specified date range.")

        # Column headers for the report
        r += 2
        sheet.write(row, 0, 'Date', format3_colored)
        sheet.write(row, 1, 'Time', format3_colored)
        sheet.write(row, 2, 'Receipt Number', format3_colored)
        sheet.write(row, 3, 'Receipt Type', format3_colored)
        sheet.write(row, 4, 'Vendor', format3_colored)
        sheet.write(row, 5, 'Stream', format3_colored)
        sheet.write(row, 6, 'Brands', format3_colored)
        sheet.write(row, 7, 'SKU', format3_colored)
        sheet.write(row, 8, 'Item', format3_colored)
        sheet.write(row, 9, 'Quantity', format3_colored)
        sheet.write(row, 10, 'Gross sales', format3_colored)
        sheet.write(row, 11, 'Discounts', format3_colored)
        sheet.write(row, 12, 'Net sales', format3_colored)
        sheet.write(row, 13, 'Cost of goods', format3_colored)
        sheet.write(row, 14, 'Gross profit', format3_colored)
        sheet.write(row, 15, 'Taxes', format3_colored)
        sheet.write(row, 16, 'MOP', format3_colored)
        sheet.write(row, 17, 'POS', format3_colored)
        sheet.write(row, 18, 'Store', format3_colored)
        sheet.write(row, 19, 'Cashier Name', format3_colored)
        sheet.write(row, 20, 'Customer Name', format3_colored)
        sheet.write(row, 21, 'Customer Contacts', format3_colored)
        row += 1

        # Loop through the pos orders and display the corresponding order lines
        for order in pos_orders:
            payment_methods = []
            # Loop through the payment methods and collect their names
            for pay in order.payment_ids:
                mop = pay.payment_method_id.name
                payment_methods.append(mop)  # Add the payment method name to the list
            # Join the payment method names with a comma separator
            payment_methods_str = ', '.join(payment_methods)

            for line in order.lines:
                date = ((order.date_order) + timedelta(hours=5)).strftime("%d-%m-%Y")
                time = ((order.date_order) + timedelta(hours=5)).strftime("%H:%M")
                vendor_name = line.product_id.vendor_id.name if line.product_id.vendor_id else ''
                customer_name = order.partner_id.name if order.partner_id else ''
                customer_contact = order.partner_id.phone if order.partner_id else ''
                receipt_type = 'Refund' if order.amount_total < 0 else 'Sale'
                dic = (line.discount * line.price_subtotal)/100
                net_sale = line.price_subtotal - dic
                cost_goods = line.qty * line.product_id.standard_price
                gross_pro = net_sale - cost_goods
                taxes = line.price_subtotal_incl - line.price_subtotal
                sheet.write(row, 0, date, center_left)
                sheet.write(row, 1, time, center_left)
                sheet.write(row, 2, order.name, center_left)
                sheet.write(row, 3, receipt_type, center_left)
                sheet.write(row, 4, vendor_name, center_left)
                sheet.write(row, 5, line.product_id.stream, center_left)
                sheet.write(row, 6, line.product_id.brand, center_left)
                sheet.write(row, 7, line.product_id.default_code, center_left)
                sheet.write(row, 8, line.product_id.name, center_left)
                sheet.write(row, 9, line.qty, center_right)
                sheet.write(row, 10, line.price_subtotal, center_right)
                sheet.write(row, 11, dic, center_right)
                sheet.write(row, 12, net_sale, center_right)
                sheet.write(row, 13, cost_goods, center_right)
                sheet.write(row, 14, gross_pro, center_right)
                sheet.write(row, 15, taxes, center_right)
                sheet.write(row, 16, payment_methods_str, center_left)
                sheet.write(row, 17, order.session_id.name, center_left)
                sheet.write(row, 18, order.session_id.config_id.name, center_left)
                sheet.write(row, 19, order.user_id.name, center_left)
                sheet.write(row, 20, customer_name, center_left)
                sheet.write(row, 21, customer_contact, center_left)
                row += 1