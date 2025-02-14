from odoo import _, api, fields, models


class RoundingResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    rounding_configuration = fields.Selection(
        related='pos_config_id.rounding_configuration', readonly=False, required=True)


class RoundingPosConfig(models.Model):
    _inherit = 'pos.config'

    rounding_configuration = fields.Selection(
        [('default', 'Default'), ('rounding_hide', 'Hide Rounding on Receipt')],
        default='default', required=True)

    # rounding_configuration = fields.Selection(
    #     [('default', 'Default'), ('all_tax', 'Show All Taxes'), ('only_total', 'Only Total Amount of Taxes'),
    #      ('hide_tax', 'Hide All Taxes Detail')],
    #     default='default', required=True,
    #     help="Tax Configuration. The following values are available:\n"
    #          "- 'Default': It works according to the default flow\n"
    #          "- 'Show All Taxes': It shows various taxes and its amount doesn't show the total amount of taxes\n"
    #          "- 'Only Total Amount': It only shows the total amount of all taxes\n"
    #          "- 'Hide All Tax Details': It hides all taxes detail")
