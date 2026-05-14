# PDF/A-3 Roadmap

`document_engine_arfr_pdfa` is not shipped in v1.1.0. A valid implementation
must pass veraPDF against generated invoices and prove all of the following:

- PDF/A-3b XMP metadata is present.
- The catalog marks the PDF/A conformance level.
- An sRGB ICC OutputIntent is embedded.
- Required fonts are embedded or subset.
- Saudi UBL XML from `l10n_sa_edi` is attached as an associated file with
  `/AFRelationship /Source`.

Until that validator-backed work lands, the addon remains `installable=False`.
