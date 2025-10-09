# task202510090602-pos-default-metal-field

## Original Request
localhost:8069 显示  
加载销售点时发生错误Invalid field 'default metal type' on model 'product.template

## Improved English Phrasing
When loading the POS interface at localhost:8069 an error appears: "Invalid field 'default metal type' on model 'product.template'."

## Technical Analysis
The POS load failure is raised while building the product dataset: the custom
module `product_weight_pricing` extends `_load_pos_data_fields` on
`product.template` and requests an extra field named `default_metal_type`. The
`pos_gold_pricing` module recently replaced that selection field with the
Many2one `default_metal_type_id`, so the former column no longer exists on the
model and the POS loader aborts.

The price computation RPC (`pos_compute_price_by_weight`) still expects to read
`default_metal_type` as a string code when calling `metal.pricelist.get_price`.
It needs to accept the new Many2one and fall back to legacy data to stay
compatible with databases that still have the old field populated.

## Steps
- [x] 分析 POS 加载流程中对 `default_metal_type` 字段的引用来源
- [x] 修正后端模型/视图，确保 `product.template` 上存在字段或不再请求该字段
- [ ] 更新受影响的模块并在 POS 中复测加载
- [ ] 记录验证步骤与结果

## Files Changed
- `addons_custom/product_weight_pricing/models/product_template.py`
- `addons_custom/product_weight_pricing/models/product_product.py`

## Apply / Verify
- 更新模块：`python odoo-bin -c odoo.conf -u product_weight_pricing pos_gold_pricing`
- 重启服务后重新加载 POS，确认不再出现 "Invalid field 'default metal type'" 报错
- 在 POS 中选择 By Weight 产品，确认自动定价仍然根据金种金价计算

## Next
- 若需要向前兼容旧数据库，可考虑在迁移脚本中同步将旧的字符串字段映射为新的 Many2one

## Detailed Technical Analysis Process

1. 重现日志中 POS 加载失败栈，定位在 `_load_pos_data_fields` 中请求了不存在的字段。
2. 检查 `pos_gold_pricing` 的模型定义，确认字段已迁移为 Many2one
   `default_metal_type_id`。
3. 更新 `product_weight_pricing` 以请求新的字段名，并在价格计算时支持新的
   Many2one（向下兼容旧字段值）。
4. 记录待验证步骤，准备通过模块更新验证。

## Work Summary / 变更说明
- 修复 `product_weight_pricing` POS 数据字段列表，匹配 `pos_gold_pricing`
  的字段迁移。
- 更新 POS 重量定价计算逻辑，兼容 Many2one 金种配置并保留旧字段兜底。
