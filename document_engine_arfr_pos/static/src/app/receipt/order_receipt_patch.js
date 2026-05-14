/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { arfrFormatAmount } from "@document_engine_arfr_pos/app/arfr_format";

patch(OrderReceipt.prototype, {
    get arfrCurrentOrder() {
        return this.order || this.props?.order || this.props?.data?.order;
    },

    get arfrReceiptEnabled() {
        return Boolean(this.arfrReceiptPreferences.enabled);
    },

    get arfrReceiptPreferences() {
        return this.arfrCurrentOrder?.config?.arfr_resolved_receipt_preferences || {};
    },

    get arfrReceiptClass() {
        if (!this.arfrReceiptEnabled) {
            return "";
        }
        return "arfr-pos-receipt";
    },

    get arfrReceiptDirection() {
        const direction = this.arfrReceiptPreferences.layout_direction;
        if (!this.arfrReceiptEnabled || !direction || direction === "company" || direction === "auto") {
            return "";
        }
        return direction === "force_rtl" ? "rtl" : "ltr";
    },

    arfrFormatAmount(amount) {
        if (!this.arfrReceiptEnabled) {
            return this.formatCurrency(amount);
        }
        return arfrFormatAmount(amount, this.arfrCurrentOrder.currency, this.arfrReceiptPreferences);
    },
});
