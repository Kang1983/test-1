# Medal Recruit App

A web app for athletes to register medals won at track meets so college coaches can discover them.

## How it Works

1. **Athlete scans QR code** → Opens `index.html` (Landing page)
2. Enters the **medal details** (Event, Date, Performance, Meet)
3. Chooses:
   - **New Athlete** → Register profile + add medal → receives unique **Athlete ID**
   - **Already Registered** → Sign in with Athlete ID → medal is added to profile

## Registration Fields

- Name, Grade, School/Team (required)
- AAU Number, USATF Number (optional)
- GPA, Photo (1), Personal Bests (optional)

## Coaches View

Open `coaches-login.html` to access the registered athletes database (searchable by name, school, or event).

**Demo login credentials:**
- Username: `coach`
- Password: `medal2026`

Login state lasts for the browser session. Log out from the database page when finished.

## Backend

The app now uses a **Flask + SQLite backend** (`app.py`) for persistent storage of all athlete registration data.

**To run:**
```bash
pip install flask flask-cors
python3 app.py
```

Then open http://localhost:8080

Database file: `athletes.db` (created automatically).

## Theme

- Background: inverted "TRIPLE CROWN / 123456789" graphic (black text on white).
- Fonts: **Oswald** (headings, inspired by the bold crown/3 logo style) + Inter (body).
- Black & white high-contrast design matching the brand.

## Files

- `index.html` — Landing / Medal entry
- `register.html` — New athlete registration
- `signin.html` — Sign in with Athlete ID
- `profile.html` — Athlete's profile & medals
- `coaches-login.html` — Coach login page
- `coaches.html` — Coaches recruit database (requires login)
- `styles.css` & `script.js` — Shared styles and utilities

## How to Use

1. Open `index.html` in any modern browser.
2. Fill in a sample medal and register a new athlete.
3. Note the generated Athlete ID.
4. Visit `coaches.html` to see the entry.
5. Register another medal using the same ID via Sign In.

Perfect for local track meets — print QR codes linking to this app's landing page!
