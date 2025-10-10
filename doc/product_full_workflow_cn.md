# Odoo 18 产品库存全流程操作指南

本指南面向使用 Odoo 18 企业版/社区版（中文界面）的业务人员，介绍从产品入库到销售、退货、盘点以及库存统计的完整操作流程。每个环节均给出所需模块、菜单路径以及关键表单字段说明，适用于标准单仓库场景。多仓库、多公司或高级路线配置可在此基础上扩展。

---

## 1. 前置准备

1. **安装模块（Install Modules）**（管理员 → `应用`）：
   - `库存（Inventory）`
   - `销售（Sales）`
   - `采购（Purchase）`（如需从供应商采购）
   - `会计（Accounting）`（若需记录发票/账务）
   - 可选：`计量单位（Units of Measure）`、`条码（Barcode）`、`质量（Quality）` 等扩展模块。
2. **启用多单位/批次等功能（Enable Advanced Inventory Features）**（`库存 → 配置 → 设置`）：
   - 勾选“多计量单位”以便选择不同单位。（Enable “Multi-Units of Measure” to allow multiple units.）
   - 如需批次/序列号管理，可启用“批次 & 序列号”。（Enable “Lots & Serial Numbers” if tracking is needed.）
   - 如需多步收货（收货→入库），可启用“高级路线”；本文按默认单步流程说明。（Enable “Advanced Routes” for multi-step receipts; this guide assumes the default single-step flow.）
3. **基础主数据（Prepare Master Data）**：
   - `库存 → 产品 → 创建`：维护产品名称、类型（库存产品/消耗品/服务）、默认计量单位、采购/销售计价等。（Maintain product basics under Inventory → Products → Create.）
   - `采购 → 供应商`、`销售 → 客户`：维护合作伙伴资料。（Maintain vendor and customer records under Purchase → Vendors and Sales → Customers.）

---

## 2. 采购入库流程（Receipt / PO）

**业务场景**：从供应商订货并收货入库。

1. **创建采购订单（Create Purchase Order）**
   1. 模块：`采购`。（Open the Purchase module.）
   2. 菜单：`采购 → 采购订单 → 创建`。（Navigate to Purchase → Purchase Orders → Create.）
   3. 在表单中：（Within the form:）
      - 选择供应商。（Select the vendor.）
      - 填写产品行（产品、数量、计量单位、单价、税率）。（Fill in product lines with product, quantity, unit of measure, unit price, and taxes.）
      - 保存并点击`确认订单`，系统生成待收货。（Save and click “Confirm Order” to create the receipt.）
2. **收货入库（Receive Products）**
   1. 从采购订单页面点击`收货`（或进入 `库存 → 操作 → 待办 → 收货`）。（Click “Receive Products” from the purchase order or go to Inventory → Operations → Transfers → Receipts.）
   2. 在收货单中：（On the receipt:）
      - 检查实际到货数量，可根据需要编辑`完成数量`。（Review the delivered quantities and adjust “Done” if needed.）
      - 如启用批次/序列号，在`详细操作`中填写对应编码。（Enter lot/serial numbers under “Detailed Operations” if tracking is enabled.）
      - 点击`验证`完成入库，库存数量更新。（Click “Validate” to post the receipt and update stock.）
3. **生成供应商账单（可选）（Create Vendor Bill - Optional）**
   1. 在采购订单页面点击`创建账单`。（Click “Create Bill” on the purchase order.）
   2. 检查账单内容后`确认`并`登记付款`。（Review, confirm, and register payment for the bill.）

**提示**：若仅需简单入库，可直接使用 `库存 → 操作 → 调拨 → 创建`，选择来源位置（供应商）与目标位置（库存），录入产品和数量后验证。

---

### 2.1 计件与计重产品的主数据配置（Master Data Setup for Unit-Based and Weight-Based Products）

**入口**：`库存 → 产品 → 产品`，点击“创建”或编辑现有产品。（Entry point: Inventory → Products → Products, then click Create or edit an existing product.）

1. **通用字段（Common Fields）**
   - `产品类型` 选择“库存产品”，以便系统记录库存数量。（Set Product Type to “Storable Product” to track stock.）
   - `产品类别` 建议区分“计件商品”“计重商品”两个类别，以便报表统计。（Use product categories to distinguish unit-based vs weight-based items for reporting.）
   - `路线` 根据业务需求启用“购买”，以允许从采购单补货。（Enable the “Buy” route if purchase replenishment is needed.）
2. **计件产品（按数量采购）（Unit-Based Products）**
   1. 在`常规信息`页签：（On the General Information tab:）
      - `计量单位` 选择“件/个”等数量单位。（Set Unit of Measure to pieces, such as Units.）
      - `采购计量单位` 保持一致（通常同样为“件”）。（Keep the Purchase UoM consistent, typically Units.）
      - `销售价格` 或 `成本` 填写每件价格。（Enter the per-unit sales price or cost.）
   2. 切换至`采购`页签：（Switch to the Purchase tab:）
      - 在`供应商列表`中添加供应商，`价格`填写“每件采购价”，`最小数量`填写1。（Add vendors with unit purchase prices and a minimum quantity of 1.）
      - 如同一产品存在不同包装（如箱），可通过 `其它` 页签 → `单位转换` 为外箱创建替换单位。（Use the Other tab → Unit of Measure to add alternative packaging such as boxes.）
3. **计重产品（按克采购）（Weight-Based Products）**
   1. **准备计量单位（Prepare Units of Measure）**：若列表中没有“克 (g)”，先到 `库存 → 配置 → 计量单位`，在“重量”类别下启用`克`，将`精度`设置为 0.01 或业务需要的最小刻度。（If Gram is not available, enable it under Inventory → Configuration → Units of Measure with the desired precision.）
   2. 在`常规信息`页签：（On the General Information tab:）
      - `计量单位` 选择“克 (g)”或业务常用重量单位；`采购计量单位` 默认跟随，可保持为“克”。（Set UoM and Purchase UoM to Gram or the appropriate weight unit.）
      - `销售价格`/`成本` 根据业务习惯填写“每克价格”，或留空并在采购时录入。（Enter per-gram sales price/cost or leave blank to fill during purchasing.）
      - 可在`库存`页签维护产品的`重量（公斤）`、`体积`等属性方便物流。（Optionally fill out weight and volume on the Inventory tab.）
   3. `采购`页签：（On the Purchase tab:）
      - 在`供应商列表`中为每个供应商设定“价格 = 每克采购价”，并可在描述中备注“到货需称重”。（Set vendor prices per gram and note weighing requirements.）
      - 如供应商按批次提供固定克数，可新增一条“供应商价格”并指定对应`最小数量`（例如500g）。（Add vendor price lines with minimum quantities for fixed-weight batches, e.g., 500 g.）
4. **附加建议（Additional Tips）**
   - 如需区分计件/计重字段，可在`内部参考`或`条码`中使用前缀（如 `PC-`、`WG-`）。（Use prefixes in Internal Reference or Barcode to distinguish product types.）
   - 若公司在销售端仍按件出售计重产品，可启用`多计量单位`，在`单位转换`里配置“1 件 = 50 g”等换算关系。（Enable multi-UoM and configure unit conversions, such as 1 Unit = 50 g, when selling by pieces.）

### 2.2 采购订单录入示例（计件 vs 计重）（PO Entry Examples for Unit vs Weight Products）

1. **创建采购订单（Create a Purchase Order）**（`采购 → 采购订单 → 创建`）：
   - 选择供应商后，在订单行添加产品。（Select a vendor and add products to the lines.）
   - 若是计件产品：（For unit-based items:）
     1. `数量` 填写件数（例如 10 件）。（Enter the quantity in pieces, such as 10 units.）
     2. `单位` 默认是“件”，`单价`自动带出“每件采购价”，可按需修改。（Keep the Unit as Units and adjust the price if needed.）
   - 若是计重产品：（For weight-based items:）
     1. `数量` 填写预计采购重量（例如 500 g）。可在下单时根据历史经验先填大致重量。（Enter the expected weight, e.g., 500 g.）
     2. `单位` 选择“克 (g)”或所设定的重量单位。（Select Gram or your defined weight unit.）
     3. `单价` 自动带出“每克采购价”；如按批次议价，可直接改为本次成交价。（Use the per-gram purchase price or overwrite with the negotiated batch price.）
     4. 如供应商按公斤计价，可在`单位`改为“千克”，系统会依据单位换算自动计算库存数量。（Switch the unit to Kilogram when vendors price per kg; Odoo converts automatically.）
2. **确认订单后收货（Receive After Confirmation）**：
   - 在收货单的`详细操作`中：（On the receipt’s detailed operations:）
     - 计件产品直接核对件数，无需额外操作。（Validate unit items directly; no extra steps required.）
     - 计重产品建议将实际称重结果录入`完成数量`（支持保留两位小数），以确保库存数量与实际重量一致。（Enter the weighed result into Done quantity to match stock with reality.）
     - 若存在重量损耗，可保留差异，系统会记录库存调整。（Keep any loss as a difference so Odoo logs an adjustment.）
3. **差异处理（Handle Variances）**：
   - 若采购订单上填写的是预计重量，实际收货重量不同：（If expected and actual weights differ:）
     1. 可以在收货时直接修改`完成数量`为实际重量，系统会根据修改后的数量生成会计/库存记录。（Edit the Done quantity to the actual weight so valuation stays correct.）
     2. 如需保留原单据与实际差异，可在收货后创建`退回`或新增一张补充采购单。（Create a return or supplemental PO to document the variance.）
4. **价格控制与报表（Price Control and Reporting）**：
   - 可在`采购 → 报表 → 采购分析`按产品类别过滤“计件商品”“计重商品”，比较不同计价方式的成本。（Use Purchase → Reporting → Purchase Analysis with category filters to compare costing methods.）
   - 若需要按照重量核算成本，请在产品类别中启用自动库存估值并指定正确的`库存账户`和`差异账户`。（Enable automated valuation and set proper Inventory and Difference accounts in the product category.）


## 3. 销售出库流程（Delivery / SO）

**业务场景**：向客户销售商品并发货。

1. **创建销售订单（Create Sales Order）**
   1. 模块：`销售`。（Open the Sales module.）
   2. 菜单：`销售 → 报价单 → 创建`。（Go to Sales → Quotations → Create.）
   3. 在表单中：（Within the form:）
      - 选择客户与有效期。（Select the customer and validity date.）
      - 添加产品行（产品、数量、售价、税金）。（Add product lines with quantities, prices, and taxes.）
      - 点击`确认`将报价转为销售订单，系统生成待出货单。（Click “Confirm” to create the delivery order.）
2. **交付发货（Deliver Products）**
   1. 在销售订单页面点击`发货`（或前往 `库存 → 操作 → 待办 → 发货`）。（Click “Deliver” from the sales order or open Inventory → Operations → Transfers → Delivery Orders.）
   2. 在发货单中：（On the delivery order:）
      - 核对`完成数量`是否与实际发货一致，可调整部分发货。（Check Done quantities and adjust for partial deliveries.）
      - 若启用批次/序列号，在`详细操作`中指定。（Assign lot/serial numbers under Detailed Operations if required.）
      - 点击`验证`执行出库，库存数量减少。（Click “Validate” to post the delivery and reduce stock.）
3. **开具客户发票（可选）（Create Customer Invoice - Optional）**
   1. 在销售订单点击`创建发票`。（Click “Create Invoice” from the sales order.）
   2. 选择发票类型（标准/退款/预付款），生成草稿发票。（Choose invoice type—regular, refund, or down payment—to draft the invoice.）
   3. 审批并`登记付款`。（Post the invoice and register payment.）

**POS 场景**：若通过POS售货，需在 `POS → 配置 → 销售点` 中设置库存和会计整合。POS确认的订单会生成交付单，可在 `库存 → 操作 → 转运单` 中查看。（For POS sales, configure inventory and accounting integration under POS → Configuration → Point of Sale; confirmed POS orders create delivery orders in Inventory → Operations → Transfers.）

---

## 4. 退货流程（Return）

退货分为两类：客户退货（销售退货）与供应商退货（采购退货）。

### 4.1 客户退货（Customer Returns）

1. 进入原销售订单或交付单。（Open the original sales order or delivery order.）
2. 在交付单上点击`退回`。（Click “Return” on the delivery order.）
3. 在弹窗中填写退货数量、退回位置（默认退回到库存）。（Enter quantities and select the return location, defaulting to Stock.）
4. 点击`退回`生成逆向调拨。（Click “Return” to create the reverse transfer.）
5. 打开生成的退货单，核对后点击`验证`完成入库。（Open the return transfer, review, and click “Validate” to receive back.）
6. 如需退款，在原销售订单点击`创建发票`并选择`退款发票`，或在会计模块开具贷项通知单。（Create a credit note from the sales order or Accounting if a refund is needed.）

### 4.2 供应商退货（Vendor Returns）

1. 打开原采购订单的收货单。（Open the original PO receipt.）
2. 点击`退回`。（Click “Return”.）
3. 填写退货数量，确认目标位置为供应商。（Enter quantities and ensure the destination is the Vendor location.）
4. `退回`后打开退货单并`验证`，库存扣减。（Open the return transfer and validate it to reduce stock.）
5. 在采购订单中可创建`退款账单`处理财务。（Create a refund bill from the purchase order to settle finances.）

**注意**：如退货货物需送往质检或损坏仓，可在退货单中修改目标存放库位。（Adjust the destination location on the return if goods go to QC or Scrap.）

---

## 5. 库存盘点与调整

### 5.1 快速盘点（即时调整）（Quick Inventory Adjustment）

1. 模块：`库存`。（Open the Inventory module.）
2. 菜单：`库存 → 操作 → 库存调整`。（Go to Inventory → Operations → Inventory Adjustments.）
3. 在列表中点击`新建`或选择现有盘点计划。（Click “New” or open an existing adjustment.）
4. 设置范围（库存地点、产品、批次等），点击`开始盘点`。（Define scope—location, products, lots—and click “Start Inventory”.）
5. 在盘点表中输入实际数量：（Enter the counted quantities:）
   - `理论数量`为系统当前数量。（Theoretical Quantity shows the system count.）
   - 在`实际数量`列填写实盘结果。（Fill Actual Quantity with the physical count.）
6. 点击`验证`生成库存调整单，系统自动记录差异。（Click “Validate” to post the adjustment and record variances.）

### 5.2 循环盘点/多库位盘点（Cycle Counting / Multi-Location Inventory）

1. 可在库存设置中启用`库存盘点计划`或使用`条码`模块扫描盘点。（Enable Inventory Count Plans or use the Barcode app for scanning.）
2. 进入 `库存 → 配置 → 库存盘点计划` 创建周期任务，指派员工并设定频率。（Go to Inventory → Configuration → Inventory Count Plans to schedule cycles and assign users.）

---

## 6. 库存统计与报表（Inventory Reporting）

1. **库存概览**：`库存 → 仓库 → 仓库看板`，查看收货、发货、延迟订单等卡片。（View the warehouse dashboard for receipts, deliveries, and delays.）
2. **当前库存（Current Inventory）**：
   - `库存 → 报表 → 库存估值`：按产品、地点、批次查看数量与金额。（Use Inventory → Reporting → Inventory Valuation for quantities and value by product/location/lot.）
   - `库存 → 报表 → 仓位库存`：查看各库位存量。（Use Inventory → Reporting → Location Stock for on-hand per location.）
3. **移动分析（Moves Analysis）**：`库存 → 报表 → 库存移动`，过滤特定日期、产品、合作伙伴。（Analyze moves via Inventory → Reporting → Stock Moves with filters.）
4. **销售/采购分析（Sales / Purchase Analytics）**：
   - `销售 → 报表 → 销售分析`：按产品/客户查看销量、收入。（Go to Sales → Reporting → Sales Analysis for product and customer performance.）
   - `采购 → 报表 → 采购分析`：按供应商/产品统计采购情况。（Use Purchase → Reporting → Purchase Analysis for vendor and product spend.）
5. **退货追踪**：在库存移动或销售/采购报表中按`操作类型`过滤`退货`。（Filter by Operation Type = Return in stock or sales/purchase reports to trace returns.）
6. **自定义报表**：使用`数据透视`或`图表`视图添加维度（日期、产品类别、仓库）。（Use Pivot or Graph views to add dimensions like date, category, or warehouse.）

---

## 7. 常见问题与建议（FAQs and Recommendations）

- **权限控制**：确保相关用户被分配到合适的安全组，如`库存/用户`、`采购/经理`、`销售/经理`等，以访问对应菜单。（Assign the proper security groups so users can reach the menus they need.）
- **多步骤仓库**：如需收货→质检→入库等流程，可在`库存 → 配置 → 仓库`中编辑仓库，将`收货`流程改为两步或三步，并按新流程执行调拨。（Edit the warehouse configuration to switch to two-step or three-step receipts when QC is required.）
- **自动化流程**：（Automation Tips:）
  - 可在销售订单上启用`自动确认采购`，由 MTO 或补货规则驱动。（Enable automatic PO confirmation via MTO or reordering rules.）
  - 在`库存 → 配置 → 补货规则`设置最小/最大库存，实现自动草拟采购单。（Configure reorder rules to draft POs automatically.）
- **盘点差异会计处理**：启用了自动估值的产品，库存调整会生成会计分录；确认相关科目（库存科目、盘盈盘亏科目）已在产品类别中配置。（When automated valuation is on, inventory adjustments create journal entries; ensure accounts are set on the product category.）
- **报表导出**：所有列表视图支持`导出`（右上角⚙️ → 导出），可勾选字段输出为 Excel。（Use the Export option in list views to download data to Excel.）

---

通过以上步骤，可以在 Odoo 18 中完成产品的入库、销售、退货、盘点和库存分析等标准流程。如需更复杂的场景（委外加工、多公司、多仓库、序列追踪等），建议在对应模块中进一步配置路线与规则。
