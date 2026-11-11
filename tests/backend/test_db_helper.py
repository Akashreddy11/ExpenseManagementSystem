from backend import db_helper
import os
import sys
def test_fetch_expense_with_date_aug_15():
    expenses=db_helper.fetch_expense_with_date("2024-08-15")
    assert len(expenses)== 1
    assert expenses[0]["category"] == "Shopping"
    assert expenses[0]["amount"] == 10

def test_fetch_expense_for_date_invalid_date():
    expenses=db_helper.fetch_expense_with_date("9999-08-15")
    assert len(expenses)== 0
  