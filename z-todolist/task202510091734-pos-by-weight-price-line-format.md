# task202510091734-pos-by-weight-price-line-format

## Original Request
测试了一下，前面的问题并没有修复成功，继续修复。
'By Weight'类型的计重类产品价格计算，在pos店铺里，价格栏显示的内容依然是'1.00x￥880/g'，而不是'￥512/g x 125 g'形式。
请查看页面截图./logs/2025-10-09_173404_674.png

## Improved English Phrasing
The previous fix did not work. In the POS, a "By Weight" product still shows the price line as "1.00x￥880/g" instead of the expected "￥512/g x 125 g". See screenshot in `logs/2025-10-09_173404_674.png`.

## Technical Analysis
- 结合截图描述与现有实现，确认 POS 行项目依旧沿用默认的 `qty x unitPrice/unit` 模板，说明我们新增的 `weightPricingLabel` 未生效。
- 检查 `addons_custom/product_weight_pricing/static/src/js/pos_pricing_method.js`，发现 `_weight_pricing` 数据仅在成功 RPC 后写入，且展示字符串对单位/数量做了严格判断，导致任一字段缺失就会回退到原模板。
- 进一步排查 `addLineToOrder` 的补丁，若 RPC 失败或金价数据缺失，则 `vals.qty`、`vals.price_unit` 仍保留默认值（1 × ￥880），从而复现用户所见结果。
- 需要在 POS 端补全权重信息的兜底逻辑，并改进展示字符串格式以输出 “￥512/g x 125 g” 样式，包含去除尾随 0、小数。

## Steps
- 查看截图和现有实现，确认问题重现
- 复核 POS 前端模板/逻辑，定位为何仍显示旧格式
- 调整代码以展示“￥512/g x 125 g”格式
- 确保总价显示与 512 × 125 一致
- 在 POS 中复测并记录验证结果

## Files Changed
- `addons_custom/product_weight_pricing/static/src/js/pos_pricing_method.js`

## Apply / Verify
- （待验证）更新模块并在 POS 前端加载 By Weight 产品，确认单价/重量标签显示为“￥512/g x 125 g”，且总价 64,000.00。

## Next
- 等待用户提供 POS 前端复测截图或在可用环境中亲自复测，并视需要进一步微调字符串格式。

## 详细技术分析过程（Detailed Technical Analysis Process）
- 阅读 `pos_pricing_method.js` 现有补丁，确认 `_weight_pricing` 仅在 RPC 成功时填充；若调用异常会直接落回 Odoo 默认逻辑。
- 追加 `trimDecimalZeros` 工具函数，确保货币/数量格式化后移除尾随 `.00` 或 `,00`。
- 在 `addLineToOrder` 中：
  - 持续调用 `pos_compute_price_by_weight`，若成功则缓存重量、单价、克价及单位标签，并在缺失克价时回退至单价；
  - 无论 RPC 成功与否，都为 By Weight 商品构造 `_weight_pricing` 兜底数据，并强制数量采用克重，避免继续显示 1.00。
- 在 `getDisplayData` 中：
  - 统一使用 `_weight_pricing`（或 `this.qty`）计算克重字符串，并通过 `trimDecimalZeros` 去掉多余小数；
  - 优先显示返回的克价，若缺失则回退到当前单价，最终输出“货币/单位 x 数量 单位”；
  - 覆盖 `data.qty` 与 `data.unit`，确保模板中其他位置也能看到正确克重/单位。

