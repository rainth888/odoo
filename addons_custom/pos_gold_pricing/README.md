
# POS Gold Pricing (Odoo 18)

最小可用模块：在 POS 中通过选择序列号（lot/serial）自动计算黄金首饰售价。

## 功能
- 在 `stock.production.lot` 上扩展首饰字段：净金重、证书号、工费等
- 新模型 `metal.type` 动态配置金属类型（金、银、铂金等）
- 新模型 `metal.pricelist` 维护每日金价/成色系数
- POS 前端：选择序列号后经 RPC 调用服务器计算单价并写入行价

## 安装
1. 将本目录放入 Odoo 的 `--addons-path` 路径下（或直接安装 ZIP）。
2. 更新应用列表，安装 **POS Gold Pricing** 模块。
3. 系统会自动创建默认金属类型（Au 999.9, Au 999, Au 18K, Au 14K）
4. 在菜单 **Point of Sale / Metal Pricing / Metal Types** 里可以添加新的金属类型（如银、铂金）
5. 在菜单 **Point of Sale / Metal Pricing / Daily Metal Prices** 里维护当日金价
6. 在产品模板上：勾选 *Available in POS*，`tracking=serial`，设置 POS 分类。
7. 在 POS 配置中启用 *Lots/Serials*，重开会话。

## 批量导入模板（CSV 在 `samples/` 目录）
- `pos_categories.csv` ：POS 分类（大类/子类）
- `products.csv` ：产品模板（可售、serial 跟踪、POS 分类）
- `lots.csv` ：序列号（净金重、工费、证书等单件差异）

导入：进入对应模型列表，点击“导入”，映射列，测试后导入。导入后重开 POS 会话。

## 配置金属类型

### 添加新的金属类型（如银、铂金）

1. 进入 **Point of Sale → Metal Pricing → Metal Types**
2. 点击 **创建**
3. 填写：
   - **Name**: 显示名称，如 "Ag 999" 或 "Pt 950"
   - **Code**: 唯一代码，如 "ag_999" 或 "pt_950"（建议小写+下划线）
   - **Default Fineness Factor**: 成色系数，如纯银为 1.0，铂金950为 0.95
   - **Sequence**: 排序号
   - **Description**: 可选的详细说明
4. 保存后，即可在每日金价中选择该金属类型

### 修改成色系数

- 在 **Metal Types** 中设置的是默认值
- 在创建 **Daily Metal Prices** 时会自动继承该默认值
- 可以在具体的每日金价记录中覆盖该值

## 升级指南

如果从旧版本升级，请参阅 [UPGRADE.md](UPGRADE.md) 了解数据迁移步骤。

## 注意
- 该模块示例级别，实际部署可根据业务调整字段/公式/权限（经理 PIN 才允许改价等）。
- 若前端未显示自动价，请清缓存并重开会话；查看浏览器控制台是否有 `POS gold pricing` 日志。

