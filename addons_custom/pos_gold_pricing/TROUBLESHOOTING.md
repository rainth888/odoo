# 🔧 POS 价格显示问题排查指南

## 问题：POS 中"By Weight"产品价格显示不正确

### 症状
- 当前显示：`1.00x￥880/g` 或 `0.00x￥880/g`
- 期望显示：`￥512/g x 125 g`，总价 `￥64,000.00`

---

## 🔍 完整排查步骤

### 步骤 1: 清空浏览器缓存 ⭐⭐⭐

#### Chrome/Edge（推荐方法）

**方法 A: 开发者工具清空缓存（最彻底）**
```
1. 按 F12 打开开发者工具
2. 右键点击浏览器刷新按钮（地址栏旁边的圆形箭头）
3. 在弹出菜单中选择：
   "清空缓存并硬性重新加载" 
   (Empty Cache and Hard Reload)
```

**方法 B: 快捷键清空所有缓存**
```
1. 按 Ctrl + Shift + Delete
2. 时间范围：选择"全部时间"
3. 勾选：
   ✓ 缓存的图片和文件
   ✓ Cookie 及其他网站数据
4. 点击"清除数据"
```

**方法 C: 硬刷新（快速但不彻底）**
```
在 Odoo 页面按：
- Ctrl + F5
或
- Ctrl + Shift + R
```

#### Firefox
```
1. Ctrl + Shift + Delete
2. 时间范围：全部
3. 勾选：缓存
4. 清除
```

### 步骤 2: 升级模块 ⭐⭐⭐

```bash
# 进入 Odoo 目录
cd /path/to/odoo

# 升级两个相关模块
./odoo-bin -c odoo.conf -d your_database -u product_weight_pricing,pos_gold_pricing --stop-after-init

# 重启服务
sudo systemctl restart odoo
# 或者直接运行
./odoo-bin -c odoo.conf
```

### 步骤 3: 检查"足金"金属类型是否创建成功

#### 方法 1: 通过界面检查
```
1. POS → Metal Pricing → Metal Types
2. 查找名为"足金"的记录
3. 确认：
   - Name = 足金
   - Code = zu_jin
   - Fineness Factor = 1.0
   - Active = ✓
```

#### 方法 2: 通过 SQL 检查
```sql
SELECT id, name, code, fineness_factor, active
FROM metal_type
WHERE name = '足金' OR code = 'zu_jin';
```

应该返回一条记录。

### 步骤 4: 检查"足金"的每日金价

#### 通过界面检查
```
1. POS → Metal Pricing → Daily Metal Prices
2. 查找 Metal Type = "足金"的记录
3. 确认：
   - Metal Type = 足金 (zu_jin)
   - Price (CNY/gram) = 512.000
   - Effective Date = 今天或更早的日期
   - Active = ✓
```

#### 通过 SQL 检查
```sql
SELECT 
    mp.id,
    mp.name,
    mt.name as metal_type,
    mp.price_per_g,
    mp.effective_date,
    mp.active
FROM metal_pricelist mp
JOIN metal_type mt ON mp.metal_type_id = mt.id
WHERE mt.name = '足金'
ORDER BY mp.effective_date DESC;
```

### 步骤 5: 检查产品属性配置

```sql
-- 检查产品
SELECT id, name, barcode, default_code
FROM product_product
WHERE barcode = '0520000699';

-- 检查产品属性（需要产品ID）
SELECT 
    pp.name as product_name,
    pa.name as attribute_name,
    pav.name as attribute_value
FROM product_product pp
JOIN product_template_attribute_value_line ptavl ON ptavl.product_id = pp.id
JOIN product_template_attribute_value ptav ON ptav.id = ptavl.product_attribute_value_id
JOIN product_attribute pa ON pa.id = ptav.attribute_id
JOIN product_attribute_value pav ON pav.id = ptav.product_attribute_value_id
WHERE pp.barcode = '0520000699';
```

确认输出包含类似：
```
product_name | attribute_name | attribute_value
-------------|----------------|----------------
[产品名]     | 成色           | 足金
```

### 步骤 6: 测试后端价格计算

```bash
./odoo-bin shell -c odoo.conf -d your_database
```

```python
# 测试完整流程
product = env['product.product'].search([('barcode', '=', '0520000699')], limit=1)

if not product:
    print("❌ 产品未找到！")
else:
    print(f"✓ 找到产品: {product.name} (ID: {product.id})")
    
    # 检查产品配置
    print(f"✓ Pricing Method: {product.product_tmpl_id.pos_pricing_method}")
    print(f"✓ Weight: {product.weight} kg = {product.weight * 1000} g")
    
    # 检查属性
    print("\n产品属性:")
    for ptav in product.product_template_attribute_value_ids:
        print(f"  - {ptav.attribute_id.name}: {ptav.name}")
    
    # 提取候选令牌
    tokens = product._pos_weight_pricing_candidate_tokens()
    print(f"\n提取的候选令牌: {tokens}")
    
    # 解析金属类型
    metal_type_ref = product._pos_weight_pricing_resolve_metal_type_ref(product.product_tmpl_id)
    print(f"\n解析的金属类型引用: {metal_type_ref}")
    
    if isinstance(metal_type_ref, int):
        metal_type = env['metal.type'].browse(metal_type_ref)
        print(f"金属类型: {metal_type.name} (Code: {metal_type.code})")
    else:
        print(f"金属类型代码: {metal_type_ref}")
    
    # 获取金价
    price_per_g, factor = env['metal.pricelist'].get_price(1, metal_type_ref)
    print(f"\n当前金价:")
    print(f"  - 价格: ￥{price_per_g}/g")
    print(f"  - 成色系数: {factor}")
    
    # 计算价格
    price_data = product.pos_compute_price_by_weight(company_id=1)
    print(f"\n价格计算结果:")
    print(f"  - weight_g: {price_data.get('weight_g')} g")
    print(f"  - price_per_g: ￥{price_data.get('price_per_g')}/g")
    print(f"  - unit_price: ￥{price_data.get('unit_price')}")
    print(f"  - fineness_factor: {price_data.get('fineness_factor')}")
    
    # 计算总价
    total = price_data.get('price_per_g', 0) * price_data.get('weight_g', 0)
    print(f"\n预期总价: ￥{total:,.2f}")
    print(f"期望显示: ￥{price_data.get('price_per_g')}/g x {price_data.get('weight_g')} g")
```

**预期输出：**
```
✓ 找到产品: [产品名] (ID: 123)
✓ Pricing Method: by_weight
✓ Weight: 0.125 kg = 125.0 g

产品属性:
  - 成色: 足金

提取的候选令牌: ['足金']

解析的金属类型引用: 5
金属类型: 足金 (Code: zu_jin)

当前金价:
  - 价格: ￥512.0/g
  - 成色系数: 1.0

价格计算结果:
  - weight_g: 125.0 g
  - price_per_g: ￥512.0/g
  - unit_price: ￥512.0
  - fineness_factor: 1.0

预期总价: ￥64,000.00
期望显示: ￥512.0/g x 125.0 g
```

### 步骤 7: 检查 POS 前端资源加载

打开 POS 页面，按 F12 打开开发者工具：

#### Console 标签页
```
查找错误信息（红色）
特别注意：
- JavaScript 错误
- 模块加载失败
- RPC 调用失败
```

#### Network 标签页
```
1. 刷新页面
2. 筛选：JS
3. 查找：
   - pos_pricing_method.js
   - pos_weight_orderline.xml
4. 确认状态码都是 200
```

### 步骤 8: 测试 RPC 调用

在 POS 页面的开发者工具 Console 中运行：

```javascript
// 获取 POS store
const pos = odoo.__DEBUG__.services['pos.store'];

// 查找产品
const product = pos.data.models['product.product'].getAll().find(p => p.barcode === '0520000699');
console.log('Product:', product);
console.log('Pricing Method:', product?.pos_pricing_method || product?.product_tmpl_id?.pos_pricing_method);

// 测试 RPC 调用
if (product) {
    const result = await pos.data.call(
        'product.product',
        'pos_compute_price_by_weight',
        [[product.id], pos.company?.id || 1]
    );
    console.log('Price Data:', result);
}
```

**预期输出：**
```javascript
Product: {id: 123, name: "...", barcode: "0520000699", ...}
Pricing Method: "by_weight"
Price Data: {
    weight_g: 125,
    unit_price: 512,
    price_per_g: 512,
    fineness_factor: 1
}
```

### 步骤 9: 强制重新加载 POS 资源

#### 方法 1: 更新资源版本号（推荐）

编辑 `addons_custom/product_weight_pricing/__manifest__.py`：

```python
{
    "name": "Product Weight & Pricing Method",
    "version": "18.0.1.5",  # ← 增加版本号
    ...
}
```

然后升级模块：
```bash
./odoo-bin -u product_weight_pricing -d your_database --stop-after-init
```

#### 方法 2: 重启 Odoo 并清空所有缓存

```bash
# 停止 Odoo
sudo systemctl stop odoo

# 清空 Odoo 会话缓存
redis-cli FLUSHDB  # 如果使用 Redis
# 或删除文件缓存
rm -rf ~/.local/share/Odoo/sessions/*

# 重启
sudo systemctl start odoo
```

### 步骤 10: 在 POS 中测试

```
1. 清空浏览器缓存（使用步骤1的方法A）
2. 关闭所有 Odoo 标签页
3. 重新登录 Odoo
4. 打开 POS
5. 开启新会话
6. 扫描或选择产品 0520000699
7. 检查显示
```

---

## 🐛 常见问题

### Q1: 显示还是 `0.00x￥880/g`

**可能原因：**
- 前端 JS 没有加载或执行
- RPC 调用失败
- `_weight_pricing` 数据未附加到订单行

**检查：**
```javascript
// 在 Console 中
const order = odoo.__DEBUG__.services['pos.store'].selectedOrder;
const line = order.orderlines[0];  // 假设是第一行
console.log('Line data:', line);
console.log('_weight_pricing:', line._weight_pricing);
```

如果 `_weight_pricing` 是 undefined，说明 RPC 调用失败或数据未正确附加。

### Q2: 显示 `125x￥512/g` 而不是 `￥512/g x 125 g`

**可能原因：**
- QWeb 模板未生效
- `weightPricingLabel` 未计算

**检查：**
```javascript
const order = odoo.__DEBUG__.services['pos.store'].selectedOrder;
const line = order.orderlines[0];
const displayData = line.getDisplayData();
console.log('Display Data:', displayData);
console.log('weightPricingLabel:', displayData.weightPricingLabel);
```

如果 `weightPricingLabel` 存在但未显示，检查 XML 模板是否正确加载。

### Q3: 金价是 0

**检查：**
1. "足金"金属类型是否存在
2. 每日金价记录是否存在且 Active = true
3. 日期是否正确（effective_date <= 今天）

### Q4: 重量是 0

**检查：**
```sql
SELECT weight FROM product_product WHERE barcode = '0520000699';
SELECT weight FROM product_template WHERE id = (
    SELECT product_tmpl_id FROM product_product WHERE barcode = '0520000699'
);
```

确保 weight 字段不为 0。注意：weight 单位是 kg，125g = 0.125kg。

---

## 🔄 完整重置流程

如果以上都不行，执行完整重置：

```bash
# 1. 升级模块
./odoo-bin -u product_weight_pricing,pos_gold_pricing -d your_db --stop-after-init

# 2. 重启服务
sudo systemctl restart odoo

# 3. 清空浏览器所有数据
# 打开 Chrome -> 设置 -> 隐私和安全 -> 清除浏览数据
# 选择"全部时间"，勾选所有选项，清除

# 4. 重新登录 Odoo
# 5. 重新打开 POS
# 6. 测试
```

---

## 📞 需要帮助？

如果按照以上步骤仍无法解决，请提供：

1. 步骤 6 的 Python 测试输出
2. 步骤 8 的 JavaScript 测试输出
3. 浏览器 Console 中的任何错误信息
4. Network 标签中 pos_pricing_method.js 的状态

