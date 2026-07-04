# Full Stack Python Developer Assignment — Reference Project

A complete, runnable implementation of the 20-mark Full Stack Python Developer
interview assignment (Sections B, C, and D). Built with **Flask**, **SQLite**,
**Bootstrap 5**, and vanilla **JavaScript**.

## Project Structure

```
project/
├── app.py                  # Flask app — all routes & CRUD logic
├── requirements.txt        # Python dependencies
├── students.db             # SQLite DB (auto-created on first run)
├── templates/
│   ├── base.html           # Shared layout, navbar, Bootstrap 5 CDN
│   ├── index.html          # Registration form (Section C)
│   └── students.html       # Student list with Update/Delete (CRUD)
└── static/
    ├── css/style.css       # Custom styling (Q12)
    └── js/validate.js      # Client-side validation + dynamic UI (Q14, Q15)
```

## Setup & Run

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Then open **http://127.0.0.1:5000/** in your browser. The SQLite database
(`students.db`) is created automatically on first run and seeded with three
sample students.

## Routes

| Method | Route              | Purpose                                           | Assignment Q |
|--------|--------------------|----------------------------------------------------|--------------|
| GET    | `/`                | Registration form (HTML/CSS/Bootstrap/JS)           | Q11–Q15      |
| GET    | `/students`         | List all students, update marks, delete records     | Read/CRUD    |
| GET    | `/welcome`          | Returns `{"message": "Welcome to Full Stack Development"}` | Q16   |
| POST   | `/register`         | **Create** a student (form POST or JSON/fetch)       | Q17–Q19      |
| POST   | `/update/<id>`      | **Update** a student's marks                         | Q19          |
| POST   | `/delete/<id>`      | **Delete** a student record                          | Q19          |
| GET    | `/api/students`     | REST API — all students as JSON                      | Q20          |
| GET    | `/api/students/top` | REST API — students with marks > 80                  | Q18 (SELECT) |

## How each Section D task is demonstrated

- **Q16 – Flask route:** `GET /welcome` in `app.py`, returns JSON directly.
- **Q17 – SQLite connection:** `get_db_connection()` opens `students.db` with
  `sqlite3.connect()` and `row_factory = sqlite3.Row` for dict-like rows.
- **Q18 – SQL queries:**
  - `SELECT * FROM students WHERE marks > 80` → see `/api/students/top`
  - `INSERT INTO students (...) VALUES (...)` → see `/register`
- **Q19 – CRUD operations:**
  - **Create** → `/register` (INSERT)
  - **Read** → `/students` and `/api/students` (SELECT)
  - **Update** → `/update/<id>` (UPDATE ... marks)
  - **Delete** → `/delete/<id>` (DELETE)
- **Q20 – REST API:** `GET /api/students` returns a JSON array of every
  student record.

## How each Section C task is demonstrated

- **Q11 – HTML form:** `templates/index.html` — Name, Email, Password, Phone
  with correct input types and `<label>`s.
- **Q12 – CSS styling:** `static/css/style.css` — custom color palette,
  rounded cards, shadows, and a hover-animated submit button.
- **Q13 – Responsive layout:** Bootstrap 5 grid (`row`, `col-12 col-md-8
  col-lg-6`) so the form and result panel stack on mobile and sit side-by-side
  on desktop.
- **Q14 – JS validation:** `static/js/validate.js` checks required name,
  valid email pattern, password ≥ 6 characters, and a 10-digit phone number,
  showing inline Bootstrap `invalid-feedback` messages.
- **Q15 – UI components:** on successful validation, `validate.js` uses
  `fetch()` to POST JSON to `/register`, then renders a Bootstrap **card**
  with the submitted details and appends a row to a live Bootstrap **table**
  — without a page reload.

## Section B — Python programs

The five short Python programs from Section B (variable swap, even-number
loop, `is_prime()`, word-frequency dictionary, palindrome check) are
self-contained scripts, independent of the Flask app. See
`section_b_solutions.py` for all five with example output.

## Notes

- Passwords are hashed with `werkzeug.security.generate_password_hash`
  before being stored — never stored in plain text.
- This is a teaching/reference implementation for an interview assignment,
  not a production-hardened app (e.g. `secret_key` should be moved to an
  environment variable in real deployments).
