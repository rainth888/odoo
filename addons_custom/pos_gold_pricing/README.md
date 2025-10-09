
# POS Gold Pricing (Odoo 18)

最小可用模块：在 POS 中通过选择序列号（lot/serial）自动计算黄金首饰售价。

## 功能
- 在 `stock.production.lot` 上扩展首饰字段：净金重、证书号、工费等
- 新模型 `pos.metal.type` 维护可配置金种，`metal.pricelist` 维护每日金价/成色系数
- POS 前端：选择序列号后经 RPC 调用服务器计算单价并写入行价

## 安装
1. 将本目录放入 Odoo 的 `--addons-path` 路径下（或直接安装 ZIP）。
2. 更新应用列表，安装 **POS Gold Pricing** 模块。
3. 在菜单 **Point of Sale / Metal Pricing / Metal Types** 里维护业务所需的金种（名称/编码，可按公司划分）。
4. 在菜单 **Point of Sale / Metal Pricing / Daily Metal Prices** 中为各金种维护当日金价与成色系数。
5. 在产品模板上：勾选 *Available in POS*，`tracking=serial`，设置 POS 分类，并选择默认金种（可选）。
6. 在 POS 配置中启用 *Lots/Serials*，重开会话。

## 批量导入模板（CSV 在 `samples/` 目录）
- `pos_categories.csv` ：POS 分类（大类/子类）
- `products.csv` ：产品模板（可售、serial 跟踪、POS 分类）
- `lots.csv` ：序列号（净金重、工费、证书等单件差异；导入前请先创建好金种并映射 `metal_type_id/id`）

导入：进入对应模型列表，点击“导入”，映射列，测试后导入。导入后重开 POS 会话。

## 注意
- 该模块示例级别，实际部署可根据业务调整字段/公式/权限（经理 PIN 才允许改价等）。
- 若前端未显示自动价，请清缓存并重开会话；查看浏览器控制台是否有 `POS gold pricing` 日志。

