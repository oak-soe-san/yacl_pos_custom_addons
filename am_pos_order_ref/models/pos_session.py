from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result.append('ir.sequence')
        return result

    def _loader_params_ir_sequence(self):
        #print('_loader_params_ir_sequencce ', self.config_id.sequence_id.id)
        return {
            'search_params': {
                'domain': [('id', '=', self.config_id.sequence_id.id)]
            },
        }

    def _get_pos_ui_ir_sequence(self, params):
        return self.env['ir.sequence'].search_read(**params['search_params'])