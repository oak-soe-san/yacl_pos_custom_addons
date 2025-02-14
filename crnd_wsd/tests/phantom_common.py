from odoo.addons.generic_mixin.tests.common import WebTourCase

from odoo.addons.generic_mixin.tests.common import deactivate_records_for_model


class TestPhantomTour(WebTourCase):

    def setUp(self):
        super(TestPhantomTour, self).setUp()

        # Disable assets from uninstalled modules
        deactivate_records_for_model(self.env, 'ir.asset')

    def _enable_use_services_setting(self):
        (
            self.env.ref('base.group_user') +
            self.env.ref('base.group_portal') +
            self.env.ref('base.group_public')
        ).write({
            'implied_ids': [
                (4,
                 self.env.ref(
                     'generic_request.group_request_use_services').id),
            ]
        })

    def _disable_use_services_setting(self):
        # Disable checkbox for using services
        (
            self.env.ref('base.group_user') +
            self.env.ref('base.group_portal') +
            self.env.ref('base.group_public')
        ).write({
            'implied_ids': [
                (3,
                 self.env.ref(
                     'generic_request.group_request_use_services').id),
            ]
        })

        # Also, clear Services from all Categories and Types
        # this is needed for tests that do not expect serivices.
        request_category_ids = self.env['request.category'].search([])
        request_type_ids = self.env['request.type'].search([])

        request_category_ids.write({
            'service_ids': [(5, 0)]
        })
        request_type_ids.write({
            'service_ids': [(5, 0)]
        })

    def _test_phantom_tour(self, start_url, tour_name, **kw):
        """ Wrapper to run web tours
        """
        return self.run_js_tour(start_url, tour_name, **kw)

    def _test_phantom_tour_requests(self, start_url, tour_name, **kw):
        """ Same as _test_phantom_tour but returns list of requests
            generated by tour
        """
        requests_before = self.env['request.request'].search([])
        self._test_phantom_tour(start_url, tour_name, **kw)
        requests_new = self.env['request.request'].search(
            [('id', 'not in', requests_before.ids)])
        return requests_new
