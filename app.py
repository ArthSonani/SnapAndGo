import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import shutil
from helpers import login_required, allowed_name
from face_recog import *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///attendance50.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/",methods=["GET"])
@login_required
def index():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        if not username:
            return render_template("login.html", error="Must provide username!")

        # Ensure password was submitted
        elif not password:
            return render_template("login.html", error="Must provide password!")

        # Query database for username
        if role == "student":
            rows = db.execute(
                "SELECT * FROM students WHERE roll_no = ?", username
            )
        else:
            rows = db.execute(
                "SELECT * FROM teachers WHERE username = ?", username
            )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password
        ):
            return render_template("login.html", error="Invalid username or password!")

        # Remember which user has logged in and then redirect user
        if role == "student":
            session["username"] = rows[0]["roll_no"]
            return redirect("/student")
        else:
            session["username"] = rows[0]["username"]
            return redirect("/teacher")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register_student", methods=["POST"])
def register_student():
    name = request.form.get("name")
    username = request.form.get("rollno")
    password = request.form.get("password")
    vpassword = request.form.get("confirmation")
    file = request.files['photo']
    if name == "" or username == "" or password == "":
        return render_template("login.html", error="Name/Username/Password is missing!")

    if password != vpassword:
        return render_template("login.html",error="Password verification failed!")

    entries = db.execute("SELECT * FROM students")
    for entry in entries:
        if entry["roll_no"] == username:
            return render_template("login.html",error="Roll_no already exists!")

    hashed_password = generate_password_hash(password)
    
    if file and allowed_name(file.filename):
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        new_name = username + ext
        file.save(os.path.join('students-photos', new_name))

        db.execute(
            "INSERT INTO students (roll_no, name, hash, photo_ref) VALUES (:r, :n, :h, :p)",
            r=username,
            n=name,
            h=hashed_password,
            p=new_name
        )

        session["username"] = username
        return redirect("/student")
    else:
        return render_template("login.html", error="Invalid username or file")

    



@app.route("/register_teacher", methods=["POST"])
def register_teacher():
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    vpassword = request.form.get("confirmation")
    
    if name == "" or username == "" or password == "":
        return render_template("login.html", error="Name/Username/Password is missing!")

    if password != vpassword:
        return render_template("login.html",error="Password verification failed!")

    entries = db.execute("SELECT * FROM teachers")
    for entry in entries:
        if entry["username"] == username:
            return render_template("login.html",error="Username already exists!")

    hashed_password = generate_password_hash(password)
    db.execute(
        "INSERT INTO teachers (name, username, hash) VALUES (:n, :u, :h)",
        n=name,
        u=username,
        h=hashed_password,
    )
    session["username"] = username
    return redirect("/teacher")
    


@app.route("/student")
@login_required
def student():
    return redirect("/student/mygroups")


@app.route("/student/mygroups", methods=["GET"])
@login_required
def student_mygroups():
    username = session["username"]
    g = []
    rows = db.execute(
        "SELECT * FROM group_data WHERE roll_no = ?", username
    )
    for row in rows:
        group_id = row["group_id"]
        entry = db.execute(
            "SELECT * FROM groups WHERE group_id = ?", group_id
        )
        g.append(entry[0]["name"])

    return render_template("student-mygroups.html", groups = g)


@app.route("/student/show_attendance/<group_name>", methods=["GET"])
@login_required
def student_show_attendance(group_name):
    username = session["username"]
    attendance = []
    rows = db.execute(
        "SELECT * FROM groups WHERE name = ?", group_name
    )
    group_id = rows[0]["group_id"]

    entries = db.execute(
        "SELECT * FROM attendance WHERE roll_no = ? AND group_id = ? ORDER BY date_time",(username), (group_id)
    )
    for entry in entries:
        record = []
        date_time = (entry["date_time"]).split(" ")
        record.append(date_time[0])
        record.append(date_time[1])
        if entry["attend"] == "y":
            record.append("Present")
        else:
            record.append("Absent")
        attendance.append(record)
    return render_template("student-attendance.html", subject= group_name, records = attendance)


@app.route("/student/joingroup", methods=["GET", "POST"])
@login_required
def joingroup():
    if request.method == "POST":
        group_name = request.form.get("group_name")
        password = request.form.get("password")

        if not group_name:
            return render_template("student-joingroup.html", error="Must provide group name!")

        # Ensure password was submitted
        elif not password:
            return render_template("student-joingroup.html", error="Must provide password!")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM groups WHERE name = ?", group_name
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("student-joingroup.html", error="Invalid group name or password!")

        username = session["username"]
        group_id = rows[0]["group_id"]

        rows = db.execute(
            "SELECT * FROM group_data WHERE roll_no = ? AND group_id = ?", 
            (username), 
            (group_id)
        )
        if len(rows) != 0:
            return redirect("/student/mygroups")
        db.execute(
            "INSERT INTO group_data (roll_no, group_id) VALUES (:r, :g)", 
            r=username, 
            g=group_id
            )
                
        directory_name = group_name
        rows = db.execute(
            "SELECT photo_ref FROM students WHERE roll_no = ?", username
        )
        photo_ref = rows[0]["photo_ref"]
        source_path = os.path.join("students-photos/", photo_ref)
        destination_path = os.path.join("group-wise/", directory_name, "students/", photo_ref)

        shutil.copyfile(source_path, destination_path)
        return redirect("/student/mygroups")

    else:
        return render_template("student-joingroup.html")


@app.route("/teacher")
@login_required
def teacher():
    return redirect("/teacher/mygroups")

@app.route("/teacher/mygroups", methods=["GET"])
@login_required
def teacher_mygroups():
    username = session["username"]
    rows = db.execute(
        "SELECT * FROM teachers WHERE username = ?", username
    )
    teacher_id = rows[0]["teacher_id"]

    g = []
    rows = db.execute(
        "SELECT * FROM groups WHERE teacher_id = ?", teacher_id
    )
    for row in rows:
        g.append(row["name"])

    return render_template("teacher-mygroups.html", groups=g)


@app.route("/teacher/group/<group_name>", methods=["GET"])
@login_required
def teacher_group_selected(group_name):
    return render_template("teacher-group-selected.html", group_name=group_name)

###TODO
@app.route("/teacher/group/<group_name>/update", methods=["GET", "POST"])
@login_required
def teacher_attendance_update(group_name):
    if request.method == "POST":
        file = request.files['photo']
        date_time = (request.form.get("date-pick")).replace("T", " ")
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        new_name = "group" + ext
        path = os.path.join('group-wise/', group_name, "class/", new_name)
        file.save(path)
        s_path = os.path.join('group-wise/', group_name, "students/")
        g_path = os.path.join('group-wise/', group_name, "class/", new_name)
        rows = db.execute(
            "SELECT * FROM groups WHERE name = ?", group_name
        )
        group_id = rows[0]["group_id"]
        face_recognition(db, s_path, g_path, group_id, date_time)

    return render_template("teacher-update-attendance.html", group_name=group_name)


@app.route("/teacher/<group_name>/attendance", methods=["GET", "POST"])
@login_required
def attendance_select_datetime(group_name):
    if request.method == "POST":
        date_time = (request.form.get("date-pick")).replace("T", " ")
        print(date_time)
        username = session["username"]
        rows = db.execute(
            "SELECT * FROM groups WHERE name = ?", group_name
        )
        group_id = rows[0]["group_id"]

        rows = db.execute(
            "SELECT * FROM attendance WHERE group_id = ? AND strftime('%Y-%m-%d %H:%M', date_time) = ?",
            (group_id),
            (date_time)
        )
        attendance = {}
        for row in rows:
            attendance[row["roll_no"]] = row["attend"]

        return render_template("teacher-show-attendance.html", group_name=group_name, attendance=attendance)
    return render_template("teacher-select-datetime.html", group_name=group_name)



@app.route("/teacher/creategroup", methods=["GET", "POST"])
@login_required
def creategroup():
    if request.method == "POST":
        group_name = request.form.get("group_name")
        password = request.form.get("password")
        if group_name == "" or password == "":
            return render_template("teacher-create-group.html", error="Group name or Password is missing!")
        
        entries = db.execute("SELECT * FROM groups")
        for entry in entries:
            if entry["name"] == group_name:
                return render_template("teacher-create-group.html", error="Group Name already exists!")
  
        hashed_password = generate_password_hash(password)
        username = session["username"]
        rows = db.execute(
            "SELECT * FROM teachers WHERE username = ?", username
        )
        id = rows[0]["teacher_id"]
        db.execute(
            "INSERT INTO groups (teacher_id, name, hash) VALUES (:t, :n, :h)",
            t=id,
            n=group_name,
            h=hashed_password
        )

        directory_name = group_name

        # Create a path for the new directory. 
        current_directory = os.getcwd()
        c = os.path.join(current_directory, 'group-wise')
        path_to_gw = os.path.join(os.path.expanduser('~'), c)
        new_directory_path = os.path.join(path_to_gw, directory_name)
        os.makedirs(new_directory_path, exist_ok=True)
        new_directory_path1 = os.path.join(new_directory_path, "class")
        os.makedirs(new_directory_path1, exist_ok=True)
        new_directory_path2 = os.path.join(new_directory_path, "students")
        os.makedirs(new_directory_path2, exist_ok=True)

    return render_template("teacher-create-group.html")


#app.run(host="0.0.0.0", port=50100, debug=True, ssl_context="adhoc")