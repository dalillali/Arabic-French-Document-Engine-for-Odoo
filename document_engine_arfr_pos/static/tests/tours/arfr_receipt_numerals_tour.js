import { registry } from "@web/core/registry";
import * as Dialog from "@point_of_sale/../tests/generic_helpers/dialog_util";
import { waitForLoading } from "@point_of_sale/../tests/pos/tours/utils/common";
import * as Chrome from "@point_of_sale/../tests/pos/tours/utils/chrome_util";
import * as ProductScreen from "@point_of_sale/../tests/pos/tours/utils/product_screen_util";
import * as PaymentScreen from "@point_of_sale/../tests/pos/tours/utils/payment_screen_util";
import * as ReceiptScreen from "@point_of_sale/../tests/pos/tours/utils/receipt_screen_util";

registry.category("web_tour.tours").add("arfr_pos_receipt_arabic_indic_digits", {
    steps: () =>
        [
            waitForLoading(),
            Chrome.startPoS(),
            Dialog.confirm("Open Register"),
            ProductScreen.clickDisplayedProduct("Desk Organizer", true, "1"),
            ProductScreen.clickPayButton(),
            PaymentScreen.clickPaymentMethod("Cash", true),
            ProductScreen.finishOrder(),
            ReceiptScreen.isShown(),
            {
                content: "receipt total uses Arabic-Indic digits",
                trigger: ".receipt-screen .pos-receipt.arfr-pos-receipt .arfr-money:contains('١')",
            },
        ].flat(),
});

