from odoo import models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(['is_discount_product'])
        result['search_params']['fields'].extend(['is_ewallet_product'])
        return result

    def _prepare_line(self, order_line):
        """ Derive from order_line the order date, income account, amount and taxes information.

        These information will be used in accumulating the amounts for sales and tax lines.
        """
        def get_income_account(order_line):
            product = order_line.product_id
            income_account = product.with_company(order_line.company_id)._get_product_accounts()['income']
            if not income_account:
                raise UserError(_('Please define income account for this product: "%s" (id:%d).')
                                % (product.name, product.id))
            return order_line.order_id.fiscal_position_id.map_account(income_account)

        tax_ids = order_line.tax_ids_after_fiscal_position\
                    .filtered(lambda t: t.company_id.id == order_line.order_id.company_id.id)
        
        sign = -1 if order_line.qty >= 0 else 1
        price = sign * order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)
        # The 'is_refund' parameter is used to compute the tax tags. Ultimately, the tags are part
        # of the key used for summing taxes. Since the POS UI doesn't support the tags, inconsistencies
        # may arise in 'Round Globally'.
        check_refund = lambda x: x.qty * x.price_unit < 0
        is_refund = check_refund(order_line)

        # KN CUSTOMIZATION FOR GLOBAL DISCOUNT TAX EXCLUSIVE
        if self.config_id.is_global_discount_tax_exclusive and order_line.order_id.amount_total != 0:
            is_discount_or_reward = False
            if order_line.product_id.is_discount_product or order_line.is_reward_line:
                is_discount_or_reward = True
                tax_ids = self.env['account.tax'].search([('name', '=', 'Tax For Global Discount')])

            tax_data = tax_ids.compute_all(price_unit=price, quantity=abs(order_line.qty), currency=self.currency_id, is_refund=is_refund, fixed_multiplicator=sign)
            taxes = tax_data['taxes']

            currency = self.env.company.currency_id
            if not is_discount_or_reward:
                if order_line.global_discount_percentage > 0:
                    for custom_tax in taxes:
                        if custom_tax['amount'] < 0:
                            custom_tax['amount'] = currency.round(-((abs(custom_tax['base']) - (abs(custom_tax['base']) * order_line.global_discount_percentage/100)) * tax_ids.amount/100))
                        else:
                            custom_tax['amount'] = currency.round((abs(custom_tax['base']) - (abs(custom_tax['base']) * order_line.global_discount_percentage/100)) * tax_ids.amount/100)

                        if not order_line.order_id.rounding_error_fix and order_line.order_id.rounding_error != 0:
                            if abs(order_line.order_id.rounding_error) < abs(1):
                                if is_refund:
                                    custom_tax['amount'] = custom_tax['amount'] - order_line.order_id.rounding_error
                                else:
                                    custom_tax['amount'] = custom_tax['amount'] + order_line.order_id.rounding_error

                            order_line.order_id.write({'rounding_error_fix': True})
        else:
            tax_data = tax_ids.compute_all(price_unit=price, quantity=abs(order_line.qty), currency=self.currency_id, is_refund=is_refund, fixed_multiplicator=sign)
            taxes = tax_data['taxes']
        #

        # For Cash based taxes, use the account from the repartition line immediately as it has been paid already
        for tax in taxes:
            tax_rep = self.env['account.tax.repartition.line'].browse(tax['tax_repartition_line_id'])
            tax['account_id'] = tax_rep.account_id.id
        date_order = order_line.order_id.date_order
        taxes = [{'date_order': date_order, **tax} for tax in taxes]
        return {
            'date_order': order_line.order_id.date_order,
            'income_account_id': get_income_account(order_line).id,
            'amount': order_line.price_subtotal,
            'taxes': taxes,
            'base_tags': tuple(tax_data['base_tags']),
        }