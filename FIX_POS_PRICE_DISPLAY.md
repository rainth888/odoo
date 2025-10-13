# 🔧 修复 POS 价格显示问题 - 完整流程

## 当前问题
POS 显示：`1.00x￥880/g`  
期望显示：`￥512/g x 125 g`（总价 ￥64,000）

---

## 🚀 快速修复步骤

### 第一步：运行诊断脚本

```bash
# Windows PowerShell
python odoo-bin shell -c odoo.conf -d 你的数据库名 < test_by_weight_pricing.py
```

**仔细查看输出**，找出哪一步失败了。

---

### 第二步：根据诊断结果修复

#### 情况 A：未找到"足金"金属类型

**通过界面创建：**
1. 打开 Odoo
2. 进入 **POS → Metal Pricing → Metal Types**
3. 点击 **创建**
4. 填写：
   - **Name**: `足金`
   - **Code**: `zu_jin`
   - **Default Fineness Factor**: `1.0`
5. 保存

**或通过 SQL 创建：**
```sql
INSERT INTO metal_type (name, code, fineness_factor, sequence, active, create_date, write_date)
VALUES ('足金', 'zu_jin', 1.0, 11, true, NOW(), NOW())
ON CONFLICT DO NOTHING;
```

#### 情况 B：未找到"足金"的每日金价

**通过界面创建：**
1. 进入 **POS → Metal Pricing → Daily Metal Prices**
2. 点击 **创建**
3. 填写：
   - **Name**: `足金-2024-10-09`
   - **Company**: 选择您的公司
   - **Metal Type**: 选择 `足金 (zu_jin)`
   - **Price (CNY/gram)**: `512.000`
   - **Effective Date**: `2024-10-09`（今天）
   - **Active**: ✓
4. 保存

**或通过 SQL 创建：**
```sql
-- 先获取金属类型 ID 和公司 ID
SELECT id FROM metal_type WHERE code = 'zu_jin';  -- 假设得到 ID = 5
SELECT id FROM res_company LIMIT 1;                -- 假设得到 ID = 1

-- 插入每日金价（替换下面的 5 和 1 为实际 ID）
INSERT INTO metal_pricelist (
    name, metal_type_id, price_per_g, fineness_factor, 
    effective_date, company_id, active, create_date, write_date
)
VALUES (
    '足金-2024-10-09', 5, 512.000, 1.0,
    '2024-10-09', 1, true, NOW(), NOW()
);
```

#### 情况 C：产品属性值不是"足金"或匹配失败

**检查产品属性：**
```sql
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

确认属性值**精确**是"足金"（不能有空格或其他字符）。

如果属性值不是"足金"，有两个选择：

**选择 1：修改产品属性为"足金"**
1. 打开产品
2. Attributes & Variants 标签页
3. 修改"成色"属性值为"足金"

**选择 2：为实际属性值创建金属类型**

例如，如果属性值是"Au999.9"：
1. 进入 Metal Types
2. 创建：Name=`Au999.9`, Code=`au9999`, Factor=`1.0`
3. 创建对应的每日金价

#### 情况 D：产品 Pricing Method 不是 'by_weight'

1. 打开产品 0520000699
2. General Information 标签页
3. Sales Price 下方
4. 选择 **By Weight**
5. 保存

#### 情况 E：产品重量不正确

1. 打开产品
2. 检查 Weight 字段
3. 确保是 `0.125` kg（= 125 g）
4. 保存

---

### 第三步：升级模块

```bash
# 升级两个相关模块
python odoo-bin -c odoo.conf -d 你的数据库名 -u product_weight_pricing,pos_gold_pricing --stop-after-init

# 重启服务
# Windows: 重启 Odoo 服务
# Linux: sudo systemctl restart odoo
```

---

### 第四步：清空浏览器缓存（重要！）

#### Chrome/Edge - 最彻底的方法

**方法 1：开发者工具清空（推荐）**
```
1. 打开 Odoo 任意页面
2. 按 F12 打开开发者工具
3. 右键点击浏览器刷新按钮（地址栏旁边）
4. 选择"清空缓存并硬性重新加载"
```

**方法 2：设置中清空**
```
1. Chrome 右上角 ⋮ → 更多工具 → 清除浏览数据
2. 时间范围：全部时间
3. 勾选：
   ✓ 浏览历史记录
   ✓ Cookie 及其他网站数据  
   ✓ 缓存的图片和文件
4. 点击"清除数据"
```

**方法 3：快捷键（快速但不彻底）**
```
按 Ctrl + Shift + Delete
选择"全部时间"
勾选"缓存的图片和文件"
清除
```

#### 确认缓存已清空

1. 关闭所有 Odoo 标签页
2. 关闭浏览器
3. 重新打开浏览器
4. 重新登录 Odoo

---

### 第五步：在 POS 中测试

```
1. 打开 POS
2. 开启新会话
3. 搜索或扫描产品 0520000699
4. 检查显示
```

**期望结果：**
```
价格栏显示：￥512/g x 125 g
总价：￥64,000.00
```

---

## 🧪 高级诊断（如果上述步骤无效）

### 在 POS 页面检查前端

按 F12 打开开发者工具，在 Console 中运行：

```javascript
// 1. 检查 POS Store
const pos = odoo.__DEBUG__.services['pos.store'];
console.log('POS Store:', pos);

// 2. 查找产品
const product = pos.data.models['product.product'].getAll()
    .find(p => p.barcode === '0520000699');
console.log('Product:', product);
console.log('Pricing Method:', product?.pos_pricing_method);
console.log('Weight:', product?.weight);

// 3. 测试 RPC 调用
if (product) {
    try {
        const result = await pos.data.call(
            'product.product',
            'pos_compute_price_by_weight',
            [[product.id], pos.company?.id || 1]
        );
        console.log('✓ RPC Result:', result);
        console.log('  - weight_g:', result.weight_g);
        console.log('  - price_per_g:', result.price_per_g);
        console.log('  - unit_price:', result.unit_price);
    } catch (error) {
        console.error('✗ RPC Error:', error);
    }
}

// 4. 检查订单行
const order = pos.selectedOrder;
if (order && order.orderlines.length > 0) {
    const line = order.orderlines[0];
    console.log('Order Line:', line);
    console.log('_weight_pricing:', line._weight_pricing);
    
    const displayData = line.getDisplayData();
    console.log('Display Data:', displayData);
    console.log('weightPricingLabel:', displayData.weightPricingLabel);
}
```

**如果 RPC 调用失败：**
- 检查后端日志（odoo.log）
- 确认模块已升级
- 确认产品配置正确

**如果 RPC 成功但 _weight_pricing 为空：**
- 前端 JS 代码可能未正确加载
- 检查 Network 标签，确认 pos_pricing_method.js 加载成功（状态 200）

**如果 weightPricingLabel 为空：**
- 检查 getDisplayData() 方法逻辑
- 可能是计算逻辑有误

---

## 📋 完整检查清单

执行每一步后打勾：

- [ ] 运行诊断脚本 `test_by_weight_pricing.py`
- [ ] 创建"足金"金属类型（如果不存在）
- [ ] 创建"足金"每日金价 512元/克
- [ ] 确认产品属性值是"足金"
- [ ] 确认产品 Pricing Method = By Weight
- [ ] 确认产品 Weight = 0.125 kg
- [ ] 升级模块 `product_weight_pricing` 和 `pos_gold_pricing`
- [ ] 重启 Odoo 服务
- [ ] 清空浏览器缓存（使用方法 1）
- [ ] 关闭并重新打开浏览器
- [ ] 重新登录 Odoo
- [ ] 打开 POS 并测试

---

## 🆘 仍然无法解决？

请提供以下信息：

1. **诊断脚本的完整输出** (`test_by_weight_pricing.py`)
2. **浏览器 Console 中的 JavaScript 测试输出**
3. **浏览器 Console 中的任何错误信息（红色）**
4. **Odoo 后端日志中的错误**
5. **产品配置截图**：
   - General Information 标签页
   - Attributes & Variants 标签页

---

## 💡 常见原因总结

| 显示问题 | 可能原因 | 解决方案 |
|---------|---------|---------|
| `1.00x￥880/g` | 默认值，RPC 未调用或失败 | 检查后端、升级模块 |
| `0.00x￥880/g` | 数量为 0 | 检查产品重量配置 |
| `125x￥512/g` | 格式不对，前端模板未生效 | 清空缓存、升级模块 |
| `125x￥0/g` | 金价为 0 | 创建"足金"每日金价 |
| `1.00x￥512/g` | 数量未更新为重量 | 检查前端 JS 逻辑 |

---

**立即开始第一步：运行诊断脚本！** 📊

