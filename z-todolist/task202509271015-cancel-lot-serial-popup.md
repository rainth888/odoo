# task202509271015-cancel-lot-serial-popup

## Summary
Disable the Lot/Serial Number(s) Required prompt in POS when selecting a product, without breaking the POS flow.

## Original Request
there should be cancel the input box 'Lot/Serial Number(s) Requiredd' in the shop when select a product.

tell me how to do it.

## Assumptions
- Odoo 18 POS (OWL) and standard Inventory tracking enabled for some products.
- You want a configuration-first solution; code customization is optional.

## How-To (recommended options)
1) POS configuration (stop asking lots in POS)
- Menu: Point of Sale > Configuration > Settings > select your POS (config_id=4)
- Disable: Lots/Serial Numbers (or similar toggle)
- Save, then restart POS session and hard refresh the POS UI
- Note: If disabled, POS will not prompt for tracked lots. In some versions, tracked products may be disallowed if lots are disabled; if so, combine with option 2.

2) Product-level (remove tracking for POS)
- Menu: Inventory > Products > Products > open the product
- Tab: Inventory > Tracking: set to “No Tracking”
- Save. The POS will no longer require lot/serial input for that product
- Use for products where tracking is not legally/operationally required at sale time

3) Operational workaround (keep tracking in backend, not in POS)
- Duplicate the product: create a POS-facing product with Tracking = No Tracking and visible in POS
- Hide the tracked version from POS (uncheck Available in POS)
- Maintain inventory for the tracked SKU in Warehouse; sell the POS SKU without lot prompts

4) Optional customization (skip popup but keep tracking)
- Create a tiny POS extension module to intercept the lot/serial prompt and auto-continue
- Caveat: May conflict with compliance and stock traceability
- High-level outline (assets in your custom module):
  - JS: patch the order-line lot requirement check to return false in POS context
  - Example locations (varies by version): `@point_of_sale/app/models` and the component handling lot editing
  - Keep the change feature-flagged (e.g., POS config boolean) to avoid surprises

## Verify
- Open POS: `/pos/ui?config_id=4`
- Add the product; the lot/serial prompt should not appear
- If changes don’t reflect, update module and clear assets:
  - WSL: `cd /mnt/d/_projects/odoo.github.rainth888 && source .venv/bin/activate && python odoo-bin -c odoo.conf -u point_of_sale`
  - Hard refresh browser (Ctrl+F5)

## Notes
- WSL path mapping: `D:\\_projects\\odoo.github.rainth888` ↔ `/mnt/d/_projects/odoo.github.rainth888`
- If you need a code patch to skip the popup while keeping tracking enabled, reply and I’ll scaffold a minimal, safe extension.
