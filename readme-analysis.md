# POS 收据/小票打印视图定位与可复用建议（分析）

本项目中 POS（point_of_sale）应用的收据/小票为前端 QWeb 模板（OWL 组件模板）。以下为与“店铺收据小票打印”最直接相关的视图名称（t-name）及源码路径，便于后续复用与定制成具有独特风格的小票。

## 关键视图（模板 t-name 与路径）

- `point_of_sale.OrderReceipt`
  - 路径：`addons/point_of_sale/static/src/app/screens/receipt_screen/receipt/order_receipt.xml`
  - 说明：核心小票内容模板（商品行、税额、小计、找零、二维码/唯一码等）。定制小票样式与结构的首选入口。

- `point_of_sale.ReceiptHeader`
  - 路径：`addons/point_of_sale/static/src/app/screens/receipt_screen/receipt/receipt_header/receipt_header.xml`
  - 说明：小票的抬头区（Logo、公司信息、抬头文案、收银员、取号/追踪号）。非常适合抽离复用、统一品牌风格。

- `point_of_sale.ReceiptScreen`
  - 路径：`addons/point_of_sale/static/src/app/screens/receipt_screen/receipt_screen.xml`
  - 说明：小票展示与打印所在的“收据屏”容器视图，内含“打印完整小票/基础小票”等按钮，页面把 `OrderReceipt` 渲染出来。

- `point_of_sale.OrderChangeReceipt`
  - 路径：`addons/point_of_sale/static/src/app/store/order_change_receipt_template.xml`
  - 说明：订单变更/后厨联（KOT）样式模板（更多用于餐饮业务流程）。

- `point_of_sale.CashMoveReceipt`
  - 路径：`addons/point_of_sale/static/src/app/navbar/cash_move_popup/cash_move_receipt/cash_move_receipt.xml`
  - 说明：现金收入/支出凭条模板，可复用 `ReceiptHeader`。

（餐饮扩展 pos_restaurant 对上述模板的继承与扩展）

- `pos_restaurant.OrderReceipt`（继承自 `point_of_sale.OrderReceipt`）
  - 路径：`addons/pos_restaurant/static/src/overrides/components/receipt_screen/order_receipt/order_receipt.xml`

- `pos_restaurant.ReceiptHeader`（继承自 `point_of_sale.ReceiptHeader`）
  - 路径：`addons/pos_restaurant/static/src/overrides/components/receipt_screen/receipt_screen.xml` 与 `.../order_receipt/order_receipt.xml`

- `pos_restaurant.ReceiptScreen`（继承自 `point_of_sale.ReceiptScreen`）
  - 路径：`addons/pos_restaurant/static/src/overrides/components/receipt_screen/receipt_screen.xml`

- `pos_restaurant.TipReceipt`
  - 路径：`addons/pos_restaurant/static/src/app/tip_receipt/tip_receipt.xml`
  - 说明：小费签名联模板。

以上模板名称与路径已在仓库中验证存在，可直接用于继承/覆盖以实现小票的深度定制与复用。

## 可复用与定制思路

1) 建议新建自定义模块（例如 `pos_custom_receipt`），依赖 `point_of_sale`（如涉及餐饮再依赖 `pos_restaurant`）。

2) 在自定义模块中新增 QWeb 模板文件，使用 `t-inherit` 对核心模板进行“extension”或“replace”式继承：

```
<!-- 示例：在抬头后增加品牌标语与分隔线 -->
<templates id="template" xml:space="preserve">
  <t t-name="pos_custom_receipt.OrderReceipt" t-inherit="point_of_sale.OrderReceipt" t-inherit-mode="extension">
    <xpath expr="//ReceiptHeader" position="after">
      <div class="pos-receipt-center-align my-1 brand-slogan">欢迎光临 · 自定义品牌</div>
      <div class="text-center">===============================</div>
    </xpath>
  </t>

  <t t-name="pos_custom_receipt.ReceiptHeader" t-inherit="point_of_sale.ReceiptHeader" t-inherit-mode="extension">
    <xpath expr="//div[hasclass('pos-receipt-contact')]" position="inside">
      <div class="text-center">门店：XX路XX号｜服务热线：400-XXX-XXXX</div>
    </xpath>
  </t>
</templates>
```

3) 将自定义 XML 加入前端 QWeb 资产：在模块 `__manifest__.py` 中：

```
"assets": {
  "point_of_sale.assets_qweb": [
    "pos_custom_receipt/static/src/xml/*.xml",
  ],
}
```

4) 自定义打印样式（热敏打印宽度、字体、间距、分隔线等）可通过引入自定义 CSS 完成：

```
"assets": {
  "point_of_sale.assets": [
    "pos_custom_receipt/static/src/css/receipt.css",
  ],
}
```

CSS 示例：

```
.pos-receipt { font-family: "Noto Sans SC", Arial, sans-serif; font-size: 12px; }
.pos-receipt .brand-slogan { font-weight: 600; letter-spacing: 1px; }
.pos-receipt .pos-receipt-logo { max-height: 48px; }
.pos-receipt .pos-receipt-right-align { float: right; }
@media print {
  .pos-receipt { width: 280px; }
}
```

5) 若需“可复用模块化”效果，尽量将共用区块抽象为独立模板（例如自定义的 `BrandHeader`、`PromoFooter`），在多个小票场景（收据、现金单、餐饮联等）中复用：

```
<t t-name="pos_custom_receipt.BrandHeader">
  <div class="text-center my-1">
    <img src="/my/module/path/logo.png" class="pos-receipt-logo"/>
    <div class="brand-slogan">定制品牌 · 专属风格</div>
  </div>
  <div class="text-center">------------------------------</div>
  <br/>
  <t t-if="0"/> <!-- 占位便于后续继承注入 -->
</t>
```

然后在 `OrderReceipt`/`ReceiptHeader` 等模板内部合适位置插入：

```
<BrandHeader />
```

## 相关（可选）页面/视图

- 发票请求相关网站页面（二维码/唯一码对应的查询流程）：
  - `point_of_sale.ticket_request_with_code`
  - `point_of_sale.ticket_validation_screen`
  - 控制器匹配：`addons/point_of_sale/controllers/main.py` 中 `/pos/ticket`、`/pos/ticket/validate` 路由

这部分并非打印小票本身，但若您希望打造“从小票扫码/取码到发票申领”的一体化体验，也可以同步自定义其视图样式（品牌化统一风格）。

## 结论与建议

- 最核心可定制与复用的模板为：`point_of_sale.OrderReceipt` 与 `point_of_sale.ReceiptHeader`。
- 若涉及餐饮/后厨联，请同步考虑 `point_of_sale.OrderChangeReceipt` 与 `pos_restaurant.*` 中的继承模板。
- 通过 `t-inherit` + 资产注入（`point_of_sale.assets_qweb` 与 `point_of_sale.assets`）即可实现“非系统默认样式”的专属小票，并以组件化方式在多场景复用，保持风格统一。

