-------------------ScholarTrack — Scholarship Search & Management System-----------------------------------------

ScholarTrack is a console-based Python and MySQL application for managing scholarship listings and applicant applications. It provides separate menus for applicants and administrators, with eligibility checks based on academic information stored in an applicant profile.
Features

Applicant:-
- Register an applicant account and log in
- Create, view, and edit a profile
- Store academic details using CGPA, percentage, or both
- Browse and search scholarship listings
- Check eligibility against a scholarship's minimum CGPA and/or percentage
- Submit scholarship applications
- View application status and application history
- View a dashboard with profile completion and application count

Administrator:-
- Log in to the admin menu
- View a dashboard with scholarship, applicant, and application counts
- Add, browse, search, and delete scholarship listings
- View applicant profiles and submitted applications
- Update application statuses: Applied, Shortlisted, Interview, Selected, or Rejected

Tech stack:-
- Language: Python
- Database: MySQL
- Python package: mysql-connector-python

Project structure:-
ScholarTrack/
├── main.py
├── requirements.txt
└── README.md


Setup:

1. Create and activate a virtual environment (recommended).
   macOS/Linux:
   python3 -m venv .venv
   source .venv/bin/activate
   Windows PowerShell:
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
2. Install the dependency.
   python -m pip install -r requirements.txt
3. Configure MySQL credentials in the Python program.
   The current source connects to a local MySQL server and includes a hard-coded password.
4. Run the program.
   python main.py
   The program is written to create the scholartrack_db database and its tables when it starts, provided the MySQL connection succeeds and the account has the required permissions.

Database tables:-
The program creates these tables:
Table	                    Purpose
users	             Login username, password, and role
profiles	          Applicant contact, education, skills, and achievements
scholarships	    Scholarship details, funding, deadline, and academic requirements
applications	    Applicant-to-scholarship records and application status


Eligibility logic:-

ScholarTrack compares the applicant's saved academic details with the minimum requirements entered for a scholarship. If a scholarship specifies a minimum CGPA or percentage, the applicant must provide that value and meet the threshold. If the required academic value is missing or below the threshold, the program reports that the applicant is not eligible.


Possible future improvements:-

- Move database credentials to environment variables
- Hash passwords securely
- Add automated tests and clearer error handling
- Validate dates and prevent applications after deadlines
- Add a web interface and scholarship filtering
