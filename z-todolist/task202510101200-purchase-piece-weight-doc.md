# task202510101200-purchase-piece-weight-doc

## Original Request
目前有两类产品，一类是计件的，每件有每件的单价，一类是计重的，每个产品进货是按重量g来计量的，那么在采购环节，我应该如何具体操作，或者在产品基础主数据方面，该如何操作，需要详细说明步骤，补充到文档./doc/product_full_workflow_cn.md中。

## Improved English Phrasing
There are two product types: per-piece items with a unit price per piece, and by-weight items purchased by grams. How should I operate during purchasing, or how should I configure the product master data? Please provide detailed steps and add them to `./doc/product_full_workflow_cn.md`.

## Technical Analysis
- 查阅现有《产品库存全流程操作指南》，确认采购章节缺少计件/计重场景说明，需要在第2节中新增子章节。
- 结合 Odoo 产品表单字段，梳理计件产品与计重产品在主数据层面的差异：计量单位、供应商价目表、单位转换等。
- 规划采购订单流程说明，突出数量（件）与重量（克）在下单、收货、差异处理环节的具体操作。
- 设计文档结构为两个子章节：`2.1` 主数据配置、`2.2` 采购录入示例，保持与原文档风格一致并使用分步说明。

## Steps
- [x] 阅读现有采购流程章节，确认插入位置和文档语气
- [x] 梳理计件与计重产品在主数据配置时的字段与操作
- [x] 草拟采购订单操作步骤并写入文档
- [x] 校对新增内容的措辞与格式
- [x] 汇总变更并准备提交

## Files Changed
- `doc/product_full_workflow_cn.md`
- `z-todolist/_todolis.md`
- `z-todolist/task202510101200-purchase-piece-weight-doc.md`

## Apply / Verify
- 手动检查文档在 markdown 查看器中渲染，确认标题层级与列表缩进正常。

## Next
- 无，等待代码评审或进一步业务反馈。

## 详细技术分析过程（Detailed Technical Analysis Process）
1. 阅读用户需求，确认需在采购环节区分计件与计重两类产品，并写入指定文档。
2. 通读 `doc/product_full_workflow_cn.md`，确定第2节采购流程最贴合，计划新增子章节。
3. 列出主数据差异点（计量单位、供应商价目表、单位转换、类别区分），梳理为分步说明。
4. 汇总采购订单实际操作步骤，结合收货与差异处理，确保覆盖“录入、收货、差异、报表”四个方面。
5. 在文档中插入 `2.1`、`2.2` 两个小节，复核语句与 Markdown 缩进，避免与原章节冲突。

