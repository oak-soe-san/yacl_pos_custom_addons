from odoo import fields, models, api

class CustomPrinter(models.Model):
    _name = 'custom.printer'
    _rec_name = 'ip_address'
    _description = 'Custom Printer'

    ip_address = fields.Char('IP Address')
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company, readonly=True)
    active = fields.Boolean('Active', default=True)

    def get_printer_ips(self, pos_session_id=False):
        company_id = (self.env.company.id)
        domain = ['&', ('active', '=', True), ('company_id', '=', company_id)]
        custom_printers = self.env['custom.printer'].sudo().search(domain)
        ip_addresses = custom_printers.mapped('ip_address')
        return ip_addresses
