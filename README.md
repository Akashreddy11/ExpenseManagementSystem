# Expense Tracking System

A full-stack personal finance and expense tracking web application. The project features a **FastAPI** REST backend connected to a **MySQL** database, coupled with an interactive **Streamlit** dashboard for logging daily expenses, monitoring category distributions, and visualizing monthly spending trends with AI-assisted budget diagnostics.

---

## Features

- **Daily Expense Logging**: Add, inspect, and update categorized transactions for specific dates.
- **Category Analytics**: Real-time spending breakdowns, percentage distributions, and dynamic budget concentration insights.
- **Monthly Trend Tracking**: Aggregated monthly expense summaries with peak spending indicators and interactive charts.
- **Robust Database Transactions**: Context-managed MySQL connections with automatic commit/rollback handling.
- **Integrated Logging**: Isolated file-based logging setup to trace database and API operations without collisions.

---

## Tech Stack

- **Frontend**: Streamlit, Pandas, Requests
- **Backend**: FastAPI, Uvicorn, Pydantic
- **Database**: MySQL (via `mysql-connector-python`)
- **Testing**: Pytest

---

## Project Structure

```text
project-expense-tracking-system/
│
├── backend/
│   ├── __init__.py
│   ├── server.py              # FastAPI endpoints and route handlers
│   ├── db_helper.py           # MySQL queries and context managers
│   ├── logging_setup.py       # Logger configuration and file handler
│   └── server.log             # Generated application runtime logs
│
├── frontend/
│   ├── app.py                 # Streamlit main entry point & navigation
│   ├── add_update_ui.py       # Expense logging and entry form tab
│   ├── analytics_ui.py        # Category distribution & AI insights
│   └── monthly_analytics_ui.py# Monthly trends and bar chart visualizer
│
├── tests/
│   └── test_api.py            # Unit and integration test suite
│
├── requirements.txt           # Python dependencies
└── README.md

# Expense Tracking System

A full-stack Expense Tracking System built using **Python, FastAPI, Streamlit, and MySQL**. The application allows users to manage daily expenses, track spending by category, and analyze monthly and date-range spending patterns.

## Database Setup

Open your MySQL client (e.g., MySQL Workbench or MySQL CLI) and execute the following SQL queries:

```sql
CREATE DATABASE IF NOT EXISTS expense_manager;

USE expense_manager;

CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_date DATE NOT NULL,
    amount FLOAT NOT NULL,
    category VARCHAR(255) NOT NULL,
    notes TEXT DEFAULT NULL
);
```

### Configure Database Credentials

Open `backend/db_helper.py` and update the database configuration to match your local MySQL settings:

```python
db_config = {
    'user': 'root',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'expense_manager',
}
```

Replace `your_password` with your actual MySQL password.

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/project-expense-tracking-system.git

cd project-expense-tracking-system
```

### 2. Set Up a Virtual Environment

**Windows:**

```bash
python -m venv .venv

.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3. Install Dependencies

Make sure your virtual environment is activated, then execute:

```bash
pip install -r requirements.txt
```

## Running the Application

Both backend and frontend services must run concurrently.

Open two separate terminals and activate the virtual environment in both.

### Terminal 1: Start Backend (FastAPI)

```bash
uvicorn backend.server:app --reload
```

**API Base URL:** http://127.0.0.1:8000

**Interactive API Documentation (Swagger):** http://127.0.0.1:8000/docs

### Terminal 2: Start Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

**Dashboard URL:** http://localhost:8501

## API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| GET | `/expenses/{date}` | Retrieve all logged expenses for a given date (YYYY-MM-DD). |
| POST | `/expenses/{date}` | Upsert or replace expense items for a specified date. |
| POST | `/analytics` | Get category breakdown and percentages for a date range. |
| GET | `/analytics/monthly` | Retrieve aggregated lifetime spending grouped by month. |

## Running Tests

Execute the test suite using `pytest`:

```bash
pytest
```

## Technologies Used

- **Python** – Backend programming language
- **FastAPI** – REST API development
- **Streamlit** – Interactive frontend dashboard
- **MySQL** – Relational database
- **Uvicorn** – ASGI server
- **Pytest** – Automated testing

## Project Structure

```text
project-expense-tracking-system/
│
├── backend/
│   ├── server.py
│   └── db_helper.py
│
├── frontend/
│   └── app.py
|   └── add_update_ui.py
|   └── analytics_ui.py
|   └── analytics_monthly.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

*Note: The project structure above is illustrative. Adjust it to match your actual repository.*

## License

This project is intended for educational and personal use.

