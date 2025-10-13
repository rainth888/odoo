# To-Do List

## task202509270946-todolist-rule-update

Original Request
> 后续开发任务处理规则重大更新：
> 我在项目中，创建了一个文件夹'z-todolist'，里面的主要文件是_todolis.md，每次我发布任务后，你首先要增加一个任务项'task202509270946-**'，其中'**'为任务的大致内容，需要你总结精简这个名称，然后，先把我的需求原文列出来，然后，理解需求后，分解为工作任务，把工作任务细化为列表清单，然后按照列表清单每一次独立执行，每一个列表项，最前面，都需要有方框[]，空方框表示未完任务，[x]方框表示完成任务。列完任务后，就可以逐个执行，直至任务完成。
> 除了在文档_todolis.md中列出所有任务外，还需要生成一个和任务名称对应的任务执行文件，文件命名为'task202509270946-**.md',需要把完成这个任务的所有工作内容，都写入这个文件夹，做工作任务流程备忘。
> 将上面这个规则写入AGENTS.md，后续所有工作内容，都需要严格执行。

Checklist
- [x] Summarize task slug as `todolist-rule-update`
- [x] Add rules to `AGENTS.md` under “Task Workflow (z-todolist)”
- [x] Create folder and scaffold `z-todolist/_todolis.md`
- [x] Create execution log `z-todolist/task202509270946-todolist-rule-update.md`
- [x] Notify user and confirm future adherence

## task202509271015-cancel-lot-serial-popup

Original Request
> there should be cancel the input box 'Lot/Serial Number(s) Requiredd' in the shop when select a product.
> tell me how to do it.

Checklist
- [x] Clarify goal and constraints (no POS breakage)
- [x] Provide POS configuration method (disable Lots/Serial Numbers on POS)
- [x] Provide product-level method (set Tracking to No tracking)
- [x] Provide safe operational workaround (POS-only duplicate product)
- [x] Provide optional customization outline (skip popup in POS UI)
- [x] Provide verification steps and WSL path notes

## task202509291015-gold-price-weight-uom

Original Request
> It has only sales price property in the 'General Information' of the Products, It can be set the unit and g.
> But I need a 'weight' and 'Unit of Measure' property in the 'General Information' of the Products when I add a new product.
> and the sales price in the Pos is calculate by weight (such 50g) multiplied by gold price today from the addons_custom module 'pos_gold_pricing'.

Checklist
- [x] Clarify English phrasing and scope
- [x] Expose Weight and Unit of Measure on Product General Information via view inheritance
- [x] Technical analysis written
- [ ] Document how POS price-by-weight integrates with pos_gold_pricing
- [ ] Propose safe implementation plan for POS frontend without breaking assets
- [ ] Optionally scaffold JS hook guarded behind config flag (on request)
- [ ] Verify in UI and note WSL path and update steps

## task202509291130-product-weight-pricing-fields

Original Request
> The addons_custom module 'pos_gold_pricing' is just supply the gold price, it needn't do other thing.
> The 'weight' and the 'Unit of Measure' property should be shown in the 'General Information' of the Products, then some product can be fill the weight and unit of measure as weight.
> the gold product has two properties in price, one is weight multiplied by gold price, the other is unit price bultiplied by number. these two properties should show when I add new products.

Checklist
- [x] Improve English phrasing and define scope
- [x] Expose Weight and Unit of Measure on Product General Information
- [x] Add a Product field “Pricing Method” with options: By Unit Price / By Weight × Gold Price
- [x] Add views to display these fields under General Information
- [x] Technical analysis written
- [ ] Leave POS behavior unchanged; document future integration using pos_gold_pricing for price lookup
- [ ] Verify fields appear when creating a new product; note update steps (WSL)

## task202509291557-pricing-method-ui-logic

Original Request
> I can see the changing in the 'General Information', but I need the item is: 'By Unit' or 'By Weight'. It should be shown the 'Sales Price', 'per' 'unit of measure', always the 'unit of measure' is unit, when user select the 'By Unit'. It should be shown the 'Weight:', 'xx', 'per' 'unit of measure', the 'xx' is value of the weight, always the 'unit of measure' is g, when user select the 'By Weight'.

Checklist
- [x] Rename selection options to 'By Unit' / 'By Weight'
- [x] Add `weight_g` field (compute/inverse) to edit grams safely
- [x] Add onchange to force `uom_id`/`uom_po_id` to Unit or g
- [x] Update product form to show conditional blocks with labels 'per', 'Weight:'
- [x] Hide duplicate base/other-module `uom_id`/`weight` fields to avoid clutter
- [ ] Verify in UI and adjust labels/readonly as needed
- [ ] Document commands to update module and test

## task202509291630-use-pos-gold-pricing

Original Request
> How can I use the module 'pos_gold_pricing', I think I can set it each day or any time.

Checklist
- [x] Review module models/views and menus
- [x] Provide daily workflow to set metal price
- [x] Explain lot fields and price formula
- [x] Explain POS integration steps (enable assets, reload POS)
- [x] Document per-day behavior and mid-day updates
- [ ] Optional: add data to ensure Gram UoM exists

## task202509291841-two-line-sales-price-block

Original Request
> in 'Sales Price' item, the 'By Unit' should be 2 lines, the 2nd line is 'Weight: nnn.nn per g'. delete other charactor.

Checklist
- [x] Clarify phrasing and desired two-line rule
- [x] Hide native Sales Price field
- [x] Always show line 2 as "Weight: <value> per g"
- [x] Keep line 1 as By Unit / By Weight selector
- [ ] Verify layout renders as exactly two lines in Sales Price section

## task202509300920-weight-line-with-uom

Original Request
> the 'By Weight' selected item, change the 'per g ' to 'g' (should be 'unit of measure'), then the second line of the the 'By Weight' just like 'Weight: 10.00 g'. Please improve the English phrasing first, then perform the tasks.

Checklist
- [x] Improve phrasing of the requirement
- [x] Remove literal "per" from By Weight second line
- [x] Keep UoM field inline and read-only to display the unit
- [ ] Verify the second line renders as "Weight: <value> <uom>"

## task202509301030-by-weight-selected-item-style

Original Request
> the 'By Weight' selected item, should conference the 'By Unit' selected item style. no 'per g'. just like 'Weight: 10.00 g' in one line.

Checklist
- [x] Identify POS orderline template that renders the selected item details
- [x] Implement QWeb override to show "Weight: <qty> g" for gram-based items
- [x] Register the override in `product_weight_pricing` POS assets
- [ ] Update module and reload POS to verify UI
- [ ] Adjust condition if UoM name differs from 'g' in this DB
- [ ] Document update/verification steps (WSL path, `-u` command)

## task202509301055-remove-g-and-per-on-product-form

Original Request
> Now， I can see the page show each line as below:
> Sales Price By Weight
> 23,000.00  g
> per g
> delete the character 'g' on the second line, delete the character 'per' on the 3rd line.

Checklist
- [x] Remove inline UoM field next to weight to drop trailing 'g'
- [x] Hide Sales Price container (`list_price_uom`) and its label when By Weight
- [ ] Update module and verify UI shows only numeric weight and no "per g"

## task202510100949-activate-multi-uom

Original Request
> 如何'库存设置中启用“多计量单位”'

Checklist
- [x] 解读需求并确认是在库存设置中启用多计量单位功能
- [x] 整理启用多计量单位的界面步骤
- [x] 给出验证启用结果的方法

## task202509300922-bus-serialize-error-on-reload

Original Request
> Server reload logs show: psycopg2.errors.SerializationFailure: could not serialize access due to concurrent update (bus_presence) during websocket terminate.

Checklist
- [x] Explain error is transient during concurrent presence update
- [x] Confirm no data loss; safe to ignore if sporadic
- [x] Suggest mitigation: full server restart, hard refresh POS
- [x] Suggest monitoring; if frequent, adjust workers/reload flow
- [ ] Optional: add retry wrapper in custom bus hook (if needed)

## task202509291557-fix-product-view-inherit-id

Original Request
> Installing `product_weight_pricing` fails with: `ValueError: External ID not found in the system: product.product_template_only_form` while parsing `addons_custom/product_weight_pricing/views/product_template_views.xml`.

Checklist
- [x] Reproduce install error and capture stack trace
- [x] Locate offending `inherit_id` reference in XML
- [x] Replace missing `product.product_template_only_form` with `product.product_template_form_view`
- [x] Remove duplicate fallback to avoid unresolved refs
- [x] Run module update to validate load
- [x] Apply same fix to `pos_gold_pricing` (optional, on request)

## task202510090602-pos-default-metal-field

Original Request
> localhost:8069 显示
> 加载销售点时发生错误Invalid field 'default metal type' on model 'product.template

Checklist
- [x] 分析 POS 加载流程中对 `default_metal_type` 字段的引用来源
- [x] 修正后端模型/视图，确保 `product.template` 上存在字段或不再请求该字段
- [ ] 更新受影响的模块并在 POS 中复测加载
- [ ] 记录验证步骤与结果

## task202510090623-pos-by-weight-price-display

Original Request
> 'By Weight'类型的产品计价，应该是当日该产品属性对应的金价乘以该产品的重量。
> 一个Product，条形码是0520000699，在Product下的General Information选项卡下，Sales Price下设置'By Weight'，下面填写的是125 g，在 Attributes & Variants选项卡下的Attribute是'成色'和对应的Values是'足金'。
> Metal Pricing菜单下Daily Metal Prices中，有一个Name是'足金'，对应的Metal Type是'足金'，对应的Price (CNY/gram)是512.000。
> 现在，在pos店铺里，选中0520000699产品后，在价格栏显示的内容是是'0.00x￥880/g', 而我希望是'￥512/g x 125 g'，显示价格是￥64000.00。

Checklist
- [x] Review current POS orderline price display for By Weight items
- [x] Ensure metal price lookup uses attribute value's daily price (512 CNY/g)
- [x] Update POS display to show "￥512/g x 125 g" for barcode 0520000699
- [ ] Confirm computed total shows ￥64,000.00
- [x] Document verification steps and any configuration assumptions

## task202510100210-product-workflow-guide

Original Request
> odoo18，我需要有一个产品全流程的详细操作说明，入库、销售、退货、盘点、库存统计的全流程操作说明，需要step by step的讲解，包括模块、菜单选项操作等。

Checklist
- [x] 理解产品全流程涉及的模块与主要菜单
- [x] 编写包含入库、销售、退货、盘点、库存统计的逐步操作说明
- [x] 复核操作步骤确保逻辑连贯、无遗漏
- [x] 在任务日志中记录分析、步骤与总结

## task202510100900-pos-by-weight-price-total

Original Request
> 'By Weight'类型的计重类产品价格计算，在pos店铺里，价格栏显示的内容依然是'0.00x￥880/g'，而不是'￥512/g x 125 g'形式。

Checklist
- [x] 复用上一任务的分析，确认当前实现仍显示旧格式
- [x] 更新 POS 价签模板以使用每克金价和重量信息
- [x] 确保总价按 512 CNY/g × 125 g 计算并展示
- [ ] 在 POS 前端验证新显示格式
- [ ] 记录验证步骤与配置假设

## task202510091734-pos-by-weight-price-line-format

Original Request
> 测试了一下，前面的问题并没有修复成功，继续修复。
> 'By Weight'类型的计重类产品价格计算，在pos店铺里，价格栏显示的内容依然是'1.00x￥880/g'，而不是'￥512/g x 125 g'形式。
> 请查看页面截图./logs/2025-10-09_173404_674.png

Checklist
- [x] 查看截图和现有实现，确认问题重现
- [x] 复核 POS 前端模板/逻辑，定位为何仍显示旧格式
- [x] 调整代码以展示“￥512/g x 125 g”格式
- [x] 确保总价显示与 512 × 125 一致
- [ ] 在 POS 中复测并记录验证结果
## task202510101200-purchase-piece-weight-doc

Original Request
> 目前有两类产品，一类是计件的，每件有每件的单价，一类是计重的，每个产品进货是按重量g来计量的，那么在采购环节，我应该如何具体操作，或者在产品基础主数据方面，该如何操作，需要详细说明步骤，补充到文档./doc/product_full_workflow_cn.md中。

Checklist
- [x] 创建任务执行文件 `z-todolist/task202510101200-purchase-piece-weight-doc.md`
- [x] 理解并整理计件与计重产品在采购环节与主数据的操作流程
- [x] 更新文档 `doc/product_full_workflow_cn.md`，补充详细步骤说明
- [x] 自查文档格式与措辞，确保与现有内容一致
- [x] 提交代码并准备 PR 描述

## task202510100355-product-workflow-bilingual

Original Request
> 将文档./doc/product_full_workflow_cn.md中，所有的操作步骤，前面中文后面标记英文，这样我好在英文界面下操作。

Checklist
- [x] 创建任务执行记录文件 `z-todolist/task202510100355-product-workflow-bilingual.md`
- [x] 梳理文档中需要标注英文的操作步骤
- [x] 为每个操作步骤补充对应英文描述
- [x] 自查文档排版与标点，确保中英并列清晰
- [x] 总结变更并更新待办记录

## task202510101530-describe-purchase-uom

Original Request
> 文档./doc/product_full_workflow_cn.md中下面的描述，详细说明一下如何找到`采购计量单位`这个操作位置。

Checklist
- [x] Review the existing instructions around purchase UoM in the product workflow doc
- [x] Update `doc/product_full_workflow_cn.md` to explain how to find the Purchase UoM field
- [x] Record execution details in the dedicated task log
- [x] Verify formatting and instructions in the updated documentation

## task202510131120-setup-odoo18-server

Original Request
> 我新申请了一个云服务器，ubuntu22.4，两个存储盘分别都是80G。
> 要准备安装生产环境的odoo18系统，从零开始装，数据库需要使用docker来装。
> 需要帮我写一个完整的，详细的过程，包括但不限于：加载硬盘，合理分配两个硬盘的应用存储，安装数据库、odoo18（我有github库代码，Branch_18.0.chowtaiking分支）使用nginx配置外网访问，外网域名jpp.chwwdk.com。
> 将整体业务流程写入z-todolist。

Checklist
- [x] 建立任务执行文件并整理原始需求
- [x] 完成磁盘规划与挂载步骤说明
- [x] 整理Docker化PostgreSQL与Odoo 18部署流程
- [x] 编写Nginx对外发布与域名配置步骤
- [x] 将完整流程同步到任务文件并准备答复
