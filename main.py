import mysql.connector as m

#DATABASE CONNECTION

def connect_db(database=None):
    try:
        if database:
            con = m.connect(host="localhost",user="root",password="24766",database="scholartrack_db")
        else:
            con = m.connect(host="localhost",user="root",password="24766")
        return con
    except m.Error as error:
        print("Database connection error:", error)
        return None

#CREATE DATABASE

def create_database():
    con = connect_db()
    if con is None:
        return False
    cursor = con.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS " + "scholartrack_db")
        con.close()
        con = connect_db("scholartrack_db")
        if con is None:
            return False
        cursor = con.cursor()

#USERS TABLE

        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL,
                role VARCHAR(20) NOT NULL)""")

#PROFILE TABLE
        cursor.execute("""CREATE TABLE IF NOT EXISTS profiles(
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT UNIQUE NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                phone VARCHAR(20),
                school VARCHAR(100),
                course VARCHAR(100),
                cgpa DECIMAL(3,2),
                percentage DECIMAL(5,2),
                skills VARCHAR(500),
                achievements VARCHAR(500),
                FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE)""")


#SCHOLARSHIP TABLE

        cursor.execute("""CREATE TABLE IF NOT EXISTS scholarships(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                country VARCHAR(100) NOT NULL,
                funding VARCHAR(30) NOT NULL,
                deadline VARCHAR(20) NOT NULL,
                eligibility VARCHAR(500) NOT NULL,
                minimum_cgpa DECIMAL(3,2),
                minimum_percentage DECIMAL(5,2))""")


#APPLICATION TABLE

        cursor.execute("""CREATE TABLE IF NOT EXISTS applications(
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                scholarship_id INT NOT NULL,
                status VARCHAR(30) DEFAULT 'Applied',

                FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

                FOREIGN KEY(scholarship_id)
                REFERENCES scholarships(id)
                ON DELETE CASCADE) """)

 #DEFAULT ADMIN

        cursor.execute("""SELECT * FROM users WHERE username = 'admin'""")
        admin = cursor.fetchone()
        if admin is None:
            cursor.execute("""INSERT INTO users (username, password, role)VALUES ('admin', 'admin123', 'admin')""")
        con.commit()
        print("\nDatabase ready.")
        return True
    except m.Error as error:
        print("Database setup error:", error)
        return False
    finally:
        con.close()


#INPUT FUNCTIONS

def get_text(message):
    while True:
        value = input(message).strip()
        if value != "":
            return value
        print("Input cannot be empty.")


def get_number(message):
    while True:
        try:
            value = int(input(message))
            if value >= 0:
                return value
            print("Enter a positive number.")
        except ValueError:
            print("Enter a valid number.")

def get_cgpa(message):
    while True:
        try:
            value = float(input(message))
            if value >= 0 and value <= 4:
                return value
            print("CGPA must be between 0 and 4.")
        except ValueError:
            print("Enter a valid CGPA.")


def get_percentage(message):
    while True:
        try:
            value = float(input(message))
            if value >= 0 and value <= 100:
                return value
            print("Percentage must be between 0 and 100.")
        except ValueError:
            print("Enter a valid percentage.")


#REGISTER APPLICANT

def register():

    print("\n")
    print("=" * 60)
    print("             APPLICANT REGISTRATION")
    print("=" * 60)

    username = get_text("Create username: ")
    password = get_text("Create password: ")
    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()

    try:
        cursor.execute("""INSERT INTO users(username, password, role)VALUES(%s, %s, %s)""", (username,password,"applicant"))
        con.commit()
        print("\nRegistration successful!")

    except m.Error as E:

        if E.errno == 1062: # ERROR 1062 : DUPPLICATE ENTRY
            print("\nUsername already exists.")
        else:
            print("\nRegistration error:", E)

    con.close()

#LOGIN

def login():

    print("\n")
    print("=" * 60)
    print("                    LOGIN")
    print("=" * 60)

    username = get_text("Username: ")
    password = get_text("Password: ")
    con = connect_db("scholartrack_db")
    if con is None:
        return None
    cursor = con.cursor()
    cursor.execute("""SELECT id, username, role FROM users WHERE username = %s AND password = %s""", (username, password))
    user = cursor.fetchone()
    con.close()
    if user is None:
        print("\nInvalid username or password.")
        return None
    print("\nLogin successful!")
    return user


#CREATE PROFILE

def create_profile(user_id):

    print("\n")
    print("=" * 60)
    print("                  CREATE PROFILE")
    print("=" * 60)

    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()

    cursor.execute("""SELECT * FROM profiles WHERE user_id = %s""", (user_id,))
    profile = cursor.fetchone()
    if profile is not None:
        print("\nProfile already exists.")
        con.close()
        return

    full_name = get_text("Full Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    school = input("School/College: ")
    course = input("Course: ")

    print("\nAcademic Details")
    print("1. CGPA")
    print("2. Percentage")
    print("3. Both")

    choice = input("Enter choice: ")
    cgpa = None
    percentage = None
    if choice == "1":
        cgpa = get_cgpa("CGPA: ")
    elif choice == "2":
        percentage = get_percentage("Percentage: ")
    elif choice == "3":
        cgpa = get_cgpa("CGPA: ")
        percentage = get_percentage("Percentage: ")

    skills = input("Skills: ")
    achievements = input("Achievements: ")

    cursor.execute("""
        INSERT INTO profiles(user_id,full_name,email,phone,school,course,cgpa,percentage,skills,achievements)
        VALUES(%s,%s,%s,%s,%s,%s,%s, %s,%s,%s) """, (user_id,full_name,email,phone,school,course,cgpa,percentage,skills,achievements))

    con.commit()
    con.close()
    print("\nProfile created successfully!")

#VIEW PROFILE

def view_profile(user_id):
    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT full_name,email,phone,school,course,cgpa,percentage,skills,achievements FROM profiles WHERE user_id = %s """, 
                   (user_id,))
    
    profile = cursor.fetchone()
    con.close()

    print("\n")
    print("=" * 60)
    print("                    MY PROFILE")
    print("=" * 60)

    if profile is None:
        print("Profile not created.")
        return
    print("Name          :", profile[0])
    print("Email         :", profile[1])
    print("Phone         :", profile[2])
    print("School        :", profile[3])
    print("Course        :", profile[4])

    if profile[5] is not None:
        print("CGPA          :",str(profile[5]) + "/4.0")
    else:
        print("CGPA          : Not provided")
    if profile[6] is not None:
        print("Percentage    :",str(profile[6]) + "%")
    else:
        print("Percentage    : Not provided")

    print("Skills        :", profile[7])
    print("Achievements  :", profile[8])

#EDIT PROFILE

def edit_profile(user_id):
    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT full_name,email,phone,school,course,cgpa,percentage,skills,achievements 
                   FROM profiles WHERE user_id = %s""", (user_id,))

    profile = cursor.fetchone()
    if profile is None:
        print("\nCreate your profile first.")
        con.close()
        return
    print("\nPress ENTER to keep the current value.")

    name = input("Full Name [" + str(profile[0]) + "]: ")
    if name == "":
        name = profile[0]

    email = input("Email [" + str(profile[1] or "") + "]: ")
    if email == "":
        email = profile[1]

    phone = input("Phone [" + str(profile[2] or "") + "]: ")
    if phone == "":
        phone = profile[2]

    school = input("School [" + str(profile[3] or "") + "]: ")
    if school == "":
        school = profile[3]

    course = input("Course [" + str(profile[4] or "") + "]: ")
    if course == "":
        course = profile[4]


    if profile[5] is None:
        old_cgpa = ""
    else:
        old_cgpa = str(profile[5])


    cgpa_input = input("CGPA [" + old_cgpa + "]: ")
    if cgpa_input == "":
        cgpa = profile[5]
    else:
        try:
            cgpa = float(cgpa_input)
            if cgpa < 0 or cgpa > 4:
                print("CGPA must be between 0 and 4.")
                con.close()
                return
        except ValueError:
            print("Invalid CGPA.")
            con.close()
            return


    if profile[6] is None:
        old_percentage = ""
    else:
        old_percentage = str(profile[6])


    percentage_input = input("Percentage [" + old_percentage + "]: ")
    if percentage_input == "":
        percentage = profile[6]
    else:
        try:
            percentage = float(percentage_input)
            if percentage < 0 or percentage > 100:
                print("Percentage must be between 0 and 100.")
                con.close()
                return
        except ValueError:
            print("Invalid percentage.")
            con.close()
            return

    skills = input("Skills [" + str(profile[7] or "") + "]: ")
    if skills == "":skills = profile[7]

    achievements = input("Achievements [" + str(profile[8] or "") + "]: ")
    if achievements == "":achievements = profile[8]
    cursor.execute("""UPDATE profiles SET full_name = %s,email = %s,phone = %s,school = %s,course = %s,cgpa = %s,percentage = %s,
                   skills = %s,achievements = %s WHERE user_id = %s """, (name,email,phone,school,course,cgpa,percentage,skills,
                    achievements, user_id))
    con.commit()
    con.close()
    print("\nProfile updated successfully!")

#ADD SCHOLARSHIP


def add_scholarship():

    print("\n")
    print("=" * 60)
    print("                 ADD SCHOLARSHIP")
    print("=" * 60)

    name = get_text("Scholarship name: ")
    country = get_text("Country: ")
    print("\nFunding")
    print("1. Fully Paid")
    print("2. Partially Paid")

    choice = input("Enter choice: ")
    if choice == "1":
        funding = "Fully Paid"
    elif choice == "2":
        funding = "Partially Paid"
    else:
        print("Invalid choice.")
        return

    deadline = get_text("Deadline (YYYY-MM-DD): ")
    print("\nEligibility")
    print("1. CGPA")
    print("2. Percentage")
    print("3. CGPA and Percentage")
    print("4. Other")

    choice = input("Enter choice: ")
    cgpa = None
    percentage = None
    eligibility = ""

    if choice == "1":
        cgpa = get_cgpa( "Minimum CGPA: ")
        eligibility = "Minimum CGPA"
    elif choice == "2":
        percentage = get_percentage("Minimum Percentage: ")
        eligibility = "Minimum Percentage"
    elif choice == "3":
        cgpa = get_cgpa("Minimum CGPA: ")
        percentage = get_percentage("Minimum Percentage: ")
        eligibility = "Minimum CGPA and Percentage"
    elif choice == "4":
        eligibility = get_text("Enter eligibility requirement: ")
    else:
        print("Invalid choice.")
        return

    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""INSERT INTO scholarships(name,country,funding,deadline,eligibility,minimum_cgpa,minimum_percentage)
        VALUES(%s,%s,%s,%s,%s,%s,%s)""", (name,country,funding,deadline,eligibility,cgpa,percentage))
    con.commit()
    con.close()

    print("\nScholarship added successfully!")

#VIEW SCHOLARSHIPS

def view_scholarships():
    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT id,name,country,funding,deadline,eligibility,minimum_cgpa,minimum_percentage FROM scholarships ORDER BY deadline""")

    records = cursor.fetchall()
    con.close()

    print("\n")
    print("=" * 75)
    print("                    SCHOLARSHIPS")
    print("=" * 75)

    if len(records) == 0:
        print("No scholarships found.")
        return

    for row in records:
        print("\nID          :", row[0])
        print("Name        :", row[1])
        print("Country     :", row[2])
        print("Funding     :", row[3])
        print("Deadline    :", row[4])
        print("Eligibility :", row[5])

        if row[6] is not None:
            print("Minimum CGPA:",str(row[6]))
        if row[7] is not None:
            print("Minimum %   :",str(row[7]) + "%")
        print("-" * 75)

#SEARCH SCHOLARSHIP

def search_scholarship():
    keyword = get_text("Enter scholarship name or country: ")
    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()
    value = "%" + keyword + "%"
    cursor.execute("""SELECT id, name,country,funding,deadline,eligibility FROM scholarships WHERE name LIKE %s OR country LIKE %s
                   ORDER BY deadline""", (value,value))
    records = cursor.fetchall()
    con.close()

    print("\n")
    print("=" * 65)
    print("                SEARCH RESULTS")
    print("=" * 65)

    if len(records) == 0:
        print("No scholarship found.")
        return

    for row in records:
        print("\nID          :", row[0])
        print("Name        :", row[1])
        print("Country     :", row[2])
        print("Funding     :", row[3])
        print("Deadline    :", row[4])
        print("Eligibility :", row[5])


#DELETE SCHOLARSHIP


def delete_scholarship():

    scholarship_id = get_number("Enter scholarship ID: ")
    con = connect_db("scholartrack_db")

    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT name FROM scholarships WHERE id = %s """, (scholarship_id,))
    scholarship = cursor.fetchone()

    if scholarship is None:
        print("Scholarship not found.")
        con.close()
        return
    print("\nScholarship:",scholarship[0])

    choice = input("Delete this scholarship? (yes/no): ").lower()
    if choice == "yes":
        cursor.execute("""DELETE FROM scholarships WHERE id = %s """, (scholarship_id,))
        con.commit()
        print("\nScholarship deleted.")
    else:
        print("\nDeletion cancelled.")
    con.close()

#CHECK ELIGIBILITY


def check_eligibility(user_id, scholarship_id):
    con = connect_db("scholartrack_db")
    if con is None:
        return False
    cursor = con.cursor()

#GET STUDENT PROFILE

    cursor.execute("""SELECT cgpa,percentage FROM profiles WHERE user_id = %s""", (user_id,))
    profile = cursor.fetchone()
    if profile is None:
        print("\nCreate your profile first.")
        con.close()
        return False
    
    student_cgpa = profile[0]
    student_percentage = profile[1]

#GET SCHOLARSHIP

    cursor.execute("""SELECT minimum_cgpa, minimum_percentage FROM scholarships WHERE id = %s""", (scholarship_id,))
    scholarship = cursor.fetchone()
    con.close()

    if scholarship is None:
        return False

    minimum_cgpa = scholarship[0]
    minimum_percentage = scholarship[1]

#CHECK CGPA

    if minimum_cgpa is not None:
        if student_cgpa is None:
            print("\nYour CGPA is missing.")
            return False

        if float(student_cgpa) < float(minimum_cgpa):
            print("\nYou are not eligible.")
            print("Required CGPA:",minimum_cgpa)
            print("Your CGPA:",student_cgpa)
            return False

#CHECK PERCENTAGE

    if minimum_percentage is not None:
        if student_percentage is None:
            print("\nYour percentage is missing.")
            return False

        if (float(student_percentage) < float(minimum_percentage)):
            print("\nYou are not eligible.")
            print( "Required Percentage:",minimum_percentage)
            print("Your Percentage:",student_percentage)
            return False

    return True

#APPLY FOR SCHOLARSHIP


def apply_scholarship(user_id):

    print("\n")
    print("=" * 60)
    print("              APPLY FOR SCHOLARSHIP")
    print("=" * 60)
    scholarship_id = get_number("Enter scholarship ID: ")
    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()

#CHECK SCHOLARSHIP

    cursor.execute("""SELECT name,deadline FROM scholarships WHERE id = %s""", (scholarship_id,))
    scholarship = cursor.fetchone()
    if scholarship is None:
        print("\nScholarship not found.")
        con.close()
        return

#CHECK PREVIOUS APPLICATION

    cursor.execute("""SELECT id FROM applicationsWHERE user_id = %sAND scholarship_id = %s""", (user_id, scholarship_id))
    application = cursor.fetchone()

    if application is not None:
        print("\nYou have already applied.")
        con.close()

        return

    con.close()

#CHECK ELIGIBILITY

    if not check_eligibility(user_id,scholarship_id):
        return
    print("\nYou are eligible for:",scholarship[0])

    choice = input("Apply now? (yes/no): ").lower()

    if choice != "yes":
        print("\nApplication cancelled.")
        return

    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()

    cursor.execute("""INSERT INTO applications(user_id,scholarship_id,status) VALUES (%s,%s,%s)""", (user_id,scholarship_id,"Applied"))
    con.commit()
    con.close()
    print("\nApplication submitted successfully!")

#MY APPLICATIONS

def my_applications(user_id):
    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT applications.id,scholarships.name,scholarships.country,scholarships.deadline,applications.status
    FROM applications JOIN scholarships ON applications.scholarship_id = scholarships.id WHERE applications.user_id = %s""", (user_id,))

    records = cursor.fetchall()
    con.close()

    print("\n")
    print("=" * 70)
    print("                  MY APPLICATIONS")
    print("=" * 70)

    if len(records) == 0:
        print("No applications found.")
        return

    for row in records:
        print("\nApplication ID :", row[0])
        print("Scholarship    :", row[1])
        print("Country        :", row[2])
        print("Deadline       :", row[3])
        print("Status         :", row[4])
        print("-" * 70)

#ADMIN VIEW APPLICANTS

def view_applicants():
    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT users.username,profiles.full_name,profiles.email,profiles.phone,profiles.school,profiles.course,profiles.cgpa,
            profiles.percentage FROM users JOIN profiles ON users.id = profiles.user_id WHERE users.role = 'applicant'""")
    records = cursor.fetchall()
    con.close()

    print("\n")
    print("=" * 75)
    print("                  APPLICANTS")
    print("=" * 75)

    if len(records) == 0:
        print("No applicants found.")
        return

    for row in records:
        print("\nUsername   :", row[0])
        print("Name       :", row[1])
        print("Email      :", row[2])
        print("Phone      :", row[3])
        print("School     :", row[4])
        print("Course     :", row[5])
        print("CGPA       :", row[6])
        print("Percentage :", row[7])
        print("-" * 75)

#ADMIN VIEW APPLICATIONS

def view_applications():
    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT applications.id,users.username,scholarships.name,scholarships.country,applications.status FROM applications 
    JOIN users ON applications.user_id = users.id JOIN scholarships ON applications.scholarship_id =scholarships.id""")
    records = cursor.fetchall()
    con.close()

    print("\n")
    print("=" * 80)
    print("                  APPLICATIONS")
    print("=" * 80)

    if len(records) == 0:
        print("No applications found.")
        return

    for row in records:
        print("\nApplication ID :", row[0])
        print("Applicant      :", row[1])
        print("Scholarship    :", row[2])
        print("Country        :", row[3])
        print("Status         :", row[4])
        print("-" * 80)


#UPDATE APPLICATION STATUS

def update_application():
    application_id = get_number("Enter application ID: ")
    print("\n1. Applied")
    print("2. Shortlisted")
    print("3. Interview")
    print("4. Selected")
    print("5. Rejected")

    choice = input("Enter choice: ")
    if choice == "1":
        status = "Applied"
    elif choice == "2":
        status = "Shortlisted"
    elif choice == "3":
        status = "Interview"
    elif choice == "4":
        status = "Selected"
    elif choice == "5":
        status = "Rejected"
    else:
        print("Invalid choice.")
        return
    
    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""UPDATE applications SET status = %s WHERE id = %s""", (status,application_id ))
    con.commit()
    con.close()

    print("\nApplication status updated.")

#ADMIN DASHBOARD

def admin_dashboard():
    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()

#TOTAL SCHOLARSHIPS

    cursor.execute("""SELECT COUNT(*) FROM scholarships""")
    scholarships = cursor.fetchone()[0]

#TOTAL APPLICANTS

    cursor.execute("""SELECT COUNT(*) FROM users WHERE role = 'applicant'""")
    applicants = cursor.fetchone()[0]


#TOTAL APPLICATIONS

    cursor.execute("""SELECT COUNT(*) FROM applications""")
    applications = cursor.fetchone()[0]
    con.close()

    print("\n")
    print("=" * 60)
    print("                 ADMIN DASHBOARD")
    print("=" * 60)

    print("Total Scholarships :",scholarships)
    print("Total Applicants   :",applicants)
    print("Total Applications :",applications)

#APPLICANT DASHBOARD


def applicant_dashboard(user_id):
    con = connect_db("scholartrack_db")
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT COUNT(*) FROM applications WHERE user_id = %s""", (user_id,))
    applications = cursor.fetchone()[0]
    cursor.execute("""SELECT COUNT(*) FROM profiles WHERE user_id = %s""", (user_id,))
    profile = cursor.fetchone()[0]
    con.close()

    print("\n")
    print("=" * 60)
    print("               APPLICANT DASHBOARD")
    print("=" * 60)

    if profile == 1:
        print("Profile Status : Complete")
    else:
        print("Profile Status : Incomplete")
    print("Applications   :",applications)

#ADMIN MENU

def admin_menu():
    while True:
        print("\n")
        print("*" * 60)
        print("                    ADMIN PANEL")
        print("*" * 60)
        print("1. Dashboard")
        print("2. Add Scholarship")
        print("3. View Scholarships")
        print("4. Search Scholarship")
        print("5. Delete Scholarship")
        print("6. View Applicants")
        print("7. View Applications")
        print("8. Update Application Status")
        print("9. Logout")
        choice = input("\nEnter choice: ")

        if choice == "1":
            admin_dashboard()
        elif choice == "2":
            add_scholarship()
        elif choice == "3":
            view_scholarships()
        elif choice == "4":
            search_scholarship()
        elif choice == "5":
            delete_scholarship()
        elif choice == "6":
            view_applicants()
        elif choice == "7":
            view_applications()
        elif choice == "8":
            update_application()
        elif choice == "9":
            print("\nLogged out.")
            break
        else:
            print("\nInvalid choice.")


#APPLICANT MENU

def applicant_menu(user_id):
    while True:
        print("\n")
        print("*" * 60)
        print("                  APPLICANT PANEL")
        print("*" * 60)
        print("1. Dashboard")
        print("2. View Scholarships")
        print("3. Search Scholarships")
        print("4. Create Profile")
        print("5. View Profile")
        print("6. Edit Profile")
        print("7. Apply for Scholarship")
        print("8. My Applications")
        print("9. Logout")

        choice = input("\nEnter choice: ")
        if choice == "1":
            applicant_dashboard(user_id)
        elif choice == "2":
            view_scholarships()
        elif choice == "3":
            search_scholarship()
        elif choice == "4":
            create_profile(user_id)
        elif choice == "5":
            view_profile(user_id)
        elif choice == "6":
            edit_profile(user_id)
        elif choice == "7":
            apply_scholarship(user_id)
        elif choice == "8":
            my_applications(user_id)
        elif choice == "9":
            print("\nLogged out.")
            break
        else:
            print("\nInvalid choice.")

#MAIN PROGRAM

def main():
    if create_database() == False:
        return
    while True:
        print("\n")
        print("=" * 60)
        print("                   SCHOLARTRACK")
        print("        Scholarship Search & Management")
        print("=" * 60)
        print("\n1. Admin Login")
        print("2. Applicant Login")
        print("3. Applicant Registration")
        print("4. Exit")
        choice = input( "\nEnter choice: ")

#ADMIN LOGIN

        if choice == "1":
            user = login()
            if user is not None:
                if user[2] == "admin":
                    admin_menu()
                else:
                    print("\nYou are not an admin.")


#APPLICANT LOGIN

        elif choice == "2":
            user = login()
            if user is not None:
                if user[2] == "applicant":
                    applicant_menu(user[0])
                else:
                    print("\nPlease use Admin Login.")


#REGISTRATION

        elif choice == "3":
            register()


#EXIT

        elif choice == "4":
            print("\nThank you for using ScholarTrack!")
            break
        else:
            print("\nInvalid choice.")

#START PROGRAM


if __name__ == "__main__":

    main()