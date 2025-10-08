/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

const _superAddLineToOrder = PosStore.prototype.addLineToOrder;

patch(PosStore.prototype, {
    async addLineToOrder(vals, order, opts = {}, configure = true) {
        let productRecord = vals.product_id;
        if (typeof productRecord === "number") {
            productRecord = this.data.models["product.product"].get(productRecord);
        }

        const pricingMethod = productRecord
            ? productRecord.pos_pricing_method ??
              productRecord.product_tmpl_id?.pos_pricing_method ??
              productRecord.raw?.pos_pricing_method
            : undefined;

        if (
            productRecord &&
            (vals.price_unit === undefined || vals.price_unit === null) &&
            pricingMethod === "by_weight"
        ) {
            try {
                const companyId = this.company?.id || false;
                const priceData = await this.data.call(
                    "product.product",
                    "pos_compute_price_by_weight",
                    [[productRecord.id], companyId]
                );

                if (priceData) {
                    const weightQty = Number(priceData.weight_g);
                    const unitPrice = Number(priceData.unit_price);

                    if (
                        !Number.isNaN(weightQty) &&
                        weightQty > 0 &&
                        (vals.qty === undefined || vals.qty === 1)
                    ) {
                        vals.qty = weightQty;
                    }

                    if (!Number.isNaN(unitPrice) && unitPrice > 0) {
                        vals.price_unit = unitPrice;
                        vals.price_type = "manual";
                    }
                }
            } catch (error) {
                console.warn(
                    "product_weight_pricing: failed to compute weight-based price",
                    error
                );
            }
        }

        return await _superAddLineToOrder.call(this, vals, order, opts, configure);
    },
});

