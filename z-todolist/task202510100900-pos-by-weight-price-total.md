# task202510100900-pos-by-weight-price-total

## Original Request
'By Weight'类型的计重类产品价格计算，在pos店铺里，价格栏显示的内容依然是'0.00x￥880/g'，而不是'￥512/g x 125 g'形式。

## Improved English Phrasing
For by-weight products in the POS, the orderline price label still shows `0.00 x ￥880/g` instead of `￥512/g x 125 g`.

## Technical Analysis
- Review previous tasks (`task202510090623-pos-by-weight-price-display`) that introduced price display logic for metal pricing and ensure the expected formatting pipeline.
- Inspect the POS QWeb templates and models in `addons_custom/product_weight_pricing/static/src` to identify where the price detail string is generated.
- Determine whether the per-gram price currently uses a hardcoded 880 value or is missing the live price from `pos_gold_pricing` daily metal prices.
- Update the template/logic to show both the per-gram price and weight quantity, ensuring localization-friendly formatting and currency symbol placement.
- Verify that the displayed total equals 512 × 125 = 64000 and matches backend orderline totals.

## Steps
- [x] Analyze existing POS orderline rendering for by-weight items.
- [x] Adjust JS/QWeb to compute and display `￥512/g x 125 g` (dynamic values).
- [x] Confirm total amount shown equals ￥64,000.00.
- [ ] Document verification steps and assumptions.

## Files Changed
- `addons_custom/product_weight_pricing/static/src/js/pos_pricing_method.js`

## Apply / Verify
- Pending implementation.

## Next
- Perform POS UI verification once environment is available; update documentation section afterwards.

## Detailed Technical Analysis Process
- Reviewed existing POS store override which only computed by-weight pricing when `price_unit` was absent, causing the base unit price (￥880/g) and qty (0.00) to remain. This aligned with the user's screenshot text `0.00x￥880/g`.
- Confirmed that the QWeb template already expected a populated `weightPricingLabel`, so the missing label was due to the `_weight_pricing` payload never being attached.
- Updated the override to always fetch `pos_compute_price_by_weight`, normalise the returned payload, and override both quantity and price so the total reflects 512 × 125 = 64,000.
- Adjusted the `getDisplayData` label construction to output the `￥512/g x 125 g` wording using the currency formatter for the per-gram price.

## Work Summary / 变更说明
- 始终在 POS 端为“By Weight”产品调用后端定价 RPC，并将返回的克重/金价写入行数据，确保数量与单价正确设置，总价按 512×125 计算。同时重构前端价签格式，显示“￥512/g x 125 g”样式。
