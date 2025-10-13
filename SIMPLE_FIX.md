# 🎯 简单直接的修复方案

## 问题：POS 显示 `1.00x￥880/g` 而不是 `￥512/g x 125 g`

---

## ✅ 解决方案（5分钟完成）

### 步骤 1：创建"足金"金属类型

1. 打开浏览器，登录 Odoo
2. 进入：**POS → Metal Pricing → Metal Types**
3. 点击右上角 **创建** 按钮
4. 填写以下信息：
   ```
   Name:                  足金
   Code:                  zu_jin
   Default Fineness Factor: 1.0
   Sequence:              11
   Description:           足金，纯度999.9
   ```
5. 点击 **保存**

### 步骤 2：创建"足金"的每日金价

1. 进入：**POS → Metal Pricing → Daily Metal Prices**
2. 点击右上角 **创建** 按钮
3. 填写以下信息：
   ```
   Name:            足金价格-今天
   Company:         [选择您的公司，通常是第一个]
   Metal Type:      足金 (zu_jin)  ← 选择刚才创建的
   Price (CNY/gram): 512
   Fineness Factor: 1.0  (应该自动填充)
   Effective Date:  [选择今天的日期]
   Active:          ✓ (必须勾选)
   ```
4. 点击 **保存**

### 步骤 3：检查产品配置

1. 进入：**库存 → 产品 → 产品**
2. 搜索条形码：`0520000699`
3. 打开产品
4. 检查 **General Information** 标签页：
   - **Sales Price** 下方应该选择了 **By Weight**
   - **Weight** 应该是 `0.125` (kg)
5. 检查 **Attributes & Variants** 标签页：
   - 应该有属性"成色"或类似的
   - 值应该是 **"足金"** （必须完全一致）

如果不一致，请修改。

### 步骤 4：重启 Odoo 服务

找到运行 Odoo 的窗口（通常是 PowerShell 或命令行窗口）：
- 按 **Ctrl + C** 停止服务
- 等待完全停止
- 重新运行启动命令（通常是 `python odoo-bin -c odoo.conf`）

### 步骤 5：清空浏览器缓存（关键！）

#### 方法 A：最彻底的方式

**Chrome/Edge：**
1. 打开 Odoo 页面
2. 按 **F12** 打开开发者工具
3. **右键点击**浏览器刷新按钮（地址栏旁边的圆形箭头）
4. 选择：**"清空缓存并硬性重新加载"**

**Firefox：**
1. 按 **Ctrl + Shift + Delete**
2. 时间范围选：**全部**
3. 只勾选：**缓存**
4. 点击 **立即清除**

#### 方法 B：完全清除

1. 按 **Ctrl + Shift + Delete**
2. 时间范围：**全部时间**
3. 勾选所有：
   - ✓ 浏览历史记录
   - ✓ Cookie 及其他网站数据
   - ✓ 缓存的图片和文件
4. 点击 **清除数据**
5. **关闭浏览器**
6. **重新打开浏览器**

### 步骤 6：测试

1. 登录 Odoo
2. 打开 **POS**
3. 点击 **新建会话** 或进入现有会话
4. 搜索或扫描产品：`0520000699`
5. 查看价格显示

**期望结果：**
```
价格栏：￥512/g x 125 g
总价：  ￥64,000.00
```

---

## 🔍 如果还是不行，检查这些：

### 检查 A：确认"足金"金属类型已创建

1. 进入：**POS → Metal Pricing → Metal Types**
2. 在列表中找到 **"足金"**
3. 确认：
   - Name = `足金`
   - Code = `zu_jin`
   - Active = ✓（勾选）

### 检查 B：确认"足金"金价已创建

1. 进入：**POS → Metal Pricing → Daily Metal Prices**
2. 找到 Metal Type 为 **"足金"** 的记录
3. 确认：
   - Price (CNY/gram) = `512`
   - Effective Date = 今天或更早的日期
   - Active = ✓（勾选）

### 检查 C：确认产品属性值完全匹配

打开产品 `0520000699`，查看 **Attributes & Variants**：

**属性值必须是以下之一：**
- 精确的 `足金` （没有空格、标点）
- 或者属性值的显示名称包含"足金"

**如果不匹配：**

**选项 1：** 修改产品属性值为"足金"

**选项 2：** 为实际的属性值创建对应的金属类型

例如，如果属性值是 "Au 999.9"：
1. 在 Metal Types 中创建：
   - Name: `Au 999.9`
   - Code: `au_999_9`
   - Fineness Factor: `1.0`
2. 在 Daily Metal Prices 中为它设置价格 512

---

## 🆘 仍然显示错误？

### 可能的显示结果和原因：

| 显示内容 | 原因 | 解决方法 |
|---------|------|---------|
| `1.00x￥880/g` | 后端计算未执行或失败 | 重启 Odoo，清空缓存 |
| `0.00x￥880/g` | 产品重量为 0 | 设置产品 Weight = 0.125 |
| `125x￥0/g` | 没有找到"足金"金价 | 创建"足金"每日金价 |
| `125x￥512/g` | 格式不对，前端模板未加载 | 清空缓存并硬刷新 |
| 无法添加产品 | 产品配置错误 | 检查产品是否 Available in POS |

---

## 📋 快速检查清单

请确保完成以下每一项：

- [ ] 创建了"足金"金属类型（Name=足金, Code=zu_jin）
- [ ] 创建了"足金"的每日金价（Price=512, 今天日期, Active=✓）
- [ ] 产品的 Pricing Method = By Weight
- [ ] 产品的 Weight = 0.125 kg
- [ ] 产品的属性值包含"足金"
- [ ] 重启了 Odoo 服务
- [ ] 清空了浏览器缓存（使用"清空缓存并硬性重新加载"）
- [ ] 关闭并重新打开了浏览器
- [ ] 重新登录了 Odoo

---

## 💡 关键提示

**最常见的问题：**
1. ❌ 没有创建"足金"金属类型
2. ❌ 没有创建"足金"的每日金价
3. ❌ 没有彻底清空浏览器缓存
4. ❌ 产品属性值和金属类型名称不匹配

**确保：**
✅ 产品属性值 = 金属类型的 Name 或 Code
✅ 每日金价的 Effective Date ≤ 今天
✅ 每日金价的 Active = ✓

---

## 🎯 最快验证方法

如果您有数据库访问权限，运行以下 SQL 快速检查：

```sql
-- 1. 检查"足金"是否存在
SELECT * FROM metal_type WHERE name = '足金';

-- 2. 检查"足金"的金价
SELECT mp.*, mt.name as metal_name 
FROM metal_pricelist mp
JOIN metal_type mt ON mt.id = mp.metal_type_id
WHERE mt.name = '足金' 
  AND mp.active = true
  AND mp.effective_date <= CURRENT_DATE
ORDER BY mp.effective_date DESC;
```

如果第一条查询返回空，说明没有创建"足金"金属类型。
如果第二条查询返回空，说明没有创建"足金"的每日金价。

---

**立即开始第一步！** 🚀

