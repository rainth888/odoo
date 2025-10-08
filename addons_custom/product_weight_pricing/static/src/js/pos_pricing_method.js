/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { formatFloat } from "@web/core/utils/numbers";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { PosStore } from "@point_of_sale/app/store/pos_store";

const _superAddLineToOrder = PosStore.prototype.addLineToOrder;
const _superGetDisplayData = PosOrderline.prototype.getDisplayData;

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
                    const weightInfo = {
                        weight_g: Number.isFinite(weightQty) ? weightQty : 0,
                        unit_price: Number.isFinite(unitPrice) ? unitPrice : 0,
                        price_per_g: Number(priceData.price_per_g || 0),
                        fineness_factor: Number(priceData.fineness_factor || priceData.factor || 1),
                    };

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

                    // Preserve the raw data for UI display (Base.setup keeps fields prefixed with _)
                    vals._weight_pricing = weightInfo;
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

patch(PosOrderline.prototype, {
    /**
     * True when the linked product should display the By Weight label.
     */
    isWeightPriced() {
        const product = this.product_id;
        const tmplMethod = product?.product_tmpl_id?.pos_pricing_method || product?.raw?.pos_pricing_method;
        return (product?.pos_pricing_method || tmplMethod) === "by_weight";
    },

    /**
     * Returns the formatted quantity (in grams) for By Weight products.
     */
    _getWeightQtyDisplay() {
        const weightData = this._weight_pricing;
        const qtySource =
            weightData?.weight_g ?? this.qty ?? 0;
        const decimals = this.models["decimal.precision"].find((dp) => dp.name === "Product Unit of Measure")?.digits || 2;
        return formatFloat(qtySource, { digits: [69, decimals] });
    },

    getDisplayData() {
        const data = _superGetDisplayData.apply(this, arguments);

        if (this.isWeightPriced() && data.unit === "g") {
            const qtyStr = this._getWeightQtyDisplay();
            const unitPrice = data.unitPrice || "";
            if (qtyStr && unitPrice) {
                data.weightPricingLabel = `${unitPrice}/${data.unit} x ${qtyStr}${data.unit}`;
            }
        }

        return data;
    },
});

