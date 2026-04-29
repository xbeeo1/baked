/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    async addNewPaymentLine(paymentMethod) {

        const order = this.currentOrder;

        if (paymentMethod.fiscal_position_id) {

            // ✅ apply custom FP
            const fp = paymentMethod.fiscal_position_id;

            console.log("Auto FP Applied:", fp.name);

            order.set_fiscal_position
                ? order.set_fiscal_position(fp)
                : order.fiscal_position_id = fp;

        } else {

            // 🔥 IMPORTANT: reset to default
            console.log("No FP on method → Reset to default");

            if (order.set_fiscal_position) {
                order.set_fiscal_position(false);
            } else {
                order.fiscal_position_id = false;
            }
        }

        return await super.addNewPaymentLine(paymentMethod);
    },
});