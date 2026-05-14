{
    "name": "Arabic/French Document Engine - POS",
    "summary": "Arabic/French rendering support for POS receipts",
    "version": "19.0.1.0.0",
    "category": "Point of Sale",
    "license": "LGPL-3",
    "author": "Arabic/French Document Engine Contributors",
    "website": "https://github.com/dalillali/Arabic-French-Document-Engine-for-Odoo",
    "depends": [
        "document_engine_arfr_core",
        "point_of_sale",
    ],
    "data": [
        "views/pos_config_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "document_engine_arfr_pos/static/src/app/arfr_format.js",
            "document_engine_arfr_pos/static/src/app/receipt/order_receipt_patch.js",
            "document_engine_arfr_pos/static/src/xml/order_receipt.xml",
            "document_engine_arfr_pos/static/src/scss/pos_receipt_rtl.scss",
        ],
        "web.assets_tests": [
            "document_engine_arfr_pos/static/tests/tours/**/*",
        ],
    },
    "installable": True,
    "application": False,
}
