# task202509301030-by-weight-selected-item-style

Summary
- POS selected item (orderline) for By Weight products should match the style expectation: no "per g"; display a single line: `Weight: 10.00 g`.

Assumptions & Notes
- Using heuristic: UoM name for grams is `g` (Odoo default). If this DB uses a customized name, we may adjust the condition.
- Keep default layout for non-gram units.
- No backend model changes required; purely a POS template override.

Changes
- Added POS QWeb override: `addons_custom/product_weight_pricing/static/src/xml/pos_weight_orderline.xml` to replace the `price-per-unit` line when unit is `g`.
- Updated module manifest to include assets so the override loads in POS:
  - `addons_custom/product_weight_pricing/__manifest__.py` -> `assets["point_of_sale.assets"]`.

Commands Executed
- N/A (code-level patch only).

Verification Steps
1) Update module and restart POS:
   - `python odoo-bin -c odoo.conf -u product_weight_pricing`
2) Reload the POS web client (hard refresh) to fetch new assets.
3) Add/select a By Weight product (with UoM set to grams) in the order:
   - The second line of the selected orderline must read: `Weight: <qty> g`.
   - There should be no `x ... / g` segment.
4) Confirm non-gram products still render the default line with `x <unit price> / <unit>`.

Follow-ups
- If the UoM label is not exactly `g`, adjust the template condition or expose a more explicit flag via model data to the POS.
- Optionally localize the `Weight:` label (use translatable string if needed).

