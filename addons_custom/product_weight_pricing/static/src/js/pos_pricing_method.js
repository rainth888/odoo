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

function trimDecimalZeros(formatted) {
    if (!formatted) {
        return formatted;
    }
    return formatted.replace(/([.,]0+)(?!\d)/u, "");
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
            console.log('[POS Weight Pricing] 检测到 By Weight 产品:', productRecord.name);
            console.log('[POS Weight Pricing] Product ID:', productRecord.id);
            console.log('[POS Weight Pricing] Pricing Method:', pricingMethod);
            
            try {
                const companyId = this.company?.id || false;
                console.log('[POS Weight Pricing] Company ID:', companyId);
                console.log('[POS Weight Pricing] 调用 RPC: pos_compute_price_by_weight');
                
                const priceData = await this.data.call(
                    "product.product",
                    "pos_compute_price_by_weight",
                    [[productRecord.id], companyId]
                );

                console.log('[POS Weight Pricing] RPC 返回数据:', priceData);

                if (priceData) {
                    const productWeightKg = toNumber(
                        productRecord.weight ?? productRecord.product_tmpl_id?.weight
                    );
                    const weightInfo = {
                        weight_g: toNumber(priceData.weight_g) || toNumber(productWeightKg * 1000),
                        unit_price: toNumber(priceData.unit_price),
                        price_per_g: toNumber(priceData.price_per_g),
                        fineness_factor: toNumber(priceData.fineness_factor || priceData.factor, 1),
                        unit_label:
                            productRecord.uom_id?.name ||
                            productRecord.product_tmpl_id?.uom_id?.name ||
                            "",
                    };

                    if (!weightInfo.price_per_g && weightInfo.unit_price > 0) {
                        weightInfo.price_per_g = weightInfo.unit_price;
                    }

                    if (
                        weightInfo.weight_g > 0 &&
                        (vals.qty === undefined || vals.qty === null || vals.qty === 1)
                    ) {
                        vals.qty = weightInfo.weight_g;
                    } else if (!vals.qty && weightInfo.weight_g > 0) {
                        vals.qty = weightInfo.weight_g;
                    }

                    if (weightInfo.unit_price > 0) {
                        vals.price_unit = weightInfo.unit_price;
                        vals.price_type = "manual";
                    } else if (vals.price_unit === 0) {
                        delete vals.price_unit;
                    }

                    vals._weight_pricing = weightInfo;
                    console.log('[POS Weight Pricing] ✓ Weight Info 已设置:', weightInfo);
                    console.log('[POS Weight Pricing] ✓ vals.qty =', vals.qty);
                    console.log('[POS Weight Pricing] ✓ vals.price_unit =', vals.price_unit);
                } else {
                    console.warn('[POS Weight Pricing] ⚠ RPC 返回数据为空');
                }
            } catch (error) {
                console.error(
                    "[POS Weight Pricing] ✗ RPC 调用失败:",
                    error
                );
            }

            if (!vals._weight_pricing) {
                const fallbackWeightKg = toNumber(
                    productRecord.weight ?? productRecord.product_tmpl_id?.weight
                );
                const fallbackWeightG =
                    fallbackWeightKg > 0 ? fallbackWeightKg * 1000 : toNumber(vals.qty) || 0;
                const fallbackUnit =
                    productRecord.uom_id?.name || productRecord.product_tmpl_id?.uom_id?.name || "";
                const fallbackUnitPrice = toNumber(vals.price_unit);
                if (fallbackWeightG || fallbackUnitPrice) {
                    vals._weight_pricing = {
                        weight_g: fallbackWeightG,
                        unit_price: fallbackUnitPrice || undefined,
                        price_per_g: fallbackUnitPrice || undefined,
                        fineness_factor: 1,
                        unit_label: fallbackUnit,
                    };
                }
            }
            if (
                vals._weight_pricing?.weight_g > 0 &&
                (vals.qty === undefined || vals.qty === null || vals.qty === 1)
            ) {
                vals.qty = vals._weight_pricing.weight_g;
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

        const weightData = this._weight_pricing || {};
        const unitLabel = data.unit || weightData.unit_label || "";
        
        console.log('[POS Weight Display] getDisplayData 调用');
        console.log('[POS Weight Display] isWeightPriced:', this.isWeightPriced());
        console.log('[POS Weight Display] _weight_pricing:', this._weight_pricing);
        
        if (this.isWeightPriced()) {
            const decimals = this.models["decimal.precision"].find(
                (dp) => dp.name === "Product Unit of Measure"
            )?.digits || 2;
            const parsedWeight = toNumber(weightData.weight_g);
            const grams = parsedWeight > 0 ? parsedWeight : this.qty;
            const qtyStr = grams
                ? trimDecimalZeros(formatFloat(grams, { digits: [69, decimals] }))
                : "";
            let pricePerUnit =
                weightData.price_per_g && weightData.price_per_g > 0
                    ? weightData.price_per_g
                    : weightData.unit_price && grams
                    ? weightData.unit_price
                    : this.price_unit;
            let unitPriceLabel = "";
            if (pricePerUnit && this.currency) {
                unitPriceLabel = trimDecimalZeros(
                    formatCurrency(pricePerUnit, this.currency)
                );
            } else if (data.unitPrice) {
                unitPriceLabel = data.unitPrice;
            }

            if (unitLabel && unitPriceLabel) {
                unitPriceLabel = `${unitPriceLabel}/${unitLabel}`;
            }

            if (qtyStr && unitPriceLabel) {
                data.weightPricingLabel = `${unitPriceLabel} x ${qtyStr} ${unitLabel}`.trim();
                console.log('[POS Weight Display] ✓ weightPricingLabel 已生成:', data.weightPricingLabel);
            } else {
                console.warn('[POS Weight Display] ⚠ weightPricingLabel 未生成');
                console.log('  - qtyStr:', qtyStr);
                console.log('  - unitPriceLabel:', unitPriceLabel);
            }
            if (qtyStr) {
                data.qty = qtyStr;
            }
            if (unitLabel) {
                data.unit = unitLabel;
            }
        }

        console.log('[POS Weight Display] 最终 displayData:', data);
        return data;
    },
});

