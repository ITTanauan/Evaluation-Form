from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date as current_date 
from collections import defaultdict
from xlsxwriter import Workbook
from reportlab.lib.pagesizes import letter
from sqlalchemy import extract
from reportlab.lib.units import inch
from werkzeug.utils import secure_filename
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from pytz import timezone, utc
from urllib.parse import urljoin
from math import ceil
import json
import uuid
import urllib.parse
import pandas as pd 
import io
import qrcode
import os
import socket

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False 

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'feedback_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Add this to fetch results as dictionaries

# Database Configuration (Update your MySQL credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  
migrate = Migrate(app, db)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER   

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)   

# Define Participants Model
class Participants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    activity_name = db.Column(db.String(255), nullable=True)
    venue = db.Column(db.String(200), nullable=True)
    school = db.Column(db.String(200), nullable=True)
    district = db.Column(db.String(200), nullable=True)
    facilitator_name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    date = db.Column(db.Date, nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    comments = db.relationship('CommentResponse', backref='participant', cascade="all, delete", lazy=True)
    assessments = db.relationship('AssessmentResponse', backref='participant', cascade="all, delete", lazy=True)
    admin = db.relationship('Admin', backref='participants')

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_text = db.Column(db.Text, nullable=False)
    question_num = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Text, nullable=False)   

class AdditionalComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    additional_question = db.Column(db.Text, nullable=False)

class CommentResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    participant_id =db.Column(db.Integer, db.ForeignKey('participants.id', ondelete="CASCADE"), nullable=False)  
    additional_comment_id = db.Column(db.Integer, db.ForeignKey('additional_comment.id', ondelete="CASCADE"), nullable=True)  
    comment_response = db.Column(db.String(200), nullable=False)
    
class AssessmentResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id', ondelete="CASCADE"), nullable=False) 
    assessment_number = db.Column(db.Integer, nullable=False)
    response = db.Column(db.String(10), nullable=False)  
    comment = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    fullname= db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)

    password_updated_at = db.Column(db.DateTime, nullable=True)

class AdminLoginActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    admin = db.relationship('Admin', backref='login_activities')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin/login')
def admin():
    return render_template('admin_login.html')

@app.route('/admin/signup')
def admin_signup_page():
    return render_template('admin_signup.html')

# Fetch all questions grouped by category
def get_all_questions():
    questions = Assessment.query.order_by(Assessment.id).all()  # Order by ID (ascending)
    questions_by_category = {}

    for index, question in enumerate(questions, start=1):
        if question.category not in questions_by_category:
            questions_by_category[question.category] = []
        question.display_number = index  # Assign sequential numbering
        questions_by_category[question.category].append(question)

    return questions_by_category

#Admin Signup
@app.route('/admin/signup', methods=['POST'])
def admin_signup():
    if request.method == 'POST':
        username = request.form['new_username']
        password = request.form['new_password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_admin = Admin(username=username, password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()

        flash('Admin account created successfully!', 'success')
        return redirect(url_for('admin_login'))

# Admin Login
@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin_data = Admin.query.filter_by(username=username).first()

        if admin_data and check_password_hash(admin_data.password, password):
            session['admin'] = username
            session['id'] = admin_data.id

            # ✅ Log login activity
            login_activity = AdminLoginActivity(
                admin_id=admin_data.id,
            )
            db.session.add(login_activity)
            db.session.commit()

            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Try again.', 'danger')
            return redirect(url_for('admin_login'))
          
    return render_template('admin_login.html') 
        
#Admin Change Password 
@app.route('/change_password_ajax', methods=['POST'])
def change_password_ajax():
    print("SESSION:", session)

    if 'id' not in session:
        print("Session does not contain 'id'. User not logged in.")
        return jsonify({"success": False, "message": "You must be logged in."}), 401

    admin = Admin.query.get(session['id'])
    if not admin:
        print("Admin user not found.")
        return jsonify({"success": False, "message": "Admin user not found."}), 404

    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    # Use werkzeug's check_password_hash
    if not check_password_hash(admin.password, old_password):
        print("Old password does not match.")
        return jsonify({"success": False, "message": "Old password is incorrect."})

    if new_password != confirm_password:
        print("New passwords do not match.")
        return jsonify({"success": False, "message": "New passwords do not match."})

    # Hash the new password using pbkdf2:sha256
    admin.password = generate_password_hash(new_password, method='pbkdf2:sha256')
    admin.password_updated_at = datetime.utcnow()
    db.session.commit()

    print("Password updated successfully.")
    return jsonify({"success": True, "message": "Password updated successfully!"})

#Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    if not admin:
        session.pop('admin', None)
        flash('Admin not found or session expired. Please log in again.', 'danger')
        return redirect(url_for('admin'))

    # 🛠 Try to read from URL first
    selected_year = request.args.get('year')
    selected_month = request.args.get('month')

    # 🛠 If user submitted new filter
    if selected_year is not None:
        if selected_year == "":
            session.pop('selected_year', None)   # Clear year filter if "All" selected
            selected_year = None
        else:
            selected_year = int(selected_year)
            session['selected_year'] = selected_year
    else:
        selected_year = session.get('selected_year')

    if selected_month is not None:
        if selected_month == "":
            session.pop('selected_month', None)  # Clear month filter if "All" selected
            selected_month = None
        else:
            selected_month = int(selected_month)
            session['selected_month'] = selected_month
    else:
        selected_month = session.get('selected_month')

    # Base query
    participant_query = Participants.query.filter_by(admin_id=admin.id)
    if selected_year:
        participant_query = participant_query.filter(extract('year', Participants.date) == selected_year)
    if selected_month:
        participant_query = participant_query.filter(extract('month', Participants.date) == selected_month)

    participants = participant_query.all()
    total_participants = participant_query.count()

    activities = db.session.query(Participants.activity_name)\
        .filter_by(admin_id=admin.id)
    if selected_year:
        activities = activities.filter(extract('year', Participants.date) == selected_year)
    if selected_month:
        activities = activities.filter(extract('month', Participants.date) == selected_month)
    activities = activities.distinct().all()

    total_activities = len(activities)
    activities = [{"activity_name": activity[0]} for activity in activities]

    participant_ids = [p.id for p in participants]

    assessments = AssessmentResponse.query.filter(
        AssessmentResponse.participant_id.in_(participant_ids)
    ).all()

    rating_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    total_responses = 0
    for assessment in assessments: 
        try:
            rating = int(assessment.response)
            if rating in rating_counts:
                rating_counts[rating] += 1
                total_responses += 1
        except ValueError:
            continue
        
    has_rating_data = total_responses > 0
    
    rating_percentages = {
        key: (count / total_responses * 100) if total_responses > 0 else 0
        for key, count in rating_counts.items()
    }

    for i in range(4):
        rating_percentages.setdefault(i, 0)

    years = db.session.query(extract('year', Participants.date)).distinct().order_by(extract('year', Participants.date)).all()
    years = [int(y[0]) for y in years if y[0] is not None]

    local_ip = get_local_ip()
    dynamic_link = urljoin(f"http://{local_ip}:5001/", f"participant?admin_id={admin.id}")

    return render_template(
        'admin_dashboard.html',
        admin=admin,
        participants=participants,
        total_participants=total_participants,
        total_activities=total_activities,
        rating_percentages=rating_percentages,
        has_rating_data=has_rating_data,
        activities=activities,
        years=years,
        dynamic_link=dynamic_link,
        selected_year=selected_year,
        selected_month=selected_month
    )

#Admin Activity List of Activity
@app.route('/admin/list')
def admin_list():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()

    selected_year = request.args.get('year', type=int)
    selected_month = request.args.get('month', type=int)
    
    participant_query = Participants.query.filter_by(admin_id=admin.id)
    if selected_year:
        participant_query = participant_query.filter(extract('year', Participants.date) == selected_year)
    if selected_month:
        participant_query = participant_query.filter(extract('month', Participants.date) == selected_month)

    participants = participant_query.all()

    grouped_activities = defaultdict(list)
    for participant in participants:
        grouped_activities[participant.activity_name].append(participant)

    return render_template(
        'admin_list.html',
        admin=admin,
        participants=participants,  
        grouped_activities=grouped_activities,
        selected_year=selected_year,
        selected_month=selected_month
    )

@app.route('/view-activity')
def view_activity():
    activity_name = request.args.get("activity_name")
    selected_year = request.args.get('year', type=int)
    selected_month = request.args.get('month', type=int)
    admin = Admin.query.filter_by(username=session['admin']).first()
    page = int(request.args.get('page', 1))
    per_page = 10

    if activity_name:
        try:
            activity_name = urllib.parse.unquote(activity_name)
        except Exception as e:
            return "Invalid activity name", 400

    if not activity_name:
        return "Activity not found", 404

    # Initial query
    participants_query = Participants.query.filter_by(activity_name=activity_name, admin_id=session['id'])

    # Apply year/month filters BEFORE pagination
    if selected_year:
        participants_query = participants_query.filter(extract('year', Participants.date) == selected_year)
    if selected_month:
        participants_query = participants_query.filter(extract('month', Participants.date) == selected_month)

    # Count total after filtering
    total = participants_query.count()
    total_pages = ceil(total / per_page)

    # Apply pagination AFTER filtering
    participants = participants_query.offset((page - 1) * per_page).limit(per_page).all()

    return render_template("view_activity.html", 
                           activity_name=activity_name, 
                           participants=participants, 
                           admin=admin,
                           selected_year=selected_year,
                           selected_month=selected_month,  
                           page=page, 
                           total_pages=total_pages)

#Export File
@app.route('/export', methods=['GET'])
def export():
    export_type = request.args.get('type')  # Get the export type (pdf or excel)
    activity_name = request.args.get('activity')

    if not activity_name:
        return "Activity parameter is required", 400

    # Query database for participant data
    participants = Participants.query.filter_by(activity_name=activity_name, admin_id=session['id']).all()

    if not participants:
        return "No participants found from the activity", 404

    if export_type == 'excel':
        return export_excel(participants)
    elif export_type == 'pdf':
        return export_pdf(participants, activity_name)
    else:
        return "Invalid export type", 400

#Excel Export
def export_excel(participants):
    """Export participants' data with responses and comments aligned correctly."""
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet("Assessment Data")

        # Define header formatting
        header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        text_format = workbook.add_format({'text_wrap': True, 'border': 1})

        # Column headers (Static Part)
        headers = ["Name", "Name of Activity", "Venue", "School", "District", "Facilitator", "Address", "Date"]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        question_categories = {
            range(1, 4): "About the Topic/s",
            range(4, 6): "About the materials",
            range(6, 13): "About the facilitator/s",
            range(13, 19): "About the food and venue",
            range(19, 30): "About Save The Children Staff Support"
        }

        # Function to get the category for a question
        def get_category(q_num):
            for q_range, category in question_categories.items():
                if q_num in q_range:
                    return category
            return "Uncategorized"

        # Fetch unique questions (ordered)
        assessments = Assessment.query.order_by(Assessment.question_num).all()
        questions_by_category = {}  # Store questions grouped by category
        for a in assessments:
            category = get_category(a.question_num)
            if category not in questions_by_category:
                questions_by_category[category] = []
            questions_by_category[category].append(a.assessment_text)

        # Add questions to headers (dynamic)
        col_offset = len(headers)
        question_mapping = {}  # Track column index for each question
        column_index = col_offset
        assessment_question_numbers = [a.question_num for a in assessments] # Track assessment numbers for response alignment

        for category, questions in questions_by_category.items():
            q_counter = 1  # Reset numbering for each category
            for q_text in questions:
                question_label = f"{category} - Q{q_counter}"
                worksheet.write(0, column_index, f"{question_label} - Response", header_format)
                worksheet.write(0, column_index + 1, "Comment", header_format)

                # Fetch correct assessment object for this question text
                matching_assessment = next((a for a in assessments if a.assessment_text == q_text), None)
                if matching_assessment:
                    question_mapping[matching_assessment.question_num] = (column_index, column_index + 1)

                print(f"Mapping: {q_text} -> Col {column_index}, {column_index + 1}")  # Debug print
                column_index += 2
                q_counter += 1

        # Set additional question columns **after** assessment columns
        additional_col_offset = column_index  

        # Add additional question headers
        additional_questions = AdditionalComment.query.all()
        additional_columns = {}

        for index, add_q in enumerate(additional_questions):
            column_name = f"Q{index + 1}: {add_q.additional_question}"
            worksheet.write(0, additional_col_offset + index, column_name, header_format)
            additional_columns[add_q.id] = additional_col_offset + index  # Map additional question ID to column index

        # Populate participant data and responses
        for row, participant in enumerate(participants, start=1):
            worksheet.write(row, 0, participant.name, text_format)
            worksheet.write(row, 1, participant.activity_name, text_format)
            worksheet.write(row, 2, participant.venue, text_format)
            worksheet.write(row, 3, participant.school, text_format)
            worksheet.write(row, 4, participant.district, text_format)
            worksheet.write(row, 5, participant.facilitator_name, text_format)
            worksheet.write(row, 6, participant.address, text_format)
            worksheet.write(row, 7, str(participant.date), text_format)

            print(f"\nParticipant: {participant.name}")
            print(f"Assessments: {participant.assessments}")

            responses = {resp.assessment_number: (resp.response or "No Response", resp.comment or "No Comment") for resp in participant.assessments}
            print(f"Expected Questions: {list(question_mapping.keys())}")
            print(f"Responses Available: {list(responses.keys())}")

            for q_number in assessment_question_numbers:
                if q_number in responses:
                    response_value, comment_value = responses[q_number]

                    print(f"Checking Q{q_number}: Response - {response_value}, Comment - {comment_value}")

                    if q_number in question_mapping:
                        resp_col, comment_col = question_mapping[q_number]

                        print(f"Writing Response at Col {resp_col}: {response_value}")
                        print(f"Writing Comment at Col {comment_col}: {comment_value}")

                        worksheet.write(row, resp_col, response_value, text_format)
                        worksheet.write(row, comment_col, comment_value, text_format)

            additional_responses = CommentResponse.query.filter_by(participant_id=participant.id).all()
            print(f"Additional Comments for {participant.name}: {additional_responses}")

            for add_resp in additional_responses:
                col_index = additional_columns.get(add_resp.additional_comment_id)
                if col_index is not None:
                    worksheet.write(row, col_index, add_resp.comment_response, text_format)

        # Adjust column width
        worksheet.set_column(0, additional_col_offset + len(additional_questions), 20)

    output.seek(0)
    return send_file(output, download_name="assessment_data.xlsx", as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

#PDF Export
def export_pdf(participants, activity_name):
    """Export assessments and participants' responses in a structured table format with logo and instructions for each participant."""
    
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter, 
                            leftMargin=40, rightMargin=40, 
                            topMargin=30, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()

    # Custom styles with font size 12
    font12_style = ParagraphStyle(
        name="Font12",
        parent=styles["Normal"],
        fontSize=10,
        leading=18,        
    )

    font12_centered = ParagraphStyle(
        name="Font14Centered",
        parent=font12_style,
        alignment=TA_CENTER
    )

    instructions_style = ParagraphStyle(
        name="InstructionsStyle",
        fontSize=10,
        leading=18,    
        parent=font12_style,
        alignment=TA_JUSTIFY
    )

    category_header_style = ParagraphStyle(
        name="CategoryHeaderStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold", 
        fontSize=13,
        alignment=TA_CENTER,
        leading=14
    )

    # Define logo path at the start
    logo_path = "static/images/STC_Logo.png"  

    # Instructions paragraph
    instructions = Paragraph(
        """
        <p>In order for us to improve future Save the Children activities, please truthfully answer the following questions based on your observations and experience.</p>
        <p>Using the scale of 1 to 3 where </p>
            <ul>
                <li><b>1</b> is DISAGREE, </li>
                <li><b>2</b> is NEUTRAL, </li>
                <li><b>3</b> is AGREE, </li>
            </ul>
            <p> kindly type the number that best correspond to your feedback and add comments as needed.</p>
            <p> Please click zero <b>"0" if NOT Applicable.</b></p>
            """, instructions_style
    )

    category_mapping = {
        "topics": "About the Topic/s",
        "materials": "About the Materials",
        "facilitators": "About the Facilitator/s",
        "food_venue": "About the Food and Venue",
        "staff_support": "About Save The Children Staff Support"
    }

    for index, participant in enumerate(participants):
        if index > 0:
            elements.append(PageBreak())  # Add a page break for each new participant

        title_style = ParagraphStyle(
            name="CustomTitle",
            fontName="Helvetica-Bold", 
            fontSize=16,               
            alignment=TA_LEFT,       
            spaceAfter=14,            
            leading=15
        )

        # Title and Logo side by side
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=150, height=40)
        else:
            logo = Paragraph("", title_style)  

        title = Paragraph("<b>EVALUATION AND FEEDBACK FORM</b>", title_style)

        header_table = Table([[title, logo]], colWidths=[424.6, 101]) 
        header_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (0, 0), "LEFT"),    
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),  
                ("LEFTPADDING", (0, 0), (-1, -1), 0),  
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("MARGIN", (0, 0), (-1, -1), 10), 
            ]))

        elements.append(header_table)
        elements.append(Spacer(1, 3)) 
        
        # Participant Info
        participant_data = [
            [Paragraph(f"<b>Participant:</b> {participant.name}", font12_style),
            Paragraph(f"<b>Date:</b> {participant.date}", font12_style)],
            
            [Paragraph(f"<b>Activity:</b> {participant.activity_name or 'N/A'}", font12_style),
            Paragraph(f"<b>Venue:</b> {participant.venue}", font12_style)],
            
            [Paragraph(f"<b>School:</b> {participant.school}", font12_style),
            Paragraph(f"<b>District:</b> {participant.district}", font12_style)],
            
            [Paragraph(f"<b>Facilitator:</b> {participant.facilitator_name}", font12_style),
            Paragraph(f"<b>Barangay/Municipal:</b> {participant.address}", font12_style)],
        ]
        
        participant_table = Table(participant_data, colWidths=[4 * inch, 3.25 * inch])
        participant_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),  # Apply uniform bottom padding for all rows
            ("BOTTOMPADDING", (0, 1), (-1, -1), 0),  # Apply a different bottom padding to the second row, for example
            ("BOTTOMPADDING", (0, 2), (-1, -1), 0),  # Adjust for the third row
            ("BOTTOMPADDING", (0, 3), (-1, -1), 10),  # Adjust for the fourth row
        ]))

        elements.append(participant_table)
        elements.append(Spacer(1, 3))

        instructions_table = Table([[instructions]], colWidths=[7.30 * inch])  # 6.5 = 8.5 inch page - (45*2 margin in points)
        instructions_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),  # 👈 controls bottom padding here
        ]))
        elements.append(instructions_table)
        elements.append(Spacer(1, 9)) 

        # Get responses
        responses = AssessmentResponse.query.filter_by(participant_id=participant.id).all()
        additional_responses = CommentResponse.query.filter_by(participant_id=participant.id).all()

        # Organize responses by category
        category_dict = {}
        for response in responses:
            assessment = Assessment.query.filter_by(id=response.assessment_number).first()
            if assessment:
                category_name = category_mapping.get(assessment.category, assessment.category)
                category_dict.setdefault(category_name, []).append([
                    Paragraph(assessment.assessment_text, font12_style),
                    Paragraph(str(response.response), font12_centered),
                    Paragraph(response.comment if response.comment else "N/A", font12_centered)
                ])

        # Create table
        table_data = []
        table_styles = [
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (1, 0), (1, -1), "CENTER"),  # Center align Rating
            ("ALIGN", (2, 0), (2, -1), "CENTER"),  # Center align Comments
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            
            # Add padding to assessment_text column (column 0)
            ("LEFTPADDING", (0, 0), (0, -1), 10),
            ("RIGHTPADDING", (0, 0), (0, -1), 10),
            ("TOPPADDING", (0, 0), (0, -1), 7),
            ("BOTTOMPADDING", (0, 0), (0, -1), 7),
        ]

        for category, questions in category_dict.items():
            table_data.append([
                Paragraph(category, category_header_style),
                Paragraph("Rating", category_header_style),
                Paragraph("Comment", category_header_style)
            ])
            
            header_row_index = len(table_data) - 1  # Track index of the current header row

            # Style for the header row
            table_styles += [
                ("FONTNAME", (0, header_row_index), (2, header_row_index), "Helvetica-Bold"),
                ("ALIGN", (0, header_row_index), (0, header_row_index), "LEFT"),  # Align category header left
                ("ALIGN", (1, header_row_index), (2, header_row_index), "CENTER"),
                ("VALIGN", (0, header_row_index), (2, header_row_index), "MIDDLE"),
                ("ROWHEIGHT", (0, header_row_index), (2, header_row_index), 32), 
            ]

            for row in questions:
                table_data.append(row)

        table = Table(table_data, colWidths=[3.9 * inch, 1 * inch, 2.3 * inch])  # Adjust column widths
        table.setStyle(TableStyle(table_styles))

        elements.append(table)
        elements.append(Spacer(1, 0))  # Space before next section

        # Additional Comments
        additional_header_style = ParagraphStyle(
            name="AdditionalHeaderStyle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            alignment=TA_LEFT,
            leading=14
        )

        if additional_responses:
            # One-column table header
            additional_table_data = [[
                Paragraph("Additional Question", additional_header_style)
            ]]

            additional_table_styles = [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]

            for add_response in additional_responses:
                additional_question = AdditionalComment.query.filter_by(id=add_response.additional_comment_id).first()
                if additional_question:
                    combined_text = f"{additional_question.additional_question}<br/><b>{add_response.comment_response}</b>"
                    additional_table_data.append([
                        Paragraph(combined_text, font12_style)
                    ])

            additional_table = Table(additional_table_data, colWidths=[7.2 * inch])  # Single wide column
            additional_table.setStyle(TableStyle(additional_table_styles))

            elements.append(additional_table)
            elements.append(Spacer(1, 24))  # Space before next section
    
    doc.build(elements)
    output.seek(0)
    return send_file(output, download_name="assessment_report.pdf", as_attachment=True, mimetype="application/pdf")

#View Total Participnats
@app.route('/view-total-participant')
def view_total_participant():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    activity_name = request.args.get("activity_name")
    selected_year = request.args.get('year', type=int)
    selected_month = request.args.get('month', type=int)
    page = int(request.args.get('page', 1))
    per_page = 10

    admin = Admin.query.filter_by(username=session['admin']).first()
    if activity_name:
        activity_name = urllib.parse.unquote(activity_name)

    participant_query = Participants.query.filter_by(admin_id=admin.id)

    if activity_name != "all":
        participant_query = participant_query.filter_by(activity_name=activity_name)

    if selected_year:
        participant_query = participant_query.filter(extract('year', Participants.date) == selected_year)
    if selected_month:
        participant_query = participant_query.filter(extract('month', Participants.date) == selected_month)

    total = participant_query.count()
    total_pages = ceil(total / per_page)

    participants = participant_query.offset((page - 1) * per_page).limit(per_page).all()
    activity_name_display = "All Activities" if activity_name == "all" else activity_name

    return render_template("view_total_participant.html",
                           activity_name=activity_name_display,
                           participants=participants,
                           admin=admin,
                           page=page,
                           total_pages=total_pages,
                           selected_year=selected_year,
                           selected_month=selected_month,
                           activity_filter=activity_name)

@app.route('/delete-participant/<int:participant_id>', methods=['POST'])
def delete_participant(participant_id):
    participant = Participants.query.get_or_404(participant_id)

    try:
        # Delete the participant (CASCADE will delete related assessments & comments)
        db.session.delete(participant)
        db.session.commit()

        print(f"✅ Successfully deleted participant {participant_id} and all related data.")  # Debugging
        return jsonify({"success": True, "message": "Participant deleted successfully."})

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error deleting participant: {e}")  # Debugging
        return jsonify({"success": False, "message": f"Error deleting participant: {e}"}), 500
        
@app.route('/view-participant/<int:participant_id>')
def view_participant(participant_id):
    participant = Participants.query.get(participant_id)
    admin = Admin.query.filter_by(username=session['admin']).first()

    # Query to join AssessmentResponse with Assessment
    responses = db.session.query(
        AssessmentResponse.assessment_number,
        Assessment.assessment_text,
        AssessmentResponse.response,
        AssessmentResponse.category,
        AssessmentResponse.comment
    ).join(Assessment, Assessment.id == AssessmentResponse.assessment_number) \
     .filter(AssessmentResponse.participant_id == participant_id).all()

    additional_responses = db.session.query(
        AdditionalComment.additional_question,
        CommentResponse.comment_response
    ).outerjoin(
        CommentResponse, AdditionalComment.id == CommentResponse.additional_comment_id
    ).filter(
        (CommentResponse.participant_id == participant_id) | (CommentResponse.participant_id.is_(None))).all()

    print("Query Results:", additional_responses)

    return render_template(
        'view_participant.html', participant=participant, responses=responses, additional_responses=additional_responses, admin=admin)

@app.route('/admin/profile')
def admin_profile():
    # Check for session
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    # Get admin by session username
    admin = Admin.query.filter_by(username=session['admin']).first()

    # If not found (just in case session is invalid or manually tampered)
    if not admin:
        session.pop('admin', None)
        flash('Admin session expired or user not found.', 'warning')
        return redirect(url_for('admin'))

    participants = Participants.query.all()

    # Define local timezone
    local_tz = timezone('Asia/Manila')

    # Safely convert timestamps to local time
    def to_local(dt):
        if dt.tzinfo is None:
            return utc.localize(dt).astimezone(local_tz)
        return dt.astimezone(local_tz)

    recent_logins = AdminLoginActivity.query.filter_by(admin_id=admin.id)\
        .order_by(AdminLoginActivity.timestamp.desc())\
        .limit(5).all()
    for login in recent_logins:
        login.timestamp = to_local(login.timestamp)

    all_logins = AdminLoginActivity.query.filter_by(admin_id=admin.id)\
        .order_by(AdminLoginActivity.timestamp.desc()).all()
    for login in all_logins:
        login.timestamp = to_local(login.timestamp)

    return render_template(
        'admin_profile.html',
        admin=admin,
        participants=participants,
        current_time=datetime.now().timestamp(),
        recent_logins=recent_logins,
        all_logins=all_logins
    )

@app.route('/admin/messages')
def admin_messages():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    participants = Participants.query.all()

    return render_template('admin_messages.html', admin=admin,  participants=participants)

@app.route('/admin/edit-profile', methods=['POST'])
def edit_admin_profile():
    if 'admin' not in session:
        return jsonify({"success": False, "message": "Please log in first."}), 403

    admin = Admin.query.filter_by(username=session['admin']).first()

    if not admin:
        return jsonify({"success": False, "message": "Admin not found."}), 404

    # Update text fields
    admin.username = request.form['username']
    admin.fullname = request.form['fullname']
    admin.email = request.form['email']
    admin.phone = request.form['phone']

    profile_picture_updated = False

    # Handle profile picture upload
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']

        if file and file.filename != "" and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(file_path)

            admin.profile_image = f"/static/uploads/{filename}"
            profile_picture_updated = True
            print("Saved profile picture path:", admin.profile_image)

    try:
        db.session.commit()
        if profile_picture_updated:
            return jsonify({"success": True, "profile_picture": admin.profile_image})
        else:
            return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
        
@app.route('/admin/results')
def admin_results():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))
    
    selected_year = request.args.get('year', type=int)
    selected_month = request.args.get('month', type=int)

    admin = Admin.query.filter_by(username=session['admin']).first()
    
    participant_query = Participants.query.filter_by(admin_id=admin.id)
    if selected_year:
        participant_query = participant_query.filter(extract('year', Participants.date) == selected_year)
    if selected_month:
        participant_query = participant_query.filter(extract('month', Participants.date) == selected_month)

    participant_ids = [p.id for p in participant_query.all()]
    assessments = AssessmentResponse.query.filter(AssessmentResponse.participant_id.in_(participant_ids)).all()

    categories = [
        "About the topic/s", "About the materials", "About the facilitator/s",
        "About the food and venue", "About Save The Children Staff Support"
    ]

    category_data = {category: [] for category in categories}

    for assessment in assessments:
        if assessment.category in category_data:
            try:
                category_data[assessment.category].append({
                    "question_number": assessment.assessment_number,
                    "rating": int(assessment.response)
                })
            except ValueError:
                print(f"Invalid response value for {assessment.assessment_number}")

    return render_template('admin_results.html', admin=admin, category_data=category_data)

# Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    session.pop('selected_year', None)
    session.pop('selected_month', None) 
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin'))

@app.route('/instructions')
def instructions(): 
    return render_template("instructions.html")

@app.route('/participant', methods=['GET', 'POST'])
def participant():
    admin_id = request.args.get('admin_id', type=int)
    if admin_id:
        session['admin_id'] = admin_id
    else:
        admin_id = session.get('admin_id')
        
    if request.method == 'POST':
        session['participant_form'] = request.form.to_dict()

        try:
            name = request.form['name']
            activity_name = request.form['activity_name']
            venue = request.form['venue']
            school = request.form['school']
            district = request.form['district']
            facilitator_name = request.form['facilitator_name']
            address = request.form['address']
            date_str = request.form['date']
            
            # If date is not filled in, use today's date
            if not date_str:
                date = current_date.today()
            else:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()

            admin_id = request.form.get('admin_id') or admin_id

            new_participant = Participants(
                name=name,
                activity_name=activity_name,
                venue=venue,
                school=school,
                district=district,
                facilitator_name=facilitator_name,
                address=address,
                date=date,
                admin_id=admin_id
            )

            db.session.add(new_participant)
            db.session.commit()

            session['participant_id'] = new_participant.id
            session.pop('participant_form', None)
            return redirect(url_for('assessment_questions'))

        except Exception as e:
            print(f"❌ Error inserting data: {e}")

    saved_data = session.get('participant_form', {})
    return render_template("assessment.html", admin_id=admin_id, saved_data=saved_data)

@app.route('/assessment_questions', methods=['GET', 'POST'])
def assessment_questions():
    participant_id = session.get('participant_id')
    admin_id = request.args.get('admin_id', type=int)
    if admin_id:
        session['admin_id'] = admin_id
    else:
        admin_id = session.get('admin_id')
        
    if not participant_id:
        flash("Please enter your details first.", "warning")
        return redirect(url_for('participant'))

    # Fetch questions grouped by category
    questions_by_category = get_all_questions()
    total_assessment = db.session.query(Assessment).count()
    current_assessment_number = session.get('current_assessment_number', 1)
    is_last_question = current_assessment_number == total_assessment

     # 🔹 Fetch additional comments from the database
    additional_questions = db.session.query(AdditionalComment).all()

    if request.method == 'POST':
        session['assessment_form'] = request.form.to_dict()
        try:
            responses_saved = False  

            # Save all responses
            for category, questions in questions_by_category.items():
                for question in questions:
                    response = request.form.get(f'q{question.id}')
                    comment = request.form.get(f'comment{question.id}')

                    if response is not None:
                        new_response = AssessmentResponse(
                            participant_id=participant_id,
                            assessment_number=question.id,
                            response=response,
                            comment=comment if comment else None,
                            category=question.category
                        )
                        db.session.add(new_response)
                        responses_saved = True  

             # 🔹 Save additional comments
            for question in additional_questions:
                additional_response = request.form.get(f'additional_question{question.id}')
                
                if additional_response:
                    new_comment = CommentResponse(
                        participant_id=participant_id,
                        additional_comment_id=question.id, 
                        comment_response=additional_response  # Assuming you have a 'comment' column in CommentResponse
                    )
                    db.session.add(new_comment)
                    responses_saved = True  

            if responses_saved:
                db.session.commit()  # Save responses to DB
                session.pop('current_assessment_number', None)  # Clear session variable
                session.pop('assessment_form', None)  # Clear the assessment form data
                admin_id = session.get('admin_id')
                return redirect(url_for('thank_you', admin_id=admin_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Error saving responses: {e}", "danger")

    # Retrieve the current question
    assessment = db.session.query(Assessment).filter_by(id=current_assessment_number).first()
    saved_assessment_data = session.get('assessment_form', {})

    return render_template('questionnaire.html', 
                           assessment=assessment, 
                           is_last_question=is_last_question, 
                           questions_by_category=questions_by_category, 
                           additional_question=additional_questions, 
                           saved_assessment_data=saved_assessment_data)

@app.route('/submit_offline_data', methods=['POST'])
def submit_offline_data():
    try:
        # Parse the incoming data
        data = request.get_json()

        # You would extract the relevant fields from 'data' and save it to the database
        name = data.get('name')
        activity_name = data.get('activity_name')
        venue = data.get('venue')
        school = data.get('school')
        district = data.get('district')
        facilitator_name = data.get('facilitator_name')
        address = data.get('address')
        date_str = data.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        new_participant = Participants(
            name=name,
            activity_name=activity_name,
            venue=venue,
            school=school,
            district=district,
            facilitator_name=facilitator_name,
            address=address,
            date=date,
            admin_id=None  # Or set this based on session or another value
        )

        db.session.add(new_participant)
        db.session.commit()

        # If submission is successful, return a success message
        return jsonify({"success": True})

    except Exception as e:
        print(f"Error saving offline data: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    
def get_local_ip():
    # Get the local machine's IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # Connect to an external server to determine the local IP address
        s.connect(('10.254.254.254', 1))  # Arbitrary external address
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'  # Default to localhost if error
    finally:
        s.close()
    return local_ip

@app.route('/generate_qr_image')
def generate_qr_image():
    if 'admin' not in session:
        return "Unauthorized", 403

    admin_id = session['id']

    # Get the local IP dynamically
    local_ip = get_local_ip()

    # Use the local IP to build the URL
    url = f"http://{local_ip}:5001/participant?admin_id={admin_id}"

    # Generate QR code
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    return send_file(buf, mimetype='image/png')

@app.route('/search_participant', methods=['GET'])
def search_participant():
    query = request.args.get("q", "").strip()
    admin_id = session.get("id")

    if not query:
        return jsonify([])

    if not admin_id:
        # Optionally log this
        print("No admin_id in session")
        return jsonify([])  # Or return an error

    participants = Participants.query.filter(
        Participants.admin_id == admin_id,
        ((Participants.name.ilike(f"%{query}%")) |
         (Participants.activity_name.ilike(f"%{query}%")))
    ).all()

    results = [{
        "id": p.id,
        "name": p.name,
        "activity_name": p.activity_name,
        "venue": p.venue,
        "school": p.school,
        "district": p.district,
        "facilitator_name": p.facilitator_name,
        "address": p.address,
        "date": p.date.strftime('%Y-%m-%d') if p.date else "N/A"
    } for p in participants]

    return jsonify(results)

@app.route('/thank-you')
def thank_you():
    admin_id = request.args.get('admin_id') or session.get('admin_id')
    return render_template('thankyou.html', admin_id=admin_id)

# Run App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0', port=5001, debug=True)

