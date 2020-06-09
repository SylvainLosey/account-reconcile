##############################################################################
#
#    Copyright (C) 2020 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Sylvain Losey <sylvainlosey@gmail.com>
#
#    The licence is in the file __manifest__.py
#
##############################################################################

from odoo import api, models


class AccountStatement(models.Model):
    """ TODO """

    _inherit = "account.bank.statement"

    @api.multi
    def automatic_reconcile(self):
        reconcile_model = self.env["account.reconcile.model"].search(
            [("rule_type", "!=", "writeoff_button")]
        )

        for bank_statement in self:
            matching_amls = reconcile_model._apply_rules(bank_statement.line_ids)

            for line_id, result in matching_amls.items():
                if result["aml_ids"]:
                    line = self.env["account.bank.statement.line"].browse(line_id)
                    matches = bank_statement.line_ids.browse(result["aml_ids"])

                    line.process_reconciliation(
                        counterpart_aml_dicts=[
                            {
                                "move_line": match,
                                "debit": hello,
                                "credit": hello,
                                "name": match.name,
                            }
                            for match in matches
                        ]
                    )
