from odoo import api, models
from odoo.tools.float_utils import float_round


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        if "weight" not in fields:
            fields.append("weight")
        return fields

    def pos_compute_price_by_weight(self, company_id=False):
        self.ensure_one()
        template = self.product_tmpl_id
        if template.pos_pricing_method != "by_weight":
            return {}

        company = (
            self.env["res.company"].browse(company_id)
            if company_id
            else self.env.company
        )
        if not company:
            company = self.env.company

        weight_kg = self.weight or template.weight or 0.0
        weight_g = float_round(weight_kg * 1000.0, precision_digits=3)

        metal_type_id = getattr(template, "default_metal_type_id", False)
        metal_type_code = getattr(template, "default_metal_type", False)
        metal_type_ref = (
            metal_type_id.id
            if metal_type_id
            else metal_type_code or "au_9999"
        )

        price_per_g, factor = self.env["metal.pricelist"].sudo().get_price(
            company.id, metal_type_ref
        )
        factor = factor or 1.0
        unit_price = float_round(price_per_g * factor, precision_digits=2)

        return {
            "weight_g": weight_g,
            "unit_price": unit_price,
            "price_per_g": price_per_g,
            "fineness_factor": factor,
        }

