from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError, UserError


class PosConfig(models.Model):
	_inherit = 'pos.config'

	print_multi_receipt = fields.Boolean(string="Print Multi Receipt")
	no_of_receipt = fields.Integer(string="Multi Receipt Count", required=True)

	@api.constrains('no_of_receipt')
	def _check_count_receipt(self):
		for pos_config in self:
			if pos_config.no_of_receipt <= 0:
				raise ValidationError(
					_('Please Enter Correct Number Of Receipt Count. (It Should Be > 0)'))


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	pos_print_multi_receipt = fields.Boolean(related='pos_config_id.print_multi_receipt', readonly=False)
	pos_no_of_receipt = fields.Integer(related='pos_config_id.no_of_receipt', readonly=False, required=True)