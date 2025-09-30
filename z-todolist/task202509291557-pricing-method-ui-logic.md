# task202509291557-pricing-method-ui-logic

Summary
- Implement conditional product form UI: 'By Unit' vs 'By Weight'. Force Unit of Measure accordingly and allow editing weight in grams.

Assumptions & Environment
- Odoo 18.0; DB `odoo`; addons path includes `addons_custom`.
- `pos_gold_pricing` provides gold price; POS behavior not changed in this patch.

Changes
- Model (`addons_custom/product_weight_pricing/models/product_template.py`):
  - Rename selection values to 'By Unit' / 'By Weight'.
  - Add `weight_g` (grams) with compute/inverse mapping to native `weight` (kg).
  - Onchange: set `uom_id` and `uom_po_id` to Unit(s) when By Unit, to Gram when By Weight (fallback to Kg if Gram missing).
- View (`addons_custom/product_weight_pricing/views/product_template_views.xml`):
  - Hide any pre-existing `uom_id`/`weight` fields from other modules to prevent duplicates.
  - Show `list_price` only when 'By Unit'.
  - Insert `pos_pricing_method` selector.
  - Add 'By Unit' row: label 'per' + read-only `uom_id` (Unit).
  - Add 'By Weight' row: label 'Weight:' + `weight_g` + 'per' + read-only `uom_id` (g).

Verify
- Update module:
  `python odoo-bin -c odoo.conf -u product_weight_pricing`
- Open Product form:
  - Select 'By Unit' → shows Sales Price and "per Unit"; UoM is Unit and read-only.
  - Select 'By Weight' → shows Weight (g) and "per g"; UoM is g and read-only.

Notes
- If `uom.product_uom_gram` is unavailable, the onchange falls back to Kg.
- Existing `pos_gold_pricing` view that adds `uom_id`/`weight` is hidden to avoid duplicates; our fields replace it.
- POS pricing calculation integration remains out of scope; this only exposes UI and data.
