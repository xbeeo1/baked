/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline, {
    extraFields: {
        ...(PosOrderline.extraFields || {}),
        selected_list_discount: {
            model: "pos.order.line",
            name: "selected_list_discount",
            relation: "pos.custom.discount",
            type: "many2one",
            local: true,
        },
        custom_discount: {
            model: "pos.order.line",
            name: "custom_discount",
            type: "boolean",
            local: true,
        },
        list_discount: {
            model: "pos.order.line",
            name: "list_discount",
            type: "boolean",
            local: true,
        },
    }
})
patch(PosOrderline.prototype, {
    setup(vals) {
        var self = this;
        super.setup(...arguments);
        console.log('self.selected_list_discount',self.selected_list_discount)
        console.log('self.custom_discount_reason',self.custom_discount_reason)
        self.custom_discount = self.custom_discount || '';
        self.custom_discount_reason = self.custom_discount_reason || '';
        self.list_discount = self.list_discount || false;
        self.selected_list_discount = self.selected_list_discount || false;
        self.discount = self.discount || 0;
    },

    get_custom_discount_reason() {
        return this.custom_discount_reason || '';
    },
});