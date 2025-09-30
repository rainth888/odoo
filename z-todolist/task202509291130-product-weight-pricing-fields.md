# task202509291130-product-weight-pricing-fields

## Summary
Show “Weight” and “Unit of Measure” in the Product General Information, and add a “Pricing Method” choice: “By Unit Price” or “By Weight × Gold Price”. Do not change POS behavior yet; pos_gold_pricing only supplies gold price.

## Original Request
The addons_custom module 'pos_gold_pricing' is just supply the gold price, it needn't do other thing.
The 'weight' and the 'Unit of Measure' property should be shown in the 'General Information' of the Products, then some product can be fill the weight and unit of measure as weight.
the gold product has two properties in price, one is weight multiplied by gold price, the other is unit price bultiplied by number. these two properties should show when I add new products.

## Improved English Phrasing
- Show “Unit of Measure” and “Weight” on Product “General Information”.
- Add a Product “Pricing Method” with two options:
  - By Unit Price (price × quantity)
  - By Weight × Gold Price (weight × today’s gold price)
- Do not modify POS logic now; pos_gold_pricing only provides the daily price.

## Technical Analysis
- Decoupling: keep price method classification in product; wire POS later as an opt‑in module.
- Data model: add `pos_pricing_method` on `product.template` with default “by_unit”.
- UI placement: insert next to `list_price`, with UoM and Weight, via XPath on product form. Provide fallback inherit id for compatibility.
- No side effects on accounting/stock; purely UI + metadata so far.
- Future integration: POS extension reads `pos_pricing_method` and applies pricing rule; gold price fetched from `pos_gold_pricing`.

## Steps
- [x] Improve English phrasing and define scope
- [x] Expose Weight and Unit of Measure under Product General Information (already added)
- [x] Add a new Product field “pos_pricing_method” with options: by_unit / by_weight_gold
- [x] Add a view to place “Pricing Method” alongside List Price, Weight, UoM
- [ ] Keep POS logic unchanged; document future integration path
- [ ] Verify in UI (create product) and note update steps

## Files Changed
- addons_custom/product_weight_pricing/__manifest__.py
- addons_custom/product_weight_pricing/__init__.py
- addons_custom/product_weight_pricing/models/__init__.py
- addons_custom/product_weight_pricing/models/product_template.py
- addons_custom/product_weight_pricing/views/product_template_views.xml

## Apply / Verify
- WSL:
  - `cd /mnt/d/_projects/odoo.github.rainth888 && source .venv/bin/activate`
  - `python odoo-bin -c odoo.conf -u product_weight_pricing`
- Open Products > Create: you should see Unit of Measure, Weight, and Pricing Method on General Information.

## Next
- When ready, implement POS pricing integration as a separate, opt-in step using the gold price from `pos_gold_pricing`.
