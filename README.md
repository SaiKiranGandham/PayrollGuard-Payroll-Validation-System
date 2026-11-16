# PayrollGuard – Payroll Validation & Reconciliation Management System

**PayrollGuard** is a web-based payroll validation and reconciliation management system developed using Python and Django. It helps manage employee payroll data, identify payroll errors, track exceptions, process approvals, and export approved payroll records.

## Overview

PayrollGuard provides a centralized platform to manage payroll operations and improve payroll accuracy through validation rules, exception management, approval workflows, and audit tracking.

## Key Features

- **Employee Management:** Manage employee information and employment status.
- **Payroll Processing:** Manage pay groups, pay periods, time entries, leave records, allowances, deductions, and payroll inputs.
- **Payroll Validation:** Detect excessive working hours, unapproved time entries, duplicate allowances, and payroll reconciliation errors.
- **Exception Management:** Track and resolve payroll validation exceptions.
- **Approval Management:** Submit payroll records for approval and approve or reject requests.
- **Audit Trail:** Track approval and payroll export activities.
- **CSV Export:** Export approved payroll records into CSV files.
- **Dashboard:** View payroll statistics, employee counts, approval status, and exception summaries.

## Technology Stack

| Technology | Usage |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| SQLite | Database |
| HTML5 | Frontend structure |
| CSS3 | Styling |
| Bootstrap 5 | Responsive UI |
| JavaScript | Frontend functionality |
| Chart.js | Dashboard charts |
| Git & GitHub | Version control |

## Project Architecture

```text
PayrollGuard/
│
├── approvals/
│   ├── management/
│   │   └── commands/
│   ├── models.py
│   ├── admin.py
│   └── services.py
│
├── audit/
│   ├── models.py
│   └── admin.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── employees/
│   ├── models.py
│   ├── views.py
│   └── admin.py
│
├── payroll/
│   ├── models.py
│   ├── views.py
│   └── admin.py
│
├── validation/
│   ├── management/
│   │   └── commands/
│   ├── models.py
│   ├── services.py
│   └── admin.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── employees/
│   │   └── employee_list.html
│   └── payroll/
│       └── dashboard.html
│
├── static/
├── exports/
├── manage.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/SaiKiranGandham/PayrollGuard-Payroll-Validation-System.git
cd PayrollGuard-Payroll-Validation-System
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an admin account

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Live Application: https://payrollguard-payroll-validation-system.onrender.com

## Payroll Validation Rules

The current validation engine checks:

1. Maximum working hours.
2. Unapproved time entries.
3. Duplicate allowance records.
4. Payroll net-pay reconciliation.

Run validation for a payroll record:

```bash
python manage.py run_payroll_validation 1
```

## Approval Workflow

Create an approval request:

```bash
python manage.py create_approval 1 1
```

Approve payroll:

```bash
python manage.py process_approval 1 APPROVE --comments "Verified and approved"
```

Reject payroll:

```bash
python manage.py process_approval 1 REJECT --comments "Requires correction"
```

## Payroll Export

Export approved payroll records:

```bash
python manage.py export_payroll 1
```

The generated CSV file is saved in the `exports/` directory.

Only approved payroll records are eligible for export.

## Database Design

The application uses Django ORM and SQLite. Its main data entities include:

- Employee
- PayGroup
- PayPeriod
- TimeEntry
- LeaveRecord
- Allowance
- Deduction
- PayrollInput
- ValidationRule
- Exception
- Approval
- ApprovalEvent
- PayrollExport
- AuditEvent

## Future Enhancements

- Synthetic payroll dataset generation.
- Additional anomaly detection rules.
- Advanced payroll analytics.
- Automated testing.
- PostgreSQL integration.
- Production deployment.

## Author

**Sai Kiran Gandham**

- GitHub: [SaiKiranGandham](https://github.com/SaiKiranGandham)
- LinkedIn: [Sai Kiran Gandham](https://www.linkedin.com/in/sai-kiran-gandham-84a0b3248/)

