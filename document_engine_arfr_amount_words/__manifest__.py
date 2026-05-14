{
    "name": "Arabic/French Document Engine - Amount in Words",
    "summary": "Optional bilingual amount-in-words blocks",
    "version": "19.0.1.2.0",
    "category": "Accounting/Localizations",
    "license": "LGPL-3",
    "author": "Arabic/French Document Engine Contributors",
    "depends": ["document_engine_arfr_core", "document_engine_arfr_account"],
    "external_dependencies": {"python": ["num2words"]},
    "data": [
        "report/amount_words_templates.xml",
    ],
    "installable": True,
    "application": False,
}
