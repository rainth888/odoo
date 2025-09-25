
/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";

// Keep reference to original method for proper super call
const _orig_setPackLotLines = PosOrderline.prototype.setPackLotLines;

// Odoo 18: setPackLotLines 接收对象参数 { modifiedPackLotLines, newPackLotLines, setQuantity }
patch(PosOrderline.prototype, {
    setPackLotLines(args = {}) {
        const res = typeof _orig_setPackLotLines === "function" ? _orig_setPackLotLines.call(this, args) : undefined;
        try {
            const { newPackLotLines = [] } = args;
            // 优先取新录入的 lot，其次取现有 pack_lot_ids
            let lotName = null;
            if (newPackLotLines.length) {
                lotName = newPackLotLines[0].lot_name || newPackLotLines[0].name || null;
            }
            if (!lotName && this.pack_lot_ids && this.pack_lot_ids.length) {
                lotName = this.pack_lot_ids[0].lot_name || this.pack_lot_ids[0].name || null;
            }
            if (!lotName) return res;

            // 取公司 ID（优先 models 中的 res.company）
            const company = this.models && this.models["res.company"] ? this.models["res.company"].getFirst() : null;
            const companyId = company ? company.id : (this.pos && this.pos.company && this.pos.company.id) || false;

            // 若有 POS rpc 可用则调用服务器定价
            if (this.pos && typeof this.pos.rpc === "function") {
                this.pos
                    .rpc({
                        model: "stock.lot",
                        method: "pos_compute_price_by_lot",
                        args: [lotName, companyId],
                    })
                    .then((out) => {
                        if (out && typeof out.price === "number" && !isNaN(out.price)) {
                            this.set_unit_price(out.price);
                            this.setLinePrice && this.setLinePrice();
                            this.order_id && this.order_id.recomputeOrderData && this.order_id.recomputeOrderData();
                        }
                    })
                    .catch((e) => console.warn("POS gold pricing RPC failed:", e));
            }
        } catch (e) {
            console.warn("POS gold pricing setPackLotLines failed:", e);
        }
        return res;
    },
});
