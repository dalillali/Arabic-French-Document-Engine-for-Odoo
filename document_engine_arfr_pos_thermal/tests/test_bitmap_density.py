from io import BytesIO

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestThermalBitmapDensity(TransactionCase):
    def test_arabic_text_renders_non_empty_bitmap(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow is required for thermal bitmap tests")

        payload = self.env["arfr.pos.thermal.bitmap"].render_text_bitmap("خدمة استشارية")
        image = Image.open(BytesIO(payload)).convert("L")
        pixels = list(image.getdata())
        dark_pixels = sum(1 for pixel in pixels if pixel < 240)
        density = dark_pixels / len(pixels)

        self.assertGreater(density, 0.005)
        self.assertLess(density, 0.5)
