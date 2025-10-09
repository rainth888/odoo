Odoo 18 Gold — Variants Only (No Lot) Import Templates
=====================================================

Import order:
1) pos.category → pos_category.csv
2) product.attribute → product_attribute.csv
3) product.attribute.value → product_attribute_value.csv
4) product.template → product_template.csv
5) product.template.attribute.line (optional, let Odoo auto-generate variants) → product_template_attribute_line.csv
6) product.product (optional alternative to step 5) → product_product.csv

Key assumptions:
- Weight base unit is GRAM (g). Use External ID: uom.product_uom_gram
- Kilogram (kg) is in the same category with Ratio=1000 and External ID: uom.product_uom_kgm
- Piece unit is Unit(s) with External ID: uom.product_uom_unit
- No lot/serial tracking: tracking='none'
- Per-piece items: uom=unit, to_weight=0, list_price=price per piece
- Per-gram items: uom=gram, to_weight=1, list_price=price per gram

Tips:
- Enable developer mode to see External IDs (View Metadata).
- After imports, refresh/sync POS session.
- Barcodes must be unique across templates/variants.
- If your instance uses different External IDs for UoMs, adjust CSV accordingly.

Generated: 2025-09-16