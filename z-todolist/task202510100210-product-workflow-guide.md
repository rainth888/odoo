# task202510100210-product-workflow-guide

## Original Request
odoo18，我需要有一个产品全流程的详细操作说明，入库、销售、退货、盘点、库存统计的全流程操作说明，需要step by step的讲解，包括模块、菜单选项操作等。

## Improved English Phrasing
Provide a step-by-step Odoo 18 guide that covers the full product inventory workflow: receiving goods into stock, selling products, processing returns, performing inventory counts, and reviewing inventory reports. Include the relevant modules, menu paths, and key configuration notes for each stage.

## Technical Analysis
- 需求重点是梳理 Odoo 18 标准功能下的产品生命周期，从采购入库、销售、退货到库存盘点与统计。
- 需要明确每一步操作涉及的模块（如库存、采购、销售、会计）及在界面中的菜单路径。
- 文档最好按照业务流程顺序编排，并区分后台（库存/销售等模块）和前端（如 POS 或门户）操作。
- 由于用户未要求自定义开发，说明应基于标准界面，适量提示必要的前提设置（例如启用多步仓库操作、启用退货权限等）。
- 产出形式可为 Markdown 文档，便于引用菜单、按钮名称，并能嵌套步骤列表。

## Steps
- [x] 研究 Odoo 18 中产品全流程涉及的模块与关键菜单。
- [x] 编写分章节的操作指南，覆盖入库、销售、退货、盘点、库存统计，逐步说明。
- [x] 自检内容的完整性与顺序合理性，确保术语准确。
- [x] 更新任务清单与总结至 todolist 并准备最终答复。

## Files Changed
- `doc/product_full_workflow_cn.md`
- `z-todolist/_todolis.md`
- `z-todolist/task202510100210-product-workflow-guide.md`

## Apply / Verify
- 无需运行代码；手动校对流程与菜单路径。

## Next
- 若用户需要具体界面截图或不同部署模式（多公司、多仓库）差异，可在后续任务中补充。

## Work Summary / 变更说明
- 编写《Odoo 18 产品库存全流程操作指南》，涵盖模块安装、采购入库、销售出库、退货、盘点及库存报表操作。
- 更新 `z-todolist/_todolis.md` 勾选任务进度，并在本任务文档记录执行过程。

## 详细技术分析过程（Detailed Technical Analysis Process）
1. 回顾 Odoo 标准库存与销售模块的典型操作流程。
2. 列举各阶段所需配置（产品、供应商、客户、仓库、库存设置）。
3. 整理每一阶段的操作步骤，并确保采用中文界面常见菜单命名，必要时标注英文名称。
4. 计划在 `doc/` 目录下创建新的中文操作手册，涵盖所有流程环节。
