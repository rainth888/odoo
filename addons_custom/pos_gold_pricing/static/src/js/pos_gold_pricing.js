
/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Orderline } from "@point_of_sale/app/store/models";

const { patch } = registry.category("models");

patch(Orderline.prototype, "pos_gold_pricing_Orderline", {
    setPackLotLines(newPackLotLines) {
        const res = this._super(newPackLotLines);
        try {
            // 只在选择了 lot/serial 时尝试算价
            const lots = this.getLots ? this.getLots() : (this.pack_lot_lines || []);
            const lotName = lots && lots.length ? (lots[0].lot_name || lots[0].name) : null;
            if (!lotName) {
                return res;
            }
            const companyId = (this.pos && this.pos.company && this.pos.company.id) || false;
            // 通过 RPC 让服务器按 lot 计算售价（避免前端预加载数据）
            if (this.pos && typeof this.pos.rpc === "function") {
                this.pos.rpc({
                    model: "stock.production.lot",
                    method: "pos_compute_price_by_lot",
                    args: [lotName, companyId],
                }).then((out) => {
                    if (out && typeof out.price === "number" && !isNaN(out.price)) {
                        this.setUnitPrice(out.price);
                    }
                }).catch((e) => {
                    console.warn("POS gold pricing RPC failed:", e);
                });
            }
        } catch (e) {
            console.warn("POS gold pricing setPackLotLines failed:", e);
        }
        return res;
    },
});
