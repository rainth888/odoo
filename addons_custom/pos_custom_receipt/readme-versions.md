# POS Custom Receipt (Thermal Style) — 版本变更记录

本文件记录模块 `pos_custom_receipt` 的版本演进、技术改动细节、兼容性与升级注意事项，便于回溯与维护。

---

## 1.1.0 — 与 sale_receipt_thermal 完整对齐（前端可配置）
- 日期时间：2025-09-22 15:00 +08:00
- 目标：在 POS 前端收据/小票中“完全复用”并对齐 `sale_receipt_thermal` 的热敏风格与公司配置项，确保在店铺现场打印出一致样式。
- 主要改动：
  - 依赖增强：`__manifest__.py` 中 `depends` 增加 `sale_receipt_thermal`，统一复用其公司配置字段。
  - 前端数据加载：新增 `models/res_company.py`，覆盖 `_load_pos_data_fields`，将以下公司字段同步到 POS 前端：
    - `receipt_paper_width`、`receipt_font_size`
    - `receipt_show_logo`、`receipt_show_barcode`、`receipt_show_qr`
    - `receipt_footer_note`、`receipt_business_number`、`receipt_promo_lines`、`receipt_slogan`
    - 动态判断字段存在性，避免未安装依赖时报错。
  - QWeb 模板强化：`static/src/xml/pos_custom_receipt.xml`
    - `ReceiptScreen`：根据 `receipt_paper_width`、`receipt_font_size` 动态设置预览容器宽度与字号。
    - `ReceiptHeader`（replace）：增加公司营业编号、标语、多行宣传语；Logo/联系方式可控；抬头居中，分隔线统一。
    - `OrderReceipt`（extension）：
      - 抬头后补充订单号/日期/门店信息。
      - 合计/取整/应收、支付行、找零等以表格右对齐显示。
      - 条码/二维码按公司配置开关显示；页脚优先显示公司备注，其次显示默认“谢谢惠顾”。
  - 样式补全：`static/src/css/receipt.css`
    - 增加 `.xs`、统一收据容器类 `.o_pos_receipt_thermal` 的打印细节；兼容中文字体与热敏机常用宽度。
  - 文档：更新 `readme.md` 的“版本与依赖”、“配置项”、“操作过程（与问题排查）”，说明如何通过公司字段控制 POS 小票外观与内容。
- 验收要点：
  - 在“设置 → 公司”中设置上述字段后，刷新 POS 界面，收据屏的预览/打印应与 `doc/Receipt-S00024.pdf` 视觉一致（Logo/抬头/分隔线/表格对齐/条码或二维码/页脚）。
  - 若条码/二维码未显示，检查对应显示开关与订单号、二维码生成逻辑是否启用。
- 兼容性：
  - 要求安装 `sale_receipt_thermal`；未安装时不加载不存在的字段。
  - 不影响后端 PDF 报表动作，两者可并存。
- 升级建议：
  - 升级模块（-u pos_custom_receipt）后，刷新浏览器缓存（Ctrl+F5）或在开发者模式下更新资产。

---

## 1.0.1 — 可见性与文档
- 日期时间：2025-09-22 12:00 +08:00
- 主要改动：
  - `__manifest__.py` 增加 `application=True`，便于在 Apps 视图默认筛选下被检索到。
  - 新增/完善模块文档 `readme.md`（功能特性、安装使用、模板与资源、注意事项等）。
- 升级建议：
  - Apps 列表中若未显示，启用开发者模式并“更新应用列表”。

---

## 1.0.0 — 初始版本
- 日期时间：2025-09-22 10:00 +08:00
- 主要内容：
  - 新增模块骨架 `pos_custom_receipt`，注册前端资产：
    - QWeb：`static/src/xml/pos_custom_receipt.xml`
    - CSS：`static/src/css/receipt.css`
  - 初次实现：
    - 继承并调整 `ReceiptScreen/ReceiptHeader/OrderReceipt`，提供热敏风格（58mm）的小票外观（抬头居中、分隔线、表格对齐、条码/二维码展示、风格化页脚）。
- 使用说明：
  - 安装后进入 POS，下单 → 收据屏预览 → 打印，即可查看初版热敏样式。

---

## 已知问题与后续计划
- 已知问题：
  - 不同热敏打印机在边距/缩放/字重上存在物理差异，可能需要在 `receipt.css` 内针对具体型号微调。
- 规划：
  - 可选：将“列宽/分隔线/字体族”抽象为更多公司配置或 POS 配置项，以便无代码微调。
  - 可选：增加“礼品小票（无价）”、“退货/换货小票”等变体模板，快速切换。

---

## 升级与回退指南（通用）
- 升级：
  - 命令行：`-u pos_custom_receipt`（或在 Apps 中“升级”）。
  - 升级后建议硬刷新前端（Ctrl+F5），确保最新资产生效。
- 回退：
  - 若需回退到旧版本，先在测试环境验证；注意清理浏览器缓存以避免缓存旧资产与新模板混用。
