"""Validate addon manifest metadata without requiring an Odoo database."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ADDONS = ROOT / "addons"

EXPECTED_DEPENDENCIES = {
    "document_engine_arfr_core": {"base", "web"},
    "document_engine_arfr_account": {
        "document_engine_arfr_core",
        "account",
        "sale",
        "purchase",
        "stock",
    },
    "document_engine_arfr_pos": {"document_engine_arfr_core", "point_of_sale"},
    "document_engine_arfr_l10n_gcc": {
        "document_engine_arfr_account",
        "l10n_gcc_invoice",
    },
    "document_engine_arfr_l10n_sa": {
        "document_engine_arfr_l10n_gcc",
        "l10n_sa",
        "l10n_sa_edi",
    },
    "document_engine_arfr_l10n_ae": {"document_engine_arfr_l10n_gcc", "l10n_ae"},
    "document_engine_arfr_l10n_eg": {
        "document_engine_arfr_account",
        "l10n_eg",
        "l10n_eg_edi_eta",
    },
    "document_engine_arfr_l10n_ma": {"document_engine_arfr_account", "l10n_ma"},
    "document_engine_arfr_l10n_gcc_pos": {
        "document_engine_arfr_pos",
        "l10n_gcc_pos",
    },
}


def _manifest(addon: str) -> dict:
    manifest_path = ADDONS / addon / "__manifest__.py"
    return ast.literal_eval(manifest_path.read_text(encoding="utf-8"))


def test_all_planned_addons_have_manifests():
    for addon in EXPECTED_DEPENDENCIES:
        assert (ADDONS / addon / "__manifest__.py").exists(), addon


def test_manifests_declare_lgpl3():
    for addon in EXPECTED_DEPENDENCIES:
        assert _manifest(addon)["license"] == "LGPL-3", addon


def test_manifests_declare_explicit_dependencies():
    for addon, expected in EXPECTED_DEPENDENCIES.items():
        assert set(_manifest(addon)["depends"]) == expected, addon


if __name__ == "__main__":
    test_all_planned_addons_have_manifests()
    test_manifests_declare_lgpl3()
    test_manifests_declare_explicit_dependencies()
