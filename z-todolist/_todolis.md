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
