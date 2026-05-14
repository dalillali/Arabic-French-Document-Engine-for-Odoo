"""Tests for bundled report font assets."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "addons" / "document_engine_arfr_core"
FONTS = CORE / "static" / "src" / "fonts" / "noto"
MANIFEST = ast.literal_eval((CORE / "__manifest__.py").read_text(encoding="utf-8"))


def test_noto_font_files_are_bundled():
    for font_file in (
        "NotoNaskhArabic-Regular.ttf",
        "NotoNaskhArabic-Bold.ttf",
        "NotoSans-Regular.ttf",
        "NotoSans-Bold.ttf",
    ):
        path = FONTS / font_file
        assert path.exists(), font_file
        assert path.stat().st_size > 100_000, font_file


def test_font_license_is_bundled():
    license_text = (FONTS / "OFL.txt").read_text(encoding="utf-8")
    assert "SIL OPEN FONT LICENSE" in license_text


def test_report_font_scss_is_registered():
    assets = MANIFEST["assets"]["web.report_assets_common"]
    assert "document_engine_arfr_core/static/src/scss/report_fonts.scss" in assets


def test_report_font_scss_references_bundled_fonts():
    scss = (CORE / "static" / "src" / "scss" / "report_fonts.scss").read_text(
        encoding="utf-8"
    )
    for font_file in (
        "NotoNaskhArabic-Regular.ttf",
        "NotoNaskhArabic-Bold.ttf",
        "NotoSans-Regular.ttf",
        "NotoSans-Bold.ttf",
    ):
        assert font_file in scss


if __name__ == "__main__":
    test_noto_font_files_are_bundled()
    test_font_license_is_bundled()
    test_report_font_scss_is_registered()
    test_report_font_scss_references_bundled_fonts()
