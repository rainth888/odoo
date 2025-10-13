# 🎯 最终修复步骤

## 情况确认
✅ "足金"金属类型已存在  
✅ "足金"每日金价已存在（512元/克）  
✅ 产品属性配置正确（成色 = 足金）  
❌ POS 仍显示 `1.00x￥880/g` 而不是 `￥512/g x 125 g`

**结论：数据配置正确，问题在前端代码或缓存**

---

## 🔧 立即执行以下步骤

### 步骤 1：升级模块（重要！）

在命令行运行：

```powershell
# 进入 Odoo 目录
cd D:\_projects\odoo.github.rainth888

# 停止正在运行的 Odoo（如果有）
# 按 Ctrl+C

# 升级相关模块
python odoo-bin -c odoo.conf -d odoo_rainth888 -u product_weight_pricing,pos_gold_pricing --stop-after-init

# 重新启动
python odoo-bin -c odoo.conf
```

**等待启动完成后再继续下一步**

---

### 步骤 2：彻底清空浏览器缓存

#### 方法 A：开发者工具清空（最有效）

1. 打开 Chrome/Edge 浏览器
2. 进入任意 Odoo 页面（不用登录）
3. 按 **F12** 打开开发者工具
4. **右键点击**浏览器刷新按钮（地址栏旁边的圆形箭头）
5. 在弹出菜单中选择：**"清空缓存并硬性重新加载"**

![清空缓存示意图](https://developers.google.com/web/tools/chrome-devtools/images/empty-cache-hard-reload.png)

#### 方法 B：完全清除（备选）

如果方法 A 没有这个选项：

1. 按 **Ctrl + Shift + Delete**
2. 时间范围：**全部时间**
3. 勾选：
   - ✓ 浏览历史记录
   - ✓ Cookie 及其他网站数据
   - ✓ 缓存的图片和文件
4. 点击 **清除数据**
5. **完全关闭浏览器**（关闭所有窗口）
6. **重新打开浏览器**

---

### 步骤 3：验证前端资源加载

1. 重新登录 Odoo
2. 打开 POS
3. 按 **F12** 打开开发者工具
4. 切换到 **Network** 标签页
5. 刷新页面
6. 在过滤框输入：`pos_pricing`
7. 查找：`pos_pricing_method.js`
8. 确认：
   - ✅ 状态码应该是 **200**（绿色）
   - ✅ Size 应该有数值（不是 cached）
   - ❌ 如果是 304 或 from cache，说明缓存没清干净

**如果显示 cached 或 304：**
- 关闭浏览器
- 删除浏览器缓存文件夹（高级方法）
- 重新打开浏览器

---

### 步骤 4：测试 POS

1. 在 POS 中新建会话
2. 搜索或扫描产品：`0520000699`
3. 检查显示

**期望结果：**
```
价格栏：￥512/g x 125 g
总价：  ￥64,000.00
```

---

## 🧪 前端调试（如果步骤 4 仍失败）

在 POS 页面，按 F12，切换到 **Console** 标签页，运行：

```javascript
// 获取 POS 服务
const posService = odoo.__DEBUG__?.services?.['pos.store'];

if (!posService) {
    console.error('❌ POS Store 未加载，请刷新页面');
} else {
    console.log('✓ POS Store 已加载');
    
    // 查找产品
    const products = posService.data.models['product.product'];
    const product = products?.getAll().find(p => p.barcode === '0520000699');
    
    if (!product) {
        console.error('❌ 产品未找到');
    } else {
        console.log('✓ 产品:', product.name);
        console.log('  - Pricing Method:', product.pos_pricing_method || product.product_tmpl_id?.pos_pricing_method);
        console.log('  - Weight:', product.weight, 'kg');
        
        // 测试 RPC 调用
        console.log('\n测试价格计算...');
        posService.data.call(
            'product.product',
            'pos_compute_price_by_weight',
            [[product.id], posService.company?.id || 1]
        ).then(result => {
            console.log('✓ 价格计算成功:');
            console.log('  - weight_g:', result.weight_g);
            console.log('  - price_per_g:', result.price_per_g);
            console.log('  - unit_price:', result.unit_price);
            console.log('  - fineness_factor:', result.fineness_factor);
            console.log('\n期望显示: ￥' + result.price_per_g + '/g x ' + result.weight_g + ' g');
            console.log('总价: ￥' + (result.price_per_g * result.weight_g).toFixed(2));
        }).catch(error => {
            console.error('❌ RPC 调用失败:', error);
        });
    }
}
```

**根据输出判断：**

- 如果显示 `❌ POS Store 未加载`：刷新页面，确保在 POS 界面
- 如果显示 `❌ 产品未找到`：产品可能未在 POS 中可用
- 如果显示 `❌ RPC 调用失败`：查看具体错误，可能是后端问题
- 如果显示 `✓ 价格计算成功`：说明后端正常，问题在前端显示逻辑

---

## 🔍 检查订单行数据

在 POS 中添加产品后，运行：

```javascript
const pos = odoo.__DEBUG__.services['pos.store'];
const order = pos.selectedOrder;

if (order && order.orderlines.length > 0) {
    const line = order.orderlines[0];  // 第一行
    
    console.log('订单行数据:');
    console.log('  - qty:', line.qty);
    console.log('  - price_unit:', line.price_unit);
    console.log('  - _weight_pricing:', line._weight_pricing);
    
    if (line._weight_pricing) {
        console.log('\n✓ Weight Pricing 数据已附加:');
        console.log('  - weight_g:', line._weight_pricing.weight_g);
        console.log('  - price_per_g:', line._weight_pricing.price_per_g);
        console.log('  - unit_price:', line._weight_pricing.unit_price);
    } else {
        console.log('\n❌ Weight Pricing 数据未附加！');
        console.log('可能原因：');
        console.log('  1. RPC 调用失败');
        console.log('  2. 前端 JS patch 未生效');
        console.log('  3. 浏览器缓存问题');
    }
    
    // 检查显示数据
    const displayData = line.getDisplayData();
    console.log('\n显示数据:');
    console.log('  - weightPricingLabel:', displayData.weightPricingLabel);
    console.log('  - qty:', displayData.qty);
    console.log('  - unitPrice:', displayData.unitPrice);
    
    if (!displayData.weightPricingLabel) {
        console.log('\n❌ weightPricingLabel 未生成！');
        console.log('需要检查 getDisplayData() 方法');
    }
}
```

---

## 🆘 高级修复：手动清除缓存文件

如果浏览器缓存顽固不清，手动删除：

### Chrome/Edge 缓存位置：

**Windows:**
```
C:\Users\你的用户名\AppData\Local\Google\Chrome\User Data\Default\Cache
C:\Users\你的用户名\AppData\Local\Microsoft\Edge\User Data\Default\Cache
```

**步骤：**
1. 完全关闭浏览器
2. 打开文件资源管理器
3. 粘贴上面的路径到地址栏
4. 删除 Cache 文件夹中的所有内容
5. 重新打开浏览器

---

## 📋 最终检查清单

请确认每一项都完成：

- [ ] 升级了 `product_weight_pricing` 和 `pos_gold_pricing` 模块
- [ ] 重启了 Odoo 服务
- [ ] 使用"清空缓存并硬性重新加载"清空了浏览器缓存
- [ ] 或者使用 Ctrl+Shift+Delete 清空了所有缓存并关闭重开浏览器
- [ ] 在 Network 标签确认 `pos_pricing_method.js` 状态是 200（不是 cached）
- [ ] 在 POS 中测试了产品

---

## 💡 关键点

**问题根源：**
- 前端 JavaScript 代码被浏览器缓存
- 即使后端数据正确，旧的前端代码不会调用新的逻辑

**解决方案：**
1. 升级模块（版本号变化会触发重新加载）
2. 彻底清空浏览器缓存
3. 验证新代码已加载

---

**立即开始步骤 1！** 🚀

