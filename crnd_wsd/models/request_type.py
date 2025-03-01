from odoo import models, fields


class RequestType(models.Model):
    _inherit = "request.type"

    website_comments_closed = fields.Boolean(
        'Are comments not available?', default=False,
        help="Disable website comments on closed requests")

    # Request type has no websitepublish url yet, so we just need
    # website_published field, thus implement it in explicit way here insetead
    # of inheriting from "website.published.mixin"
    website_published = fields.Boolean(
        'Visible in Website', copy=False, index=True)
    website_ids = fields.Many2many('website')

    # Help message for request text
    website_request_text_help = fields.Text()
    # Custom title for request
    website_request_title = fields.Char()
    # Custom label for request text editor
    website_custom_label_editor = fields.Html()
    website_custom_congratulation_note = fields.Html()

    selection_priority_view = fields.Selection(
        [('selection', 'Selection'),
         ('star', 'Star bar')], default='selection', required=True)

    def website_publish_button(self):
        for rec in self:
            rec.website_published = not rec.website_published
