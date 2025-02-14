from odoo import fields, models

class KitchenBarSlip(models.Model):
    _inherit = "kitchen.bar.slip"

    active = fields.Boolean('Active', default=True)
    ip_address = fields.Char('IP Address')

    def get_printer_ips_bar(self):
        company_id = (self.env.company.id)
        domain = ['&', ('active', '=', True), ('company_id', '=', company_id), ('printer_type', '=', 'bar')]
        custom_printers = self.env['kitchen.bar.slip'].sudo().search(domain)
        ip_addresses = custom_printers.mapped('ip_address')
        print(ip_addresses)
        return ip_addresses

    def get_printer_ips_kitchen(self):
        company_id = (self.env.company.id)
        domain = ['&', ('active', '=', True), ('company_id', '=', company_id), ('printer_type', '=', 'kitchen')]
        custom_printers = self.env['kitchen.bar.slip'].sudo().search(domain)
        ip_addresses = custom_printers.mapped('ip_address')
        print(ip_addresses)
        return ip_addresses
