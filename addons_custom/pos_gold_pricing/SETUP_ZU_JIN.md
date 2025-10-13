# 设置"足金"金属类型和价格

## 问题描述

产品属性值为"足金"，但系统找不到对应的金属类型，导致 POS 显示错误的价格。

## 解决方案

### 方法 1: 通过界面手动创建（推荐）

#### 步骤 1: 创建"足金"金属类型

1. 进入 **POS → Metal Pricing → Metal Types**
2. 点击 **创建**
3. 填写以下信息：
   - **Name**: `足金`
   - **Code**: `zu_jin`
   - **Default Fineness Factor**: `1.0`
   - **Sequence**: `11`
   - **Description**: `足金，与 Au 999.9 等价`
4. 点击 **保存**

#### 步骤 2: 创建或更新"足金"的每日金价

1. 进入 **POS → Metal Pricing → Daily Metal Prices**
2. 点击 **创建**
3. 填写以下信息：
   - **Name**: `足金-2024-10-09` （或其他名称）
   - **Company**: 选择您的公司
   - **Metal Type**: 选择刚创建的 `足金 (zu_jin)`
   - **Price (CNY/gram)**: `512.000`
   - **Fineness Factor**: `1.0` （应自动继承）
   - **Effective Date**: `2024-10-09` （今天或您需要的日期）
   - **Active**: 勾选
4. 点击 **保存**

### 方法 2: 通过 SQL 直接插入

如果您有数据库访问权限，可以直接执行以下 SQL：

```sql
-- 1. 插入"足金"金属类型
INSERT INTO metal_type (name, code, fineness_factor, sequence, active, create_date, write_date)
VALUES ('足金', 'zu_jin', 1.0, 11, true, NOW(), NOW())
ON CONFLICT (code) DO NOTHING;

-- 2. 获取刚创建的金属类型 ID 和公司 ID
-- 假设您的公司 ID 是 1（base.main_company）
WITH metal_type_id AS (
    SELECT id FROM metal_type WHERE code = 'zu_jin' LIMIT 1
),
company_id AS (
    SELECT id FROM res_company WHERE name = 'My Company' LIMIT 1  -- 修改为您的公司名称
)
INSERT INTO metal_pricelist (
    name, 
    metal_type_id, 
    price_per_g, 
    fineness_factor, 
    effective_date, 
    company_id, 
    active,
    create_date,
    write_date
)
SELECT 
    '足金-2024-10-09',
    (SELECT id FROM metal_type_id),
    512.000,
    1.0,
    '2024-10-09',
    (SELECT id FROM company_id),
    true,
    NOW(),
    NOW()
FROM metal_type_id, company_id
WHERE NOT EXISTS (
    SELECT 1 FROM metal_pricelist 
    WHERE metal_type_id = (SELECT id FROM metal_type_id)
      AND effective_date = '2024-10-09'
      AND company_id = (SELECT id FROM company_id)
);
```

### 方法 3: 升级模块（如果是新安装）

如果这是新安装的数据库，可以直接升级模块：

```bash
./odoo-bin -u pos_gold_pricing -d your_database --stop-after-init
```

**注意**: 由于数据文件使用了 `noupdate="1"`，已有数据库升级模块不会自动创建新记录。

---

## 验证步骤

### 1. 检查 Metal Type 是否存在

```sql
SELECT id, name, code, fineness_factor 
FROM metal_type 
WHERE name = '足金' OR code = 'zu_jin';
```

应该返回一条记录。

### 2. 检查 Daily Metal Price 是否存在

```sql
SELECT 
    mp.name,
    mt.name as metal_type_name,
    mp.price_per_g,
    mp.effective_date,
    mp.active
FROM metal_pricelist mp
JOIN metal_type mt ON mp.metal_type_id = mt.id
WHERE mt.name = '足金'
ORDER BY mp.effective_date DESC
LIMIT 5;
```

应该返回您创建的每日金价记录，价格为 512.000。

### 3. 测试产品价格计算

在 Python Shell 中测试：

```python
# 获取产品
product = env['product.product'].search([('barcode', '=', '0520000699')], limit=1)

# 检查产品属性
print("产品属性值：")
for ptav in product.product_template_attribute_value_ids:
    print(f"  - {ptav.attribute_id.name}: {ptav.name}")

# 检查能否找到金属类型
tokens = product._pos_weight_pricing_candidate_tokens()
print(f"\n提取的候选令牌: {tokens}")

# 计算价格
price_data = product.pos_compute_price_by_weight(company_id=1)
print(f"\n价格计算结果:")
print(f"  weight_g: {price_data.get('weight_g')}")
print(f"  price_per_g: {price_data.get('price_per_g')}")
print(f"  unit_price: {price_data.get('unit_price')}")
print(f"  fineness_factor: {price_data.get('fineness_factor')}")

# 预期结果
expected_total = 512.0 * 125  # 512元/克 × 125克 = 64000元
print(f"\n预期总价: ￥{expected_total:,.2f}")
```

### 4. 在 POS 中验证

1. 重启 Odoo 服务
2. 清除浏览器缓存
3. 重新打开 POS 会话
4. 扫描或选择产品 `0520000699`
5. 检查价格显示：
   - 应该显示：`￥512/g x 125 g`
   - 总价应该是：`￥64,000.00`

---

## 常见问题

### Q1: 升级模块后还是没有"足金"金属类型？

**A**: 因为数据文件使用了 `noupdate="1"`，已有数据库不会自动创建。请使用**方法 1** 手动创建。

### Q2: 创建每日金价时找不到"足金"金属类型？

**A**: 请先确保按照**步骤 1** 创建了"足金"金属类型。

### Q3: POS 中还是显示错误的价格？

**A**: 请检查：
1. "足金"金属类型是否存在
2. 今天的每日金价记录是否存在且 Active = true
3. 产品的属性值是否确实是"足金"（精确匹配，区分大小写）
4. 是否重启了 Odoo 服务和清除了浏览器缓存
5. 使用上面的 Python Shell 测试，检查哪一步出错

### Q4: 如何为其他金属类型（如"18K"、"彩金"等）设置价格？

**A**: 按照相同的步骤：
1. 在 Metal Types 中创建新类型（如"18K"，code: "18k", factor: 0.75）
2. 在 Daily Metal Prices 中为该类型添加每日金价
3. 产品属性值要与 Metal Type 的 name 或 code 匹配

---

## 相关文档

- [UPGRADE.md](UPGRADE.md) - 升级指南
- [README.md](README.md) - 模块说明
- [TEST_CHECKLIST.md](TEST_CHECKLIST.md) - 测试清单

