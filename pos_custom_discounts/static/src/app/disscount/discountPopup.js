/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { useState, onMounted, Component } from "@odoo/owl";
import { NumberPopup } from "@point_of_sale/app/components/popups/number_popup/number_popup";
import { _t } from "@web/core/l10n/translation";
import { WkCustomDiscountPopup } from "@pos_custom_discounts/app/disscount/CoustomDiscountPoupop";
import { Dialog } from "@web/core/dialog/dialog";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

export class WkDiscountPopup extends Component {
    static template = "WkDiscountPopup";
    static components = { Dialog };

    setup() {
        super.setup();
        this.pos = usePos();
        this.state = useState({ value: this.props.value });
        onMounted(this.onMounted);
    }
    onMounted() {
        var wk_discount_list = this.pos.all_discounts;
        this.wk_discount_percentage = 0;
        this.selected_discount = false;
        $(".button.apply").show();
        $(".button.apply_complete_order").show();
        $("#discount_error").hide();
        if (wk_discount_list && !wk_discount_list.length) {
            $(".button.apply_complete_order").hide();
            $(".button.apply").hide();
        }
        if (this.props.selected_list_discount) {
            $(".wk_popup_body span.discount_percent[id=" + this.props.selected_list_discount.id + "]").click()
        }
    }
    async wk_ask_password(password) {
        var self = this;
        var ret = new $.Deferred();
        if (password) {
            await this.pos.dialog.add(NumberPopup, {
                title: _t("Password?"),
                startingValue: undefined,
                getPayload: async  (num) => {
                    if (password !== Sha1.hash(num)) {
                        this.pos.dialog.add(AlertDialog, {
                            title: _t("Incorrect Password"),
                            body: _t(
                                "Please try again."
                            ),
                        });
                        return false;
                    }
                    await self.pos.dialog.add(WkCustomDiscountPopup);
                },
            });
        } else {
            ret.resolve();
        }
        return ret;
    }
    async click_customize() {
        var self = this;
        let employee = self.pos.getCashier();
        if (self.pos.config.allow_security_pin && employee && employee._pin) {
                self.props.close();
                await self.wk_ask_password(employee._pin);
        }
        else {
            self.props.close();
            this.pos.dialog.add(WkCustomDiscountPopup);
        }

    }
    click_wk_product_discount(event) {
        $("#discount_error").hide();
        $(".wk_product_discount").css('background', 'white');
        var discount_id = parseInt($(event.currentTarget).attr('id'));
        $(event.currentTarget).css('background', '#6EC89B');
        var wk_discount_list = this.pos.all_discounts;
        for (var i = 0; i < wk_discount_list.length; i++) {
            if (wk_discount_list[i].id == discount_id) {
                var wk_discount = wk_discount_list[i];
                this.wk_discount_percentage = wk_discount.discount_percent;
                this.selected_discount = wk_discount;
            }
        }
    }
    async click_remove_discount() {
        let order = this.pos.getOrder();
        let selected_orderline = order.getSelectedOrderline();
        selected_orderline.setDiscount(0);
        selected_orderline.update({'list_discount': false})
        selected_orderline.selected_list_discount = false;
        selected_orderline.update({'custom_discount_reason': ""});
        if (order._updateRewards) {
            order._updateRewards();
        }
        this.props.close();
    }
    click_apply(event) {
        var order = this.pos.getOrder();
        let selected_orderline = order.getSelectedOrderline();
        if (this.wk_discount_percentage != 0) {
            selected_orderline.setDiscount(this.wk_discount_percentage);
            selected_orderline.update({'custom_discount_reason': this.selected_discount.name || ""});
            selected_orderline.update({'custom_discount': false});
            selected_orderline.update({'list_discount': true});
            selected_orderline.update({'selected_list_discount': this.selected_discount});
            $('ul.orderlines li.selected div#custom_discount_reason').text('');

            if (order._updateRewards) {
                order._updateRewards();
            }
            this.props.close();
        } else {
            $(".wk_product_discount").css("background-color", "burlywood");
            setTimeout(function () {
                $(".wk_product_discount").css("background-color", "");
            }, 100);
            setTimeout(function () {
                $(".wk_product_discount").css("background-color", "burlywood");
            }, 200);
            setTimeout(function () {
                $(".wk_product_discount").css("background-color", "");
            }, 300);
            setTimeout(function () {
                $(".wk_product_discount").css("background-color", "burlywood");
            }, 400);
            setTimeout(function () {
                $(".wk_product_discount").css("background-color", "");
            }, 500);
            return;
        }
    }
    click_apply_complete_order(event) {
        var order = this.pos.getOrder();
        if (this.wk_discount_percentage != 0) {
            var orderline_ids = order.getOrderlines();
            for (var i = 0; i < orderline_ids.length; i++) {
                orderline_ids[i].update({'custom_discount': false});
                orderline_ids[i].update({'custom_discount_reason': this.selected_discount.name || ""});
                orderline_ids[i].setDiscount(this.wk_discount_percentage);
                orderline_ids[i].update({'list_discount': true})
                orderline_ids[i].update({'selected_list_discount': this.selected_discount});
            }
            if (order._updateRewards) {
                order._updateRewards();
            }
            this.props.close();
        } else {
            $(".wk_product_discount").css("background-color", "burlywood");
            setTimeout(function () {
                $(".wk_product_discount").css("background-color", "");
            }, 100);
            setTimeout(function () {
                $(".wk_product_discount").css("background-color", "burlywood");
            }, 200);
            setTimeout(function () {
                $(".wk_product_discount").css("background-color", "");
            }, 300);
            setTimeout(function () {
                $(".wk_product_discount").css("background-color", "burlywood");
            }, 400);
            setTimeout(function () {
                $(".wk_product_discount").css("background-color", "");
            }, 500);
            return;
        }
    }
    cancel() {
        this.props.close();
    }

}

