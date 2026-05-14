"""Saudi visible invoice coexistence checks."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[3]
SA = ROOT / "addons" / "document_engine_arfr_l10n_sa"


def test_saudi_addon_declares_edi_dependencies_and_template():
    manifest = (SA / "__manifest__.py").read_text(encoding="utf-8")
    assert '"l10n_sa"' in manifest
    assert '"l10n_sa_edi"' in manifest
    assert "saudi_invoice_templates.xml" in manifest


def test_saudi_template_only_adds_visible_presentation_hooks():
    path = SA / "report" / "saudi_invoice_templates.xml"
    ET.parse(path)
    xml = path.read_text(encoding="utf-8")
    assert 'inherit_id="account.report_invoice_document"' in xml
    assert "arfr-zatca-visible" in xml
    forbidden = ["_l10n_sa", "ubl", "clearance", "qr_code_method", "edi"]
    lowered = xml.lower()
    for token in forbidden:
        assert token not in lowered


if __name__ == "__main__":
    test_saudi_addon_declares_edi_dependencies_and_template()
    test_saudi_template_only_adds_visible_presentation_hooks()
