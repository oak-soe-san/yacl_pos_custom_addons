import base64
from odoo import http
from escpos.printer import Network
import tempfile
import os
import subprocess
import string
import random
from odoo.exceptions import UserError, ValidationError,Warning
import logging

_logger = logging.getLogger(__name__)

class PosPrintIP(http.Controller):
    @http.route('/km_pos_direct_print', type='json', auth='user', csrf=False, website=False)
    def pos_print_ip(self, receipt, printer_type):
        # Decode the base64 encoded image data received from the client
        image_data = base64.b64decode(receipt)

        settings = http.request.env['kitchen.bar.slip'].sudo()

        if printer_type == 'bar':
            printer_ips = settings.get_printer_ips_bar()
        elif printer_type == 'kitchen':
            printer_ips = settings.get_printer_ips_kitchen()
        else:
            # Handle unknown printer types
            printer_ips = []

        # Print to each printer
        for printer_ip in printer_ips:
           # try:
           #     if self.is_printer_online(printer_ip):
           #         self.print_image(image_data, printer_ip)
           #     else:
           #         self.handle_offline_printer(printer_ip)
           # except TimeoutError as e:
           #     self.handle_timeout_error(printer_ip, e)
           self.print_image(image_data, printer_ip)
    
    def is_printer_online(self, printer_ip):
        response = subprocess.run(['ping', '-n', '1', '-w', '1000', printer_ip], capture_output=True, timeout=5)
        return response.returncode == 0

    def handle_offline_printer(self, printer_ip):
        _logger.debug(f"Printer {printer_ip} is offline. Please check the printer connection.")

    def handle_timeout_error(self, printer_ip, error):
        _logger.debug(f"Timeout error occurred when trying to ping printer {printer_ip}: {error}")
    
    def generate_random_text(self, length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

    def print_image(self, image_data, printer_ip):
        # Write the image data to a temporary file
        temp_dir = tempfile.mkdtemp()

        # Define the file path inside the temporary directory
        #file_path = os.path.join(temp_dir, self.generate_random_text(5) + ".png")
        file_path = "/opt/yacl_odoo_16/tmp_slip/" + self.generate_random_text(5) + ".png" 
        with open(file_path, 'wb') as file:

            file.write(image_data)

        # Connect to the printer and send the image for printing
        printer = Network(printer_ip)
        printer.image(file_path)
        printer.cut()
