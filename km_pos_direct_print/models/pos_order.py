from odoo import models, fields

from PIL import Image
Image.register_extension("PDF", ".pdf")
from PIL import PdfImagePlugin
Image.register_save_all("PDF", PdfImagePlugin._save_all)

import io, base64
from io import BytesIO

from printnodeapi.gateway import Gateway
from odoo.exceptions import UserError

class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _get_fields_for_order_line(self):
        fields = super(PosOrder, self)._get_fields_for_order_line()
        fields.extend(['printed', 'printed_qty', 'printed_total_qty'])
        return fields

    # def action_receipt_to_print_node(self, name, printer_type, ticket):
    #     domain_name = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #     custom_addons_path = self.env['ir.config_parameter'].sudo().get_param('custom.addons.path') # /opt/odoo16/custom-addons
    #     OUTPUT_FILENAME = str(custom_addons_path) + '/km_pos_direct_print/static/' + str(name) + '.pdf'
    #     pil_images = []
    #
    #     pil_images.append(Image.open(io.BytesIO(base64.decodebytes(bytes(ticket, "utf-8")))))
    #     convert_pil_images = []
    #
    #     for pil_image in pil_images:
    #         convert_pil_images.append(pil_image.convert('RGB'))
    #
    #     image_list = convert_pil_images[1:]
    #
    #     try:
    #         convert_pil_images[0].save(OUTPUT_FILENAME, save_all = True, append_images = image_list)
    #     except Exception as e:
    #         raise UserError('File Write Error ' + str(e))
    #
    #     print_node_api = self.env['ir.config_parameter'].sudo().get_param('api_key_print_node')
    #     pos_session = self.env['pos.session'].browse(name)
    #     if printer_type == 'bar':
    #         printer_id = pos_session.config_id.bar_printer_id
    #     else:
    #         printer_id = pos_session.config_id.kitchen_printer_id
    #
    #     printer_det = self.env['printer.details'].browse(int(printer_id))
    #     gateway = Gateway(url='https://api.printnode.com/', apikey=print_node_api)
    #
    #     base_urls = str(domain_name) + '/km_pos_direct_print/static/' + str(name) + '.pdf'
    #     #raise UserError('OUTPUT_FILENAME => ' + str(OUTPUT_FILENAME) + ' base_urls => ' + str(base_urls))
    #     result = None
    #     try:
    #         result = gateway.PrintJob(printer=int(printer_det.id_of_printer), options={"copies": 1, "rotate": 0}, uri=base_urls)
    #     except Exception as e:
    #         raise UserError('Print Job Error ' + str(e))
    #
    #     return True

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    printed = fields.Boolean('Printed')
    printed_qty = fields.Integer('Printed Qty')
    printed_total_qty = fields.Integer('Printed Total Qty')