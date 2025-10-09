# task202510090623-pos-by-weight-price-display

## Original Request
'By Weight'类型的产品计价，应该是当日该产品属性对应的金价乘以该产品的重量。
一个Product，条形码是0520000699，在Product下的General Information选项卡下，Sales Price下设置'By Weight'，下面填写的是125 g，在 Attributes & Variants选项卡下的Attribute是'成色'和对应的Values是'足金'。
Metal Pricing菜单下Daily Metal Prices中，有一个Name是'足金'，对应的Metal Type是'足金'，对应的Price (CNY/gram)是512.000。
现在，在pos店铺里，选中0520000699产品后，在价格栏显示的内容是是'0.00x￥880/g', 而我希望是'￥512/g x 125 g'，显示价格是￥64000.00。

## Improved English Phrasing
For "By Weight" pricing, the POS should multiply the product's configured weight by the current metal price of the matching attribute value. Product 0520000699 is set to "By Weight" with 125 g and has the attribute value "足金". In Daily Metal Prices, "足金" costs ¥512 per gram. When selecting the product in the POS, the price ribbon currently shows "0.00 x ￥880/g". It should instead display "￥512/g x 125 g" with a total of ￥64,000.00.

## Technical Analysis
- Investigate how the POS frontend currently renders price details for By Weight products supplied by the `product_weight_pricing` and `pos_gold_pricing` modules.
- Determine why the POS is picking a ￥880/g rate (likely hard-coded default) instead of using the matching Daily Metal Price for attribute value "足金".
- Ensure that the POS orderline uses the product's configured weight and fetched metal rate when computing subtotal and display strings.

## Steps
- [x] Inspect backend models to confirm weight and attribute configuration for the product.
- [x] Trace the POS data loading to verify metal price information sent to the frontend.
- [x] Adjust POS price computation/display logic to reference the correct metal rate and product weight.
- [ ] Test in POS to confirm the display reads "￥512/g x 125 g" and totals ￥64,000.00.
- [x] Document verification steps and any remaining questions.

## Files Changed
- `addons_custom/product_weight_pricing/models/product_product.py`
- `addons_custom/product_weight_pricing/static/src/js/pos_pricing_method.js`
- `z-todolist/_todolis.md`

## Apply / Verify
- ✅ `python3 -m compileall addons_custom/product_weight_pricing`
- ☐ POS manual check once frontend assets are rebuilt/reloaded.

## Next
- [ ] Reload POS (update module + hard refresh) to validate UI output once environment is available.
- [ ] Capture screenshots in POS after verification if required.

## Detailed Technical Analysis Process
- Reviewed `pos_gold_pricing` and `product_weight_pricing` models to understand how POS pulls metal pricing and weight metadata.
- Identified that `pos_compute_price_by_weight` always fell back to the legacy `default_metal_type`/`au_9999` when template defaults were missing, so attribute-based metal selections (e.g., "成色" → "足金") never influenced the lookup.
- Implemented attribute-derived metal type resolution by parsing the variant's `product_template_attribute_value_ids`, prioritising tokens from "成色"/"金种" style attributes and matching them against `metal.type` records.
- Updated the POS orderline patch to rely on the server-provided gram price for display, ensuring the label renders as "￥<price>/g x <weight> g" with proper spacing and currency formatting.
- Ran `python3 -m compileall addons_custom/product_weight_pricing` to catch syntax issues in the modified Python module.

## Work Summary
- Added metal type detection from product attribute values so weight-based products fetch the correct daily price (`足金` → ¥512/g).
- Refined POS orderline display logic to show the gram price multiplied by the configured weight with clearer formatting.

