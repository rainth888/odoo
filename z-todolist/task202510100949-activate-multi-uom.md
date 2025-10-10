# task202510100949-activate-multi-uom

## Original Request
如何'库存设置中启用“多计量单位”'

## Improved English Phrasing
How do I enable the "Multi-Unit of Measure" option in the Inventory settings?

## Technical Analysis
The feature is part of Odoo's Inventory module. Activating it requires Inventory module access and the correct user permissions. Once enabled, it allows products to have alternative units of measure and operations. The setting lives under Inventory ‣ Configuration ‣ Settings in the Units of Measure section.

## Steps
1. 打开库存应用（Inventory）。
2. 进入“配置 → 设置”（Configuration ‣ Settings）。
3. 在“产品”（Products）或“单位”相关的小节中找到“多计量单位”（Multi-Unit of Measure）。
4. 勾选“多计量单位”选项后保存设置。
5. 保存后，检查产品表单确认新增的“计量单位”和“采购计量单位”等字段可用。

## Files Changed
- `z-todolist/_todolis.md`
- `z-todolist/task202510100949-activate-multi-uom.md`

## Apply / Verify
- 启用后，在任意产品表单的“常规信息”页面查看“计量单位”、“采购计量单位”字段是否出现。
- 在库存应用中创建或编辑一条操作记录（如采购订单），确认可以选择不同单位。

## Next
- 如需使用自定义单位，前往“库存 → 配置 → 计量单位”创建或启用所需单位。

## Detailed Technical Analysis Process
1. 识别需求：用户希望知道如何启用库存设置中的“多计量单位”功能。
2. 查阅 Odoo 界面结构：该功能属于库存应用配置项，位于设置页面。
3. 整理启用步骤与验证方式，确保用户按照界面即可操作，无需代码。

## Work Summary / 变更说明
- 归纳了在库存设置中启用“多计量单位”的详细步骤和验证方式。
