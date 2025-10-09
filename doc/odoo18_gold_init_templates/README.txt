Odoo 18 Gold Products Initialization Templates
=============================================

Import order (very important):
1) pos.category → pos_category.csv
2) product.attribute → product_attribute.csv
3) product.attribute.value → product_attribute_value.csv
4) product.template → product_template.csv
5) product.template.attribute.line (optional, auto-generate variants) → product_template_attribute_line.csv
6) product.product (optional if step 5 is used) → product_product.csv
7) stock.production.lot (per-piece serials) → stock_production_lot.csv
8) metal.pricelist (if using pos_gold_pricing) → metal_pricelist.csv

Notes:
- Use developer mode during import.
- '/id' columns refer to external IDs defined in previous CSVs.
- Units:
  - per piece: uom.product_uom_unit (to_weight=0)
  - per weight: uom.product_uom_kgm (to_weight=1), list_price = price_per_gram * 1000 (yuan/kg).
- After imports, close & reopen the POS session (or Sync) to refresh cache.
- Lots/Serials columns like net_gold_weight, wage_type, etc. come from the pos_gold_pricing module.