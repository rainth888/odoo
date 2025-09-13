
from odoo import models, fields, api

class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    # 单件差异字段（黄金首饰）
    net_gold_weight = fields.Float("净金重(g)", digits=(16, 4))
    gross_weight    = fields.Float("总重(g)", digits=(16, 4))
    stone_weight_ct = fields.Float("石重(ct)", digits=(16, 4))
    certificate_no  = fields.Char("证书号")
    wage_value      = fields.Float("工费")
    wage_type       = fields.Selection([('per_g','克工费'), ('per_piece','件工费')], default='per_piece')
    process_technique = fields.Selection([
        ('hard','硬金'), ('3d','3D'), ('5d','5D'), ('5g','5G'), ('enamel','珐琅')
    ], string="工艺")
    metal_type = fields.Selection([
        ('au_9999','Au 999.9'), ('au_999','Au 999'), ('au_au18k','Au 18K'), ('au_au14k','Au 14K')
    ], string="金种/成色", help="用于匹配当日金价；也可从模板继承默认值。")

    def compute_pos_unit_price(self):
        """服务器侧统一算价：净金重×当日金价×成色系数 + 工费"""
        self.ensure_one()
        company_id = self.company_id.id or self.env.company.id
        price_per_g, factor = self.env['metal.pricelist'].get_price(company_id, self.metal_type or 'au_9999')
        gold_part = (self.net_gold_weight or 0.0) * price_per_g * (factor or 1.0)
        if self.wage_type == 'per_g':
            wage = (self.net_gold_weight or 0.0) * (self.wage_value or 0.0)
        else:
            wage = self.wage_value or 0.0
        return round(gold_part + wage, 2)

    @api.model
    def pos_compute_price_by_lot(self, lot_name, company_id=False):
        """供 POS 前端调用。通过 lot 名称返回计算后的售价。"""
        domain = [('name', '=', lot_name)]
        if company_id:
            domain.append(('company_id', '=', company_id))
        lot = self.sudo().search(domain, limit=1)
        if not lot:
            return {"price": 0.0}
        return {"price": lot.compute_pos_unit_price()}
