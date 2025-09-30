# task202509291630-use-pos-gold-pricing

Summary
- Explain how to use `pos_gold_pricing` to set daily metal prices and have POS compute price per lot by weight.

Key Points
- Set daily price via menu: Point of Sale → Metal Pricing → Daily Metal Prices.
- Each record: Company, Metal Type, Price per gram, Fineness factor, Effective date.
- POS integration via JS asset (uncomment in manifest) triggers server RPC on lot entry.

Steps
1) Install/upgrade module `pos_gold_pricing`.
2) Create/update daily price(s): menu “Daily Metal Prices”. One per day/metal/company (unique constraint).
3) Prepare products/lots:
   - Product: enable Tracking by Lots, optional default metal type.
   - Lot: set net_gold_weight (g), metal_type, wage_type/value, etc.
4) Enable POS frontend asset:
   - In `addons_custom/pos_gold_pricing/__manifest__.py`, uncomment `point_of_sale._assets_pos` with `static/src/js/pos_gold_pricing.js`.
   - Upgrade module and hard-reload POS UI.
5) Use in POS:
   - Add a tracked item, enter/scan Lot number.
   - JS calls `stock.lot.pos_compute_price_by_lot` to compute price.

Behavior Details
- Price formula: net_gold_weight × daily price_per_g × fineness_factor + wage (per g or per piece).
- Daily lookup picks latest record with `effective_date` <= today.
- Mid-day change: update today’s record value (or create another record with same date — latest date still applies since time isn’t stored).

Verification
- Example: 50g, price 600, factor 1.0, wage per g = 2 → 50×600 + 50×2 = 30,100.

Follow-ups
- Ensure Gram UoM exists (`uom.product_uom_gram`) or fallback shows kg.
- Optionally gate POS logic by product’s `Pricing Method` if needed.
