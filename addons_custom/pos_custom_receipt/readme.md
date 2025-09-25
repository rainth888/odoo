# POS Custom Receipt (Thermal Style)

模块代号：`pos_custom_receipt`

面向 Odoo POS 的前端小票（收据）样式定制模块。参考并复用已有模块 `sale_receipt_thermal` 的热敏票据风格（58mm/简洁表格/分隔线/Logo 抬头等），在 POS 的收据屏（Receipt Screen）中展示与打印，形成可复用且具有品牌统一风格的小票。

> 研发背景与模板定位请参考仓库技术分析文档：`readme-analysis.md`

---

## 功能特性
- 在 POS 收据屏内应用热敏小票外观（默认 58mm 风格）。
- 抬头居中显示：公司 Logo、名称、联系方式等。
- 订单信息：订单号、日期、门店名称。
- 商品明细与合计：基于 POS 原生数据渲染，表格对齐、分隔线清晰。
- 支付信息与找零：以表格形式右对齐。
- 条码/二维码：
  - 条码使用 `pos.order` 的 `name` 生成 Code128 条码（供识别/对帐）。
  - 若原生 POS 已提供二维码数据（如发票/自助门户），继续保留显示。
- 页脚：“谢谢惠顾”与订单号/日期，风格统一且简洁。

> 注：本模块尽量不依赖后端自定义字段，直接使用 POS 前端可用数据，确保即装即用。

---

## 版本与依赖
- 适配版本：Odoo 18（前端 OWL/QWeb 架构）。
- 依赖模块：`point_of_sale`、`sale_receipt_thermal`（用于提供公司配置字段与风格参考）。
- 关系说明：直接复用 `sale_receipt_thermal` 定义的公司配置字段（纸宽/字体/Logo/条码/二维码/页脚备注/营业编号/宣传语/标语），并将其加载到 POS 前端用于渲染。

---

## 安装
1. 确保 `addons_custom` 在 Odoo 的 `--addons-path` 中。
2. 更新应用列表，在应用中安装“POS Custom Receipt (Thermal Style)”。

---

## 使用
- 打开 POS，下单并完成支付，进入“收据屏（Receipt Screen）”。
- 屏幕右侧的收据预览区域会呈现热敏票据风格；点击“Print Full Receipt”打印。
- 手机/平板界面同样适配（自动换行、简化间距）。

### 配置项（复用自 sale_receipt_thermal 的公司字段）
- 路径：设置 → 公司或技术设置 → 公司（启用开发者模式）
- 字段：
  - 纸宽：`receipt_paper_width`（58/80），打印预览容器宽度随之变化
  - 字体：`receipt_font_size`（8/10/12/14）
  - 显示 Logo：`receipt_show_logo`
  - 显示条码（订单号）：`receipt_show_barcode`
  - 显示二维码（订单号/业务二维码）：`receipt_show_qr`
  - 小票页脚备注：`receipt_footer_note`
  - 营业编号：`receipt_business_number`
  - 宣传语（多行）：`receipt_promo_lines`
  - 标语：`receipt_slogan`

> 以上字段已通过 `_load_pos_data_fields` 注入到 POS 前端，修改后重新进入 POS 界面即可生效（部分场景需刷新浏览器缓存）。

---

## 模板与资源
- QWeb 模板（前端，继承 POS 核心模板）：
  - `pos_custom_receipt.ReceiptScreen` 继承 `point_of_sale.ReceiptScreen`
  - `pos_custom_receipt.ReceiptHeader` 替换 `point_of_sale.ReceiptHeader`
  - `pos_custom_receipt.OrderReceipt` 扩展 `point_of_sale.OrderReceipt`
- 模板路径：
  - `addons_custom/pos_custom_receipt/static/src/xml/pos_custom_receipt.xml`
- 样式路径：
  - `addons_custom/pos_custom_receipt/static/src/css/receipt.css`
- 主样式类：
  - `.o_pos_receipt_thermal`（58mm 外观容器）
  - `.center` / `.r` / `.bold` / `.muted` / `.dash` / `.logo`

> 收据容器还会根据公司配置动态设置 `style`：`width: {receipt_paper_width}mm; font-size: {receipt_font_size}px;`

---

## 行为细节
- 收据容器：在收据预览容器上注入 `.o_pos_receipt_thermal` 类，控制宽度/字体/间距。
- 抬头（Header）：使用公司 Logo + 名称 + 营业编号 + 电话/邮箱；支持公司标语与多行宣传语；可附加 Header 自定义文本和收银员信息；追踪号（客显号码）较大字体显示。
- 合计区域：保持与原生逻辑一致，仅做表格对齐展示（总计/四舍五入/应收）。
- 支付与找零：按行右对齐；在“页脚前”区块按公司配置显示条码/二维码。
- “Powered by” 原区块替换为风格化页脚（优先显示公司页脚备注），保留订单号与时间信息。

---

## 可配置与扩展
- 纸宽/字体：推荐优先在公司配置中设置（`receipt_paper_width`/`receipt_font_size`），本模块已在前端动态应用。
- 条码/二维码控制：如需开关控制，可在前端判断（或扩展 POS 加载公司配置字段），例如：
  ```xml
  <t t-if="props.data.name and company.receipt_show_barcode">
    <img t-att-src="'/report/barcode/Code128/' + props.data.name + '?width=300&height=60&humanreadable=1'"/>
  </t>
  ```
  若要复用 `sale_receipt_thermal` 中的公司配置（纸宽/字体/是否显示条码等），需要在 POS 前端加载这些字段：
  - 扩展 POS `models`，将自定义字段注入 `res.company` 加载列表。
  - 在模板中使用 `props.data.headerData.company.<field>` 做条件控制。
  本模块已实现该数据加载与模板控制（详见 `models/res_company.py` 与 `static/src/xml/pos_custom_receipt.xml`）。

---

## 二开指引
- 继承点：优先使用 `t-inherit` + `xpath` 定位替换（避免完全重写）。
- 复用块：将可复用区块（如品牌头、活动页脚）拆分为独立模板片段，再在 `OrderReceipt/ReceiptHeader` 中引用。
- 字体与国际化：热敏打印机常见宽度有限，建议使用紧凑字体与较小字号；注意多语言换行与对齐。
- 与后台 PDF 报表并存：本模块不影响 `ir.actions.report` 的后端报表（如 `sale_receipt_thermal` 的 PDF 报表），两者可以并存。

---

## 注意事项与兼容性
- 浏览器打印设置：请关闭“缩放以适应纸张”，避免自动缩放影响排版；建议纸张边距设为最小。
- 打印机驱动：不同品牌热敏打印机对边距与字符渲染略有差异，请按实际设备微调 `receipt.css`。
- 硬件端：若使用 IoT Box 或网络打印机，建议先在 POS 前端确认预览无误，再测打印效果。

---

## 故障排查
- 前端样式未生效：
  - 开发者模式 → 更新资产（Assets）/ 硬刷新（Ctrl+F5）。
  - 确认模块已安装且 `__manifest__.py` 的 `assets` 正确加载到 `point_of_sale.assets`/`assets_qweb`。
- 条码/二维码不显示：确认订单号存在、二维码字段 `props.data.pos_qr_code` 已按业务启用。
- 字体缺失中文：为热敏打印机安装中文字体或使用内置支持的等宽字体，或调整为支持 CJK 的字体族。

---

## 操作过程（与问题排查记录）
1. 新建模块 `pos_custom_receipt`，注册 QWeb 与 CSS 资产，前端继承 `ReceiptScreen/ReceiptHeader/OrderReceipt` 模板，完成热敏布局初版。
2. 将 `sale_receipt_thermal` 作为依赖，复用其公司配置字段，并在 `models/res_company.py` 中扩展 `_load_pos_data_fields`，把相关字段（纸宽/字体/Logo/条码/二维码/页脚/营业编号/宣传语/标语）加载到 POS 前端。
3. 在模板中按公司配置动态渲染：
   - 容器宽度/字号（`receipt_paper_width`/`receipt_font_size`）
   - Logo 显示、条码/二维码开关、页脚备注、营业编号、标语、宣传语
4. 测试步骤：
   - 在 Apps 中安装 `sale_receipt_thermal`、`pos_custom_receipt`
   - 设置 → 公司 → 配置上述字段（如：纸宽=58、字体=10、标语=“免税 TAX FREE”、宣传语多行等）
   - 刷新前端 POS，完成一笔订单 → 收据屏 预览与打印验证
   - 对比期望样例 `doc/Receipt-S00024.pdf`，确认排版一致性
5. 若安装后搜不到模块：
   - 清除 Apps 过滤器，启用开发者模式并“更新应用列表”
   - 或命令行安装：`-i pos_custom_receipt`，首次安装后再正常启动


---

## 变更记录（Changelog）
- 1.0.0（初始）
  - 新增：ReceiptScreen 容器风格化、ReceiptHeader 重构、OrderReceipt 扩展（订单信息/合计/支付/条码/二维码/页脚）。
  - 新增：`receipt.css`（58mm 默认样式）。

> 维护约定：后续所有技术变更、功能开关、使用方式更新，需同步维护本 README 的对应章节（含版本号与日期）。

---

## 维护建议
- 提交前检查清单（建议）：
  - [ ] 更新/新增模板是否遵循 `t-inherit` + `xpath` 原则。
  - [ ] 前端资产已加入 `__manifest__.py` 并通过热加载/刷新验证。
  - [ ] 变更点已在本文件“变更记录/使用说明/可配置项”中同步。
  - [ ] 在 58mm 与 80mm 打印机上做最小验证（如有）。
