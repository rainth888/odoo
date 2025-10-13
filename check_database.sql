-- ========================================
-- 检查 POS "足金" 配置
-- ========================================

-- 1. 检查"足金"金属类型是否存在
SELECT 
    '【检查1】足金金属类型' as check_name,
    CASE 
        WHEN COUNT(*) > 0 THEN '✓ 已创建'
        ELSE '✗ 未创建 - 需要创建！'
    END as status,
    COUNT(*) as count
FROM metal_type 
WHERE name = '足金' OR code = 'zu_jin';

-- 显示"足金"金属类型详情
SELECT 
    '足金金属类型详情' as info,
    id, name, code, fineness_factor, sequence, active
FROM metal_type 
WHERE name = '足金' OR code = 'zu_jin';

-- 2. 检查"足金"的每日金价是否存在
SELECT 
    '【检查2】足金每日金价' as check_name,
    CASE 
        WHEN COUNT(*) > 0 THEN '✓ 已创建'
        ELSE '✗ 未创建 - 需要创建！'
    END as status,
    COUNT(*) as count
FROM metal_pricelist mp
JOIN metal_type mt ON mt.id = mp.metal_type_id
WHERE mt.name = '足金' 
  AND mp.active = true
  AND mp.effective_date <= CURRENT_DATE;

-- 显示"足金"每日金价详情
SELECT 
    '足金每日金价详情' as info,
    mp.id, mp.name, 
    mt.name as metal_type,
    mp.price_per_g,
    mp.fineness_factor,
    mp.effective_date,
    mp.active
FROM metal_pricelist mp
JOIN metal_type mt ON mt.id = mp.metal_type_id
WHERE mt.name = '足金'
ORDER BY mp.effective_date DESC
LIMIT 5;

-- 3. 检查产品 0520000699 是否存在
SELECT 
    '【检查3】产品0520000699' as check_name,
    CASE 
        WHEN COUNT(*) > 0 THEN '✓ 存在'
        ELSE '✗ 不存在'
    END as status,
    COUNT(*) as count
FROM product_product 
WHERE barcode = '0520000699';

-- 显示产品详情
SELECT 
    '产品详情' as info,
    pp.id, 
    pp.name,
    pp.barcode,
    pp.weight as weight_kg,
    pp.weight * 1000 as weight_g,
    pt.pos_pricing_method
FROM product_product pp
JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE pp.barcode = '0520000699';

-- 4. 检查产品属性
SELECT 
    '【检查4】产品属性' as check_name,
    pa.name as attribute_name,
    pav.name as attribute_value
FROM product_product pp
JOIN product_template_attribute_value_line ptavl ON ptavl.product_id = pp.id
JOIN product_template_attribute_value ptav ON ptav.id = ptavl.product_attribute_value_id
JOIN product_attribute pa ON pa.id = ptav.attribute_id
JOIN product_attribute_value pav ON pav.id = ptav.product_attribute_value_id
WHERE pp.barcode = '0520000699';

-- 5. 显示所有金属类型（参考）
SELECT 
    '【参考】所有金属类型' as info,
    id, name, code, fineness_factor, active
FROM metal_type
WHERE active = true
ORDER BY sequence, name;

-- ========================================
-- 修复 SQL（如果需要）
-- ========================================

-- 如果检查1失败，创建"足金"金属类型：
/*
INSERT INTO metal_type (name, code, fineness_factor, sequence, active, create_date, write_date)
VALUES ('足金', 'zu_jin', 1.0, 11, true, NOW(), NOW());
*/

-- 如果检查2失败，先获取金属类型ID和公司ID：
/*
SELECT id FROM metal_type WHERE name = '足金';  -- 记下这个 ID
SELECT id FROM res_company LIMIT 1;             -- 记下这个 ID

-- 然后插入金价（替换下面的 5 和 1 为实际 ID）：
INSERT INTO metal_pricelist (name, metal_type_id, price_per_g, fineness_factor, effective_date, company_id, active, create_date, write_date)
VALUES ('足金-2024-10-09', 5, 512.0, 1.0, CURRENT_DATE, 1, true, NOW(), NOW());
*/

