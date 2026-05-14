from io import BytesIO
from pathlib import Path

from odoo import api, modules, models


class ArfrPosThermalBitmap(models.AbstractModel):
    _name = "arfr.pos.thermal.bitmap"
    _description = "AR/FR POS Thermal Bitmap Renderer"

    @api.model
    def _font_path(self):
        return Path(modules.get_module_resource(
            "document_engine_arfr_core",
            "static/src/fonts/noto/NotoNaskhArabic-Regular.ttf",
        ))

    @api.model
    def _has_raqm(self, ImageFont):
        features = getattr(ImageFont, "features", None)
        return bool(features and features.check("raqm"))

    @api.model
    def _fallback_rtl_text(self, text):
        return "\n".join(line[::-1] for line in (text or "").splitlines())

    @api.model
    def render_text_bitmap(self, text, width=576, font_size=28):
        from PIL import Image, ImageDraw, ImageFont

        font = ImageFont.truetype(str(self._font_path()), font_size)
        image = Image.new("L", (width, max(120, font_size * 4)), 255)
        draw = ImageDraw.Draw(image)
        if self._has_raqm(ImageFont):
            draw.multiline_text((width - 8, 8), text or "", font=font, fill=0, spacing=4, direction="rtl", anchor="ra")
        else:
            draw.multiline_text((8, 8), self._fallback_rtl_text(text), font=font, fill=0, spacing=4)
        output = BytesIO()
        image.save(output, format="PNG")
        return output.getvalue()
