from odoo import models, fields


class PosOrder(models.Model):
    _inherit = 'pos.order'

    surname = fields.Char('Surname', related="partner_id.surname", readonly=True)
    date_of_birth = fields.Char('Date of Birth', related="partner_id.date_of_birth", readonly=True)
    expiry_date = fields.Char('Expiry Date', related="partner_id.expiry_date", readonly=True)
    doc_number = fields.Char('Doc. Number', related="partner_id.doc_number", readonly=True)
    issuing_state = fields.Char('Issuing State', related="partner_id.issuing_state", readonly=True)
    issue_date = fields.Char('Issue Date', related="partner_id.issue_date", readonly=True) 
    nationality = fields.Char('Nationality', related="partner_id.nationality", readonly=True)
    flight_date = fields.Char('Flight Date', related="partner_id.flight_date", readonly=True)
    flight_number = fields.Char('Flight Number', related="partner_id.flight_number", readonly=True)
    gender = fields.Selection('Gender', related="partner_id.gender", readonly=True)