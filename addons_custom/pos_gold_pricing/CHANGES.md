# 变更日志

## Version 18.0.2.0 - 2024-10-09

### 🎉 新功能

#### 动态配置金属类型
- **新增模型**: `metal.type` - 可通过界面动态添加和管理金属类型
- **新增菜单**: Point of Sale → Metal Pricing → Metal Types
- **支持特性**:
  - 自定义金属类型名称和代码
  - 配置默认成色系数
  - 拖拽排序
  - 归档功能
  - 多语言支持

### 🔄 变更内容

#### 模型变更

1. **metal.pricelist**
   - ❌ 移除: `metal_type` (Selection 字段)
   - ✅ 新增: `metal_type_id` (Many2one → metal.type)
   - 🔄 修改: `fineness_factor` 现在从 metal.type 自动继承，但可手动覆盖
   - 🔄 更新: `get_price()` 方法支持传入代码或ID（向后兼容）

2. **stock.lot**
   - ❌ 移除: `metal_type` (Selection 字段)
   - ✅ 新增: `metal_type_id` (Many2one → metal.type)
   - 🔄 更新: `compute_pos_unit_price()` 方法优化，处理缺失金属类型的情况

3. **product.template**
   - ❌ 移除: `default_metal_type` (Selection 字段)
   - ✅ 新增: `default_metal_type_id` (Many2one → metal.type)

#### 视图变更

- **metal_pricelist_views.xml**: 字段从 `metal_type` 改为 `metal_type_id`
- **stock_production_lot_views.xml**: 字段从 `metal_type` 改为 `metal_type_id`
- **metal_type_views.xml**: 新增 Metal Type 的树视图和表单视图

#### 数据文件

- **metal_type_data.xml**: 新增，包含4个默认金属类型：
  - Au 999.9 (au_9999) - 足金，系数 1.0
  - Au 999 (au_999) - 足金，系数 0.999
  - Au 18K (au_au18k) - 18K金，系数 0.75
  - Au 14K (au_au14k) - 14K金，系数 0.585

#### 安全权限

- 新增 `metal.type` 模型的访问权限配置

### 📋 文件清单

#### 新增文件
```
models/metal_type.py              - 金属类型模型
views/metal_type_views.xml        - 金属类型视图
data/metal_type_data.xml          - 默认金属类型数据
UPGRADE.md                        - 升级指南
CHANGES.md                        - 变更日志（本文件）
```

#### 修改文件
```
models/__init__.py                - 导入新模型
models/metal_pricelist.py         - 字段类型变更
models/stock_lot.py               - 字段类型变更
models/product_template.py        - 字段类型变更
views/metal_pricelist_views.xml   - 字段名称更新
views/stock_production_lot_views.xml - 字段名称更新
security/ir.model.access.csv      - 新增权限配置
__manifest__.py                   - 更新数据文件列表
README.md                         - 更新使用说明
```

### ⚠️ 破坏性变更

1. **数据库字段变更**
   - `metal_type` → `metal_type_id` 需要数据迁移
   - 需要执行 SQL 迁移脚本（见 UPGRADE.md）

2. **API 变更**
   - `get_price(company_id, metal_type)` 中的 `metal_type` 参数：
     - 旧版本: 只接受字符串代码 (如 'au_9999')
     - 新版本: 接受字符串代码或整数ID（向后兼容）

### 🎯 优势

#### 灵活性
- ✅ 无需修改代码即可添加新金属类型（银、铂金、钯金等）
- ✅ 可以为每种金属类型设置不同的默认成色系数
- ✅ 支持归档不再使用的金属类型

#### 可维护性
- ✅ 金属类型配置与代码分离
- ✅ 更好的数据一致性（外键约束）
- ✅ 更容易扩展和定制

#### 用户体验
- ✅ 业务用户可以自主管理金属类型
- ✅ 更直观的配置界面
- ✅ 支持多语言

### 🔧 升级步骤概要

1. 备份数据库
2. 更新代码
3. 升级模块 (`-u pos_gold_pricing`)
4. 执行数据迁移 SQL 脚本
5. 验证数据完整性
6. 测试功能

详细步骤请参阅 [UPGRADE.md](UPGRADE.md)

### 🐛 已知问题

无

### 📚 相关文档

- [README.md](README.md) - 模块说明和使用指南
- [UPGRADE.md](UPGRADE.md) - 详细升级指南和数据迁移脚本

### 🙏 致谢

感谢用户反馈，促成了这次改进！

---

## Version 18.0.1.0 - Initial Release

- 初始版本
- 硬编码 4 种金属类型（Selection 字段）
- 基本的每日金价管理功能

