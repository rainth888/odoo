#!/usr/bin/env python3
"""
测试 By Weight 产品价格计算
运行方式: ./odoo-bin shell -c odoo.conf -d your_database < test_by_weight_pricing.py
或在 shell 中直接执行
"""

print("=" * 80)
print("测试 By Weight 产品价格计算")
print("=" * 80)

# 1. 检查"足金"金属类型
print("\n【步骤 1】检查"足金"金属类型")
print("-" * 80)
metal_type = env['metal.type'].search([('name', '=', '足金')], limit=1)
if metal_type:
    print(f"✓ 找到金属类型: {metal_type.name}")
    print(f"  - ID: {metal_type.id}")
    print(f"  - Code: {metal_type.code}")
    print(f"  - Fineness Factor: {metal_type.fineness_factor}")
    print(f"  - Active: {metal_type.active}")
else:
    print("✗ 未找到"足金"金属类型！")
    print("\n请创建：")
    print("  1. 进入 POS → Metal Pricing → Metal Types")
    print("  2. 创建记录：Name=足金, Code=zu_jin, Fineness Factor=1.0")
    print("\n或执行SQL：")
    print("  INSERT INTO metal_type (name, code, fineness_factor, sequence, active)")
    print("  VALUES ('足金', 'zu_jin', 1.0, 11, true);")

# 2. 检查"足金"的每日金价
print("\n【步骤 2】检查"足金"的每日金价")
print("-" * 80)
if metal_type:
    from datetime import date
    today = str(date.today())
    pricelist = env['metal.pricelist'].search([
        ('metal_type_id', '=', metal_type.id),
        ('effective_date', '<=', today),
        ('active', '=', True)
    ], order='effective_date desc', limit=1)
    
    if pricelist:
        print(f"✓ 找到金价记录: {pricelist.name}")
        print(f"  - Metal Type: {pricelist.metal_type_id.name}")
        print(f"  - Price: ￥{pricelist.price_per_g}/g")
        print(f"  - Fineness Factor: {pricelist.fineness_factor}")
        print(f"  - Effective Date: {pricelist.effective_date}")
        print(f"  - Active: {pricelist.active}")
    else:
        print("✗ 未找到"足金"的每日金价！")
        print(f"\n请创建（今天日期：{today}）：")
        print("  1. 进入 POS → Metal Pricing → Daily Metal Prices")
        print(f"  2. 创建记录：Metal Type=足金, Price=512, Effective Date={today}")

# 3. 检查产品
print("\n【步骤 3】检查产品 0520000699")
print("-" * 80)
product = env['product.product'].search([('barcode', '=', '0520000699')], limit=1)

if not product:
    print("✗ 未找到条形码为 0520000699 的产品！")
else:
    print(f"✓ 找到产品: {product.name}")
    print(f"  - ID: {product.id}")
    print(f"  - Barcode: {product.barcode}")
    
    # 检查模板配置
    template = product.product_tmpl_id
    print(f"\n  产品模板配置:")
    print(f"  - Pricing Method: {template.pos_pricing_method or '未设置'}")
    print(f"  - Weight: {product.weight} kg = {product.weight * 1000} g")
    print(f"  - UoM: {product.uom_id.name}")
    
    # 检查属性
    print(f"\n  产品属性:")
    if product.product_template_attribute_value_ids:
        for ptav in product.product_template_attribute_value_ids:
            attr_name = ptav.attribute_id.name
            value_name = ptav.name or ptav.product_attribute_value_id.name
            print(f"    - {attr_name}: {value_name}")
    else:
        print("    (无属性)")
    
    # 4. 测试候选令牌提取
    print("\n【步骤 4】测试属性值到金属类型的匹配")
    print("-" * 80)
    if template.pos_pricing_method == 'by_weight':
        tokens = product._pos_weight_pricing_candidate_tokens()
        print(f"提取的候选令牌: {tokens}")
        
        if tokens:
            print("\n尝试匹配金属类型:")
            for token in tokens:
                matched = env['metal.type'].search([
                    '|',
                    ('code', '=', token),
                    ('name', '=', token)
                ], limit=1)
                if matched:
                    print(f"  ✓ '{token}' → {matched.name} (ID: {matched.id})")
                else:
                    print(f"  ✗ '{token}' → 未匹配")
        
        # 5. 测试金属类型解析
        print("\n【步骤 5】测试金属类型解析")
        print("-" * 80)
        metal_type_ref = product._pos_weight_pricing_resolve_metal_type_ref(template)
        print(f"解析结果: {metal_type_ref}")
        
        if isinstance(metal_type_ref, int):
            resolved_metal = env['metal.type'].browse(metal_type_ref)
            print(f"  → 金属类型: {resolved_metal.name} (Code: {resolved_metal.code})")
        else:
            print(f"  → 使用代码: {metal_type_ref}")
        
        # 6. 测试价格获取
        print("\n【步骤 6】测试价格获取")
        print("-" * 80)
        company_id = env.company.id
        price_per_g, factor = env['metal.pricelist'].get_price(company_id, metal_type_ref)
        print(f"Company ID: {company_id}")
        print(f"Metal Type Ref: {metal_type_ref}")
        print(f"Price per gram: ￥{price_per_g}/g")
        print(f"Fineness Factor: {factor}")
        
        # 7. 测试完整价格计算
        print("\n【步骤 7】测试完整价格计算")
        print("-" * 80)
        try:
            price_data = product.pos_compute_price_by_weight(company_id=company_id)
            print("计算结果:")
            print(f"  - weight_g: {price_data.get('weight_g')} g")
            print(f"  - price_per_g: ￥{price_data.get('price_per_g')}/g")
            print(f"  - unit_price: ￥{price_data.get('unit_price')}")
            print(f"  - fineness_factor: {price_data.get('fineness_factor')}")
            
            total = price_data.get('price_per_g', 0) * price_data.get('weight_g', 0)
            print(f"\n  计算总价: ￥{total:,.2f}")
            print(f"  期望显示: ￥{price_data.get('price_per_g')}/g x {price_data.get('weight_g')} g")
        except Exception as e:
            print(f"✗ 计算失败: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"✗ 产品的 Pricing Method 不是 'by_weight'，而是: {template.pos_pricing_method}")
        print("\n请设置：")
        print("  1. 打开产品")
        print("  2. General Information 标签页")
        print("  3. Sales Price 下方选择 'By Weight'")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)

