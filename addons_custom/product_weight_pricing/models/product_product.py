import re

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

    def _pos_weight_pricing_candidate_tokens(self):
        """Return ordered tokens that may map attribute values to metal types."""
        self.ensure_one()

        candidates = []
        keywords = ["metal", "成色", "金种", "纯度", "fineness", "金属"]

        for ptav in self.product_template_attribute_value_ids:
            attribute_label = (ptav.attribute_id.display_name or ptav.attribute_id.name or "").strip()
            if not attribute_label:
                continue

            normalized_label = attribute_label.lower()
            if not any(keyword in normalized_label for keyword in keywords):
                continue

            raw_values = {
                (ptav.display_name or "").strip(),
                (ptav.name or "").strip(),
                (ptav.product_attribute_value_id.display_name or "").strip(),
                (ptav.product_attribute_value_id.name or "").strip(),
            }

            for raw in filter(None, raw_values):
                tokens = {raw}
                if ":" in raw:
                    tokens.add(raw.split(":")[-1].strip())
                if "：" in raw:
                    tokens.add(raw.split("：")[-1].strip())

                match = re.search(r"\(([^)]+)\)", raw) or re.search(r"（([^）]+)）", raw)
                if match:
                    tokens.add(match.group(1).strip())

                for token in filter(None, tokens):
                    if token not in candidates:
                        candidates.append(token)

        return candidates

    def _pos_weight_pricing_resolve_metal_type_ref(self, template):
        """Determine which metal type should be used for the POS pricing."""
        metal_type = getattr(template, "default_metal_type_id", False)
        if metal_type:
            return metal_type.id

        metal_type_model = self.env["metal.type"].sudo()
        for token in self._pos_weight_pricing_candidate_tokens():
            metal_type_record = metal_type_model.search([
                "|",
                ("code", "=", token),
                ("name", "=", token),
            ], limit=1)
            if metal_type_record:
                return metal_type_record.id

        legacy_code = getattr(template, "default_metal_type", False)
        if legacy_code:
            return legacy_code

        return "au_9999"

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

        metal_type_ref = self._pos_weight_pricing_resolve_metal_type_ref(template)

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

