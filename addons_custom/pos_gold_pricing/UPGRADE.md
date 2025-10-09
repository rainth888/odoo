# POS Gold Pricing - 升级指南

## 从 Selection 字段升级到动态配置的 Metal Type

### 变更说明

**版本**: 18.0.1.0 → 18.0.2.0

**重要变更**: 
- Metal Type 从硬编码的 Selection 字段改为可动态配置的 `metal.type` 模型
- 用户现在可以通过界面添加、修改和管理金属类型（如：添加银、铂金等）

### 升级步骤

#### 1. 备份数据库
在升级前，请务必备份您的 Odoo 数据库！

```bash
# 备份数据库示例
pg_dump your_database_name > backup_before_upgrade.sql
```

#### 2. 更新模块代码
```bash
cd /path/to/odoo
git pull  # 或其他方式更新代码
```

#### 3. 升级模块

方式一：通过 Odoo 界面
1. 登录 Odoo
2. 进入 **应用** 菜单
3. 激活 **开发者模式**
4. 搜索 "POS Gold Pricing"
5. 点击 **升级** 按钮

方式二：通过命令行
```bash
./odoo-bin -u pos_gold_pricing -d your_database_name --stop-after-init
```

#### 4. 数据迁移

升级后，系统会自动创建以下默认金属类型：
- Au 999.9 (code: au_9999)
- Au 999 (code: au_999)
- Au 18K (code: au_au18k)
- Au 14K (code: au_au14k)

**但是**，现有的 Daily Metal Prices 记录中的 `metal_type` 字段需要手动迁移到 `metal_type_id` 字段。

##### 数据迁移 SQL 脚本

**重要**: 在生产环境执行前，请先在测试环境验证！

```sql
-- 步骤 1: 为 metal.pricelist 表添加临时列（如果需要）
-- 这个步骤通常由 Odoo 自动完成

-- 步骤 2: 更新 metal_type_id 字段，将旧的 selection 值映射到新的 metal.type 记录
UPDATE metal_pricelist mp
SET metal_type_id = mt.id
FROM metal_type mt
WHERE mp.metal_type_id IS NULL
  AND mt.code = 'au_9999'
  AND (mp.metal_type = 'au_9999' OR mp.metal_type IS NULL);

UPDATE metal_pricelist mp
SET metal_type_id = mt.id
FROM metal_type mt
WHERE mp.metal_type_id IS NULL
  AND mt.code = 'au_999'
  AND mp.metal_type = 'au_999';

UPDATE metal_pricelist mp
SET metal_type_id = mt.id
FROM metal_type mt
WHERE mp.metal_type_id IS NULL
  AND mt.code = 'au_au18k'
  AND mp.metal_type = 'au_au18k';

UPDATE metal_pricelist mp
SET metal_type_id = mt.id
FROM metal_type mt
WHERE mp.metal_type_id IS NULL
  AND mt.code = 'au_au14k'
  AND mp.metal_type = 'au_au14k';

-- 步骤 3: 验证迁移结果
SELECT 
    COUNT(*) as total,
    COUNT(metal_type_id) as migrated,
    COUNT(*) - COUNT(metal_type_id) as unmigrated
FROM metal_pricelist;

-- 步骤 4: 对 stock.lot 表执行相同的迁移
UPDATE stock_lot sl
SET metal_type_id = mt.id
FROM metal_type mt
WHERE sl.metal_type_id IS NULL
  AND mt.code = sl.metal_type
  AND sl.metal_type IS NOT NULL;

-- 步骤 5: 验证 stock.lot 迁移结果
SELECT 
    COUNT(*) as total_with_metal_type,
    COUNT(metal_type_id) as migrated
FROM stock_lot
WHERE net_gold_weight > 0;
```

#### 5. 验证升级结果

1. **检查 Metal Types 配置**
   - 进入 POS → Metal Pricing → Metal Types
   - 确认存在 4 个默认金属类型

2. **检查 Daily Metal Prices**
   - 进入 POS → Metal Pricing → Daily Metal Prices
   - 确认现有记录的 Metal Type 字段显示正确
   - 创建一条新记录，测试金属类型选择功能

3. **检查库存批次**
   - 打开一个有黄金数据的库存批次
   - 确认金属类型显示正确

### 新功能使用

#### 添加新的金属类型

现在您可以轻松添加新的金属类型，如银、铂金等：

1. 进入 **POS → Metal Pricing → Metal Types**
2. 点击 **创建**
3. 填写信息：
   - **Name**: Ag 999 （显示名称）
   - **Code**: ag_999 （唯一代码，建议使用小写字母和下划线）
   - **Default Fineness Factor**: 1.0 （成色系数）
   - **Sequence**: 50 （排序）
4. 点击 **保存**

#### 修改现有金属类型

1. 进入 **POS → Metal Pricing → Metal Types**
2. 选择要修改的金属类型
3. 修改成色系数或其他信息
4. 点击 **保存**

### 常见问题

**Q: 升级后，现有的每日金价记录会丢失吗？**
A: 不会。但需要执行数据迁移 SQL 脚本来关联到新的金属类型。

**Q: 可以删除旧的金属类型吗？**
A: 如果该金属类型已被每日金价或库存批次使用，建议归档（Archive）而不是删除。

**Q: 成色系数可以在每日金价中单独设置吗？**
A: 可以。每日金价会继承金属类型的默认成色系数，但可以单独修改。

**Q: 升级失败怎么办？**
A: 使用备份的数据库恢复，然后联系技术支持。

### 技术细节

#### 字段映射关系

| 旧字段 (v1.0) | 新字段 (v2.0) | 类型变更 |
|--------------|---------------|---------|
| metal_type | metal_type_id | Selection → Many2one |
| default_metal_type | default_metal_type_id | Selection → Many2one |

#### API 兼容性

`get_price()` 方法已更新，现在同时支持：
- `metal_type_code` (string): 金属类型代码，如 'au_9999'
- `metal_type_id` (int): 金属类型 ID

示例：
```python
# 方式 1: 使用代码（向后兼容）
price, factor = self.env['metal.pricelist'].get_price(company_id, 'au_9999')

# 方式 2: 使用 ID
price, factor = self.env['metal.pricelist'].get_price(company_id, metal_type_record.id)
```

### 回滚

如果需要回滚到旧版本：

1. 恢复数据库备份
2. 切换到旧版本代码
3. 重启 Odoo 服务

**注意**: 回滚后，升级期间创建的新金属类型将丢失。

