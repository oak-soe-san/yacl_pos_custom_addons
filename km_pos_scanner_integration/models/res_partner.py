from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    surname = fields.Char('Surname')
    forenames = fields.Char('Forenames') 
    date_of_birth = fields.Char('Date of Birth')
    expiry_date = fields.Char('Expiry Date')
    issue_date = fields.Char('Issue Date') 
    document = fields.Char('Document')
    doc_number = fields.Char('Doc. Number')
    issuing_state = fields.Char('Issuing State')
    nationality = fields.Char('Nationality')
    address_street = fields.Char('Address Street')
    address_city = fields.Char('Address City')
    address_state = fields.Char('Address State')
    address_postal_code = fields.Char('Address Postal Code')
    address_country = fields.Char('Address Country')
    height = fields.Char('Height')
    weight = fields.Char('Weight')
    hair_color = fields.Char('Hair Color')
    eye_color = fields.Char('Eye Color')
    flight_date = fields.Char('Flight Date')
    flight_number = fields.Char('Flight Number')
    gender = fields.Selection(string='Gender', selection=[('male', 'Male'),('female','Female'),('other','Other')])