from enum import nonmember
from idlelib import query

import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from backend.logging_setup import getlogger

logger = getlogger(__name__)




conn= None
cursor=None

@contextmanager
def db_cursor(commit = False):
    db_config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'expense_manager',
    }
    try:
        conn= mysql.connector.connect(**db_config)
        if conn.is_connected():
           cursor= conn.cursor(dictionary=True)
           yield cursor

        if commit:
            conn.commit()

        print("Closing cursor")
        cursor.close()
        conn.close()

    except Error as e:
        print(f"Database error occurred: {e}")

def get_all_records():
      with db_cursor() as cursor:
          cursor.execute( "select * from expenses")
          records = cursor.fetchall()
          return records

def fetch_expense_with_date(date):
    logger.info(f"Fetching expenses  for date:{date} ")
    query = "select * from expenses where expense_date= %s"
    with db_cursor() as cursor:
        cursor.execute(query, (date,))
        records = cursor.fetchall()
        return records

def insert_expense(expense_date, amount, category, notes):

    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

def delete_expenses_for_date(expense_date):
    with db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def fetch_expenses_summary(start_date, end_date):
    logger.info(f"Fetching expenses summary for start:{start_date} and end :{end_date}date")
    with db_cursor() as cursor:
        cursor.execute(
            '''
            SELECT category,SUM(amount) as total 
            FROM expenses 
            where expense_date between %s and %s
            GROUP BY category;
            
            ''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data

def fetch_monthly_analytics():
    logger.info("Fetching monthly expense summary")
    query = """
        SELECT 
            DATE_FORMAT(expense_date, '%Y-%m') AS month_year,
            SUM(amount) AS total
        FROM expenses
        GROUP BY DATE_FORMAT(expense_date, '%Y-%m')
        ORDER BY month_year ASC;
    """
    with db_cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Formats to: {"2024-07": 1450.0, "2024-08": 2100.5, ...}
    return {
        str(row["month_year"]): float(row["total"] or 0.0)
        for row in rows
        if row.get("month_year") is not None
    }

if __name__ == "__main__":

    """expenses= get_all_records()
    for expense in expenses:
        print(expense)"""

    expenses = fetch_expense_with_date('2024-08-01')
    for expense in expenses:
        print(expense)




