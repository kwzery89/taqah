#!/usr/bin/python
from . import model
import logging
log = logging.getLogger(__name__)

def set_init_data(cr, registry):
    cr.execute(
        """UPDATE account_move_line
                     SET einv_amount_discount =quantity * price_unit * (discount/100);
        """
    )
    cr.execute(
            """update account_move_line set einv_amount_tax = price_subtotal * (select sum(tax.amount)/100 from account_tax tax where (id in (select account_tax_id from account_move_line_account_tax_rel where account_move_line_id = account_move_line.id)));    """
        )
    cr.execute(
        """
        update account_move set einv_amount_sale_total = (amount_untaxed + (select sum(einv_amount_discount) from account_move_line where move_id = account_move.id and exclude_from_invoice_tab = False));
        """)
    cr.execute(
        """
        update account_move set einv_amount_discount_total = (select sum(einv_amount_discount) from account_move_line where move_id = account_move.id and exclude_from_invoice_tab = False);
        """)
    cr.execute(
        """
        update account_move set einv_amount_tax_total = (select sum(einv_amount_tax) from account_move_line where move_id = account_move.id and exclude_from_invoice_tab = False);
    """)