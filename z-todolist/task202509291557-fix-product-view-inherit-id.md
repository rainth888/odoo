# task202509291557-fix-product-view-inherit-id

Summary
- Fix install error for `product_weight_pricing`: bad `inherit_id` to non-existent `product.product_template_only_form` on Odoo 18.

Assumptions & Environment
- Odoo 18.0, DB `odoo` on 127.0.0.1:5432 with user `proot`.
- Addons path includes `addons_custom` where module lives.
- Goal: minimal change, no POS UI breakage.

Steps Executed
1) Reproduced error from user log; stack points to `views/product_template_views.xml` line 2.
2) Searched for external IDs used:
   - Found references to `product.product_template_only_form` and `product.product_template_form_view`.
3) Chose stable target `product.product_template_form_view` (exists on Odoo 18).
4) Simplified XML to a single inheritance to `product_template_form_view` and removed fallback block to avoid unresolved refs.

Files Changed
- Updated: `addons_custom/product_weight_pricing/views/product_template_views.xml`
  - Change: set `<field name="inherit_id" ref="product.product_template_form_view"/>` and remove duplicate fallback record.

Commands to Verify
- Update/install the module:
  `python odoo-bin --addons-path=addons,addons_custom -d odoo --db_host=127.0.0.1 --db_port=5432 --db_user=proot --db_password=proot -u product_weight_pricing`

Notes & Follow-ups
- `addons_custom/pos_gold_pricing/views/product_template_views.xml` contains the same optional reference to `product.product_template_only_form`. Apply identical change there if that module will be installed to prevent similar failures.
- No changes to business logic or POS assets.

