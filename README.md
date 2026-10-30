# MediCare — Hospital Management System UI

A responsive, beginner-friendly Flask + SQLite starter project with seven requested public pages:
Home, About, Services, Contact, Help, Login and Register. It also includes a small protected Account page to demonstrate authentication.

## Features
- Responsive hospital landing page and service cards
- Register/login with password hashing
- SQLite database created automatically (`hospital.db`)
- Contact form saves messages into SQLite
- Flash messages for success and errors
- Simple accessible navigation and mobile menu
- No real patient records, clinical workflows, appointment booking, or notifications

## Run locally
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (recommended):
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install packages: `pip install -r requirements.txt`
5. Set a secret key for anything beyond local testing:
   - PowerShell: `$env:HOSPITAL_SECRET_KEY="replace-with-a-long-random-secret"`
   - macOS/Linux: `export HOSPITAL_SECRET_KEY="replace-with-a-long-random-secret"`
6. Start: `python app.py` (Windows can use `py app.py`)
7. Open `http://127.0.0.1:5000`

## Pages
- `/` Home
- `/about` About
- `/services` Services
- `/contact` Contact
- `/help` Help
- `/login` Login
- `/register` Register
- `/account` protected demo account page

## Important
This is a learning/demo starter, not a production hospital information system. Before handling real patient or health information, add security review, CSRF protection, rate limiting, secure deployment settings, access controls, audit logs, backups, privacy/legal review, and appropriate healthcare compliance controls. Do not put real patient information into this demo.
