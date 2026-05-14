# Golden Fixture Regeneration

Regenerate these fixtures only from a clean Odoo 19 database with
`document_engine_arfr_core`, `document_engine_arfr_account`, and
`document_engine_arfr_pos` installed. The generator exercises
`ir.actions.report._render_qweb_pdf()`, extracts text with `pdfminer.six`,
normalizes it with the same whitespace and current-year filtering used by
`test_golden_snapshots.py`, and writes perceptual hashes through
`pdf2image` plus `imagehash`.

Example:

```bash
docker cp addons/. odoo19-web:/mnt/extra-addons/arfr
docker exec -u root odoo19-web bash -lc "chown -R odoo:odoo /mnt/extra-addons/arfr"
docker exec -u root odoo19-web bash -lc "apt-get update && apt-get install -y poppler-utils"
docker exec -u root odoo19-web bash -lc "python3 -m pip install --break-system-packages pdfminer.six pdf2image imagehash"
docker exec odoo19-web bash -lc "odoo -d arfr_golden_v11 --without-demo=True -i document_engine_arfr_core,document_engine_arfr_account,document_engine_arfr_pos --stop-after-init"
docker cp scripts/regenerate_golden_fixtures.py odoo19-web:/tmp/regenerate_golden_fixtures.py
docker exec odoo19-web bash -lc "odoo shell -d arfr_golden_v11 --no-http < /tmp/regenerate_golden_fixtures.py"
docker cp odoo19-web:/mnt/extra-addons/arfr/document_engine_arfr_account/tests/fixtures/golden/. addons/document_engine_arfr_account/tests/fixtures/golden
```

Review text diffs and phash changes before committing. A changed fixture means
the rendered document content or layout changed, even when the template edit
looked cosmetic.
