/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { formatFloat } from "@web/core/utils/numbers";
import { formatCurrency } from "@point_of_sale/app/models/utils/currency";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { PosStore } from "@point_of_sale/app/store/pos_store";

const _superAddLineToOrder = PosStore.prototype.addLineToOrder;
const _superGetDisplayData = PosOrderline.prototype.getDisplayData;

function toNumber(value, fallback = 0) {
    const numeric = Number(value);
    return Number.isFinite(numeric) ? numeric : fallback;
}

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

        if (productRecord && pricingMethod === "by_weight") {
            try {
                const companyId = this.company?.id || false;
                const priceData = await this.data.call(
                    "product.product",
                    "pos_compute_price_by_weight",
                    [[productRecord.id], companyId]
                );

                if (priceData) {
                    const weightInfo = {
                        weight_g: toNumber(priceData.weight_g),
                        unit_price: toNumber(priceData.unit_price),
                        price_per_g: toNumber(priceData.price_per_g),
                        fineness_factor: toNumber(priceData.fineness_factor || priceData.factor, 1),
                    };

                    if (
                        weightInfo.weight_g > 0 &&
                        (vals.qty === undefined || vals.qty === null || vals.qty === 1)
                    ) {
                        vals.qty = weightInfo.weight_g;
                    }

                    if (weightInfo.unit_price > 0) {
                        vals.price_unit = weightInfo.unit_price;
                        vals.price_type = "manual";
                    } else {
                        delete vals.price_unit;
                    }

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

        const weightData = this._weight_pricing;
        const unitLabel = data.unit || "";
        if (this.isWeightPriced() && weightData && unitLabel) {
            const qtyStr = this._getWeightQtyDisplay();
            let unitPriceLabel = data.unitPrice || "";
            if (weightData.price_per_g && this.currency) {
                unitPriceLabel = `${formatCurrency(weightData.price_per_g, this.currency)}/${unitLabel}`;
            } else if (unitPriceLabel) {
                unitPriceLabel = `${unitPriceLabel}/${unitLabel}`;
            }
            if (qtyStr && unitPriceLabel) {
                data.weightPricingLabel = `${unitPriceLabel} x ${qtyStr} ${unitLabel}`;
            }
        }

        return data;
    },
});

