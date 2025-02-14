from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_res_partner(self):
        res = super()._loader_params_res_partner()
        res["search_params"]["fields"].append("surname")
        res["search_params"]["fields"].append("forenames")
        res["search_params"]["fields"].append("expiry_date")
        res["search_params"]["fields"].append("date_of_birth")
        res["search_params"]["fields"].append("issue_date")
        res["search_params"]["fields"].append("document")
        res["search_params"]["fields"].append("doc_number")
        res["search_params"]["fields"].append("issuing_state")
        res["search_params"]["fields"].append("nationality")
        res["search_params"]["fields"].append("address_street")
        res["search_params"]["fields"].append("address_city")
        res["search_params"]["fields"].append("address_state")
        res["search_params"]["fields"].append("address_postal_code")
        res["search_params"]["fields"].append("address_country")
        res["search_params"]["fields"].append("height")
        res["search_params"]["fields"].append("weight")
        res["search_params"]["fields"].append("hair_color")
        res["search_params"]["fields"].append("eye_color")
        res["search_params"]["fields"].append("flight_date")
        res["search_params"]["fields"].append("flight_number")
        res["search_params"]["fields"].append("gender")
        return res