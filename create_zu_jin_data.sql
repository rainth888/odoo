-- ========================================
-- 创建"足金"金属类型和每日金价
-- ========================================

-- 1. 创建"足金"金属类型（如果不存在）
INSERT INTO metal_type (name, code, fineness_factor, sequence, active, create_date, write_date, create_uid, write_uid)
SELECT '足金', 'zu_jin', 1.0, 11, true, NOW(), NOW(), 1, 1
WHERE NOT EXISTS (
    SELECT 1 FROM metal_type WHERE name = '足金' OR code = 'zu_jin'
);

-- 验证"足金"金属类型已创建
SELECT '✓ 足金金属类型' as status, id, name, code, fineness_factor 
FROM metal_type 
WHERE name = '足金';

-- 2. 创建"足金"的每日金价（如果不存在）
-- 先获取金属类型ID和公司ID
DO $$
DECLARE
    v_metal_type_id INTEGER;
    v_company_id INTEGER;
BEGIN
    -- 获取"足金"金属类型ID
    SELECT id INTO v_metal_type_id FROM metal_type WHERE name = '足金' LIMIT 1;
    
    -- 获取第一个公司ID
    SELECT id INTO v_company_id FROM res_company ORDER BY id LIMIT 1;
    
    -- 插入今天的金价（如果不存在）
    IF v_metal_type_id IS NOT NULL AND v_company_id IS NOT NULL THEN
        INSERT INTO metal_pricelist (
            name, 
            metal_type_id, 
            price_per_g, 
            fineness_factor, 
            effective_date, 
            company_id, 
            active,
            create_date,
            write_date,
            create_uid,
            write_uid
        )
        SELECT 
            '足金-' || CURRENT_DATE,
            v_metal_type_id,
            512.0,
            1.0,
            CURRENT_DATE,
            v_company_id,
            true,
            NOW(),
            NOW(),
            1,
            1
        WHERE NOT EXISTS (
            SELECT 1 
            FROM metal_pricelist 
            WHERE metal_type_id = v_metal_type_id 
              AND effective_date = CURRENT_DATE
              AND company_id = v_company_id
        );
        
        RAISE NOTICE '✓ 足金每日金价已创建或已存在';
    ELSE
        RAISE EXCEPTION '✗ 无法创建金价：metal_type_id=%, company_id=%', v_metal_type_id, v_company_id;
    END IF;
END $$;

-- 验证"足金"每日金价已创建
SELECT 
    '✓ 足金每日金价' as status,
    mp.id,
    mp.name,
    mt.name as metal_type,
    mp.price_per_g,
    mp.effective_date,
    mp.active
FROM metal_pricelist mp
JOIN metal_type mt ON mt.id = mp.metal_type_id
WHERE mt.name = '足金'
ORDER BY mp.effective_date DESC
LIMIT 1;

-- ========================================
-- 最终验证
-- ========================================

-- 检查完整配置
SELECT 
    '=== 配置检查完成 ===' as info,
    (SELECT COUNT(*) FROM metal_type WHERE name = '足金') as 金属类型数量,
    (SELECT COUNT(*) FROM metal_pricelist mp 
     JOIN metal_type mt ON mt.id = mp.metal_type_id 
     WHERE mt.name = '足金' AND mp.active = true) as 金价记录数量;

