from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import json
import uuid
import mysql.connector
from datetime import datetime 
from collections import defaultdict
import urllib.parse
import pandas as pd
import io
from xlsxwriter import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas 
from sqlalchemy.orm import joinedload
import os
from reportlab.lib.units import inch
from werkzeug.utils import secure_filename
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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
    name = db.Column(db.String(100), nullable=False)
    activity_name = db.Column(db.String(255), nullable=True)
    venue = db.Column(db.String(200), nullable=False)
    school = db.Column(db.String(200), nullable=False)
    district = db.Column(db.String(200), nullable=False)
    facilitator_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)

    comments = db.relationship('CommentResponse', backref='participant', cascade="all, delete", lazy=True)
    assessments = db.relationship('AssessmentResponse', backref='participant', cascade="all, delete", lazy=True)

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
    participants = Participants.query.all()
    total_participants = db.session.query(Participants).count()  

    # Get unread user responses
    activities = db.session.query(Participants.activity_name).distinct().all()
    total_activities = db.session.query(Participants.activity_name).distinct().count()

    activities = [{"activity_name": activity[0]} for activity in activities]

    # 🔹 Count ratings (initialize counts for 0, 1, 2, 3)
    rating_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    total_responses = 0

    assessments = AssessmentResponse.query.all()
    for assessment in assessments:
        try:
            rating = int(assessment.response)
            if rating in rating_counts:
                rating_counts[rating] += 1
                total_responses += 1
        except ValueError:
            continue  # Skip invalid ratings

    # 🔹 Compute percentages (avoid division by zero)
    rating_percentages = {
        key: (count / total_responses * 100) if total_responses > 0 else 0
        for key, count in rating_counts.items()
    }

    for i in range(4):  
        rating_percentages.setdefault(i, 0)

    return render_template(
        'admin_dashboard.html',
        admin=admin,participants=participants,  total_participants=total_participants, total_activities=total_activities, rating_percentages=rating_percentages,
        activities=activities
    )

#Admin Activity List
@app.route('/admin/list')
def admin_list():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    
    participants = Participants.query.all()  # Fetch all users
    assessment_responses = AssessmentResponse.query.all()

    grouped_activities = defaultdict(list)
    for participant in participants:
        grouped_activities[participant.activity_name].append(participant)

    return render_template(
        'admin_list.html',
        admin=admin,
        participants=participants,  
        assessment_responses=assessment_responses,
        grouped_activities=grouped_activities
    )

#View Activity
@app.route('/view-activity')
def view_activity():
    activity_name = request.args.get("activity_name")
    admin = Admin.query.filter_by(username=session['admin']).first()

    # Decode the URL-encoded activity name
    if activity_name:
        try:
            # Decode the URL-encoded string
            activity_name = urllib.parse.unquote(activity_name)
            print(f"Decoded activity_name: {activity_name}")
        except Exception as e:
            print("Error decoding activity name:", e)
            return "Invalid activity name", 400
        
    if not activity_name:
        return "Activity not found", 404
    
    # Get all participants in the same activity
    participants = Participants.query.filter_by(activity_name=activity_name).all()
    print(f"Received activity_name: {activity_name}")

    return render_template("view_activity.html", activity_name=activity_name, participants=participants, admin=admin)

#Export File
@app.route('/export', methods=['GET'])
def export():
    export_type = request.args.get('type')  # Get the export type (pdf or excel)
    activity_name = request.args.get('activity')

    if not activity_name:
        return "Activity parameter is required", 400

    # Query database for participant data
    participants = Participants.query.filter_by(activity_name=activity_name).all()

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
                            leftMargin=58, rightMargin=58, 
                            topMargin=70, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()

    # Define logo path at the start
    logo_path = "static/images/STC_Logo.png"  

    # Instructions paragraph
    instructions = Paragraph(
        """
        <p>In order for us to improve future Save the Children activities, please truthfully answer the following questions based on your observations and experience.</p>
        <p><b>Using the scale of 1 to 3 where:</b></p>
            <ul>
                <li><b>1</b> - DISAGREE</li>
                <li><b>2</b> - NEUTRAL</li>
                <li><b>3</b> - AGREE</li>
            </ul>
            <p>Please click zero <b>0</b> if NOT Applicable.</p>
            """, styles["Normal"]
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

        # Add logo (AFTER defining logo_path)
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=90, height=90)  # Adjust logo size as needed
            elements.append(logo)
            elements.append(Spacer(1, 12))  # Add spacing below the logo
        else:
            print(f"Warning: Logo not found at {logo_path}")  # Log missing logo instead of raising error

        title_style = ParagraphStyle(
            name="CustomTitle",
            fontName="Helvetica-Bold", 
            fontSize=18,               
            alignment=TA_CENTER,       
            spaceAfter=14,            
            leading=24
        )

        # Title
        title = Paragraph(f"<b>Evaluation and Feedback for {activity_name}</b>", title_style)

        header_table = Table([[logo, title]], colWidths=[100, 400])  # Adjust widths as needed

        # Apply table style (align logo to the left and title to the center)
        header_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),  # Align items to the top
            ("ALIGN", (0, 0), (0, 0), "LEFT"),  # Align logo to the left
            ("ALIGN", (1, 0), (1, 0), "CENTER"),  # Align title to the center
        ]))

        elements.append(title)
        elements.append(Spacer(1, 12))  # Spacing

        # Instructions
        elements.append(instructions)
        elements.append(Spacer(1, 12))  # Spacing

        # Participant Info
        participant_info = Paragraph(
            f"<b>Participant:</b> {participant.name}<br/>" 
            f"<b>Date:</b> {participant.date} <br/>"
            f"<b>Venue:</b> {participant.venue} <br/>"
            f"<b>School:</b> {participant.school} <br/>" 
            f"<b>District:</b> {participant.district} <br/>"
            f"<b>Facilitator:</b> {participant.facilitator_name} <br/>"
            f"<b>Barangay/Municipal:</b> {participant.address} <br/>", 
            styles["Normal"]
        )
        elements.append(participant_info)
        elements.append(Spacer(1, 12))  # Space before table

        centered_style = ParagraphStyle(name="Centered", parent=styles["Normal"], alignment=TA_CENTER)

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
                    Paragraph(assessment.assessment_text, styles["Normal"]),
                    Paragraph(str(response.response), centered_style),
                    Paragraph(response.comment if response.comment else "N/A", centered_style)
                ])

        # Create table
        table_data = []
        table_styles = [
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 0), (1, -1), "CENTER"),  # Center align Rating
            ("ALIGN", (2, 0), (2, -1), "CENTER"),  # Center align Comments
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]

        for category, questions in category_dict.items():
            table_data.append([f"{category}", "Rating", "Comment"])
            table_styles.append(("BACKGROUND", (0, len(table_data)-1), (2, len(table_data)-1), colors.lightblue))
            table_styles.append(("FONTNAME", (0, len(table_data)-1), (2, len(table_data)-1), "Helvetica-Bold"))
            table_styles.append(("ALIGN", (0, len(table_data)-1), (2, len(table_data)-1), "CENTER"))

            for row in questions:
                table_data.append(row)

        table = Table(table_data, colWidths=[3.8 * inch, 1 * inch, 2.2 * inch])  # Adjust column widths
        table.setStyle(TableStyle(table_styles))

        elements.append(table)
        elements.append(Spacer(1, 24))  # Space before next section

        # Additional Comments
        if additional_responses:
            elements.append(Paragraph("<b>Additional Comments</b>", styles["Heading2"]))
            elements.append(Spacer(1, 12))

            additional_table_data = [["Additional Question", "Response"]]
            additional_table_styles = [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]

            for add_response in additional_responses:
                additional_question = AdditionalComment.query.filter_by(id=add_response.additional_comment_id).first()
                if additional_question:
                    additional_table_data.append([
                        Paragraph(additional_question.additional_question, styles["Normal"]),
                        Paragraph(add_response.comment_response, centered_style)
                    ])

            additional_table = Table(additional_table_data, colWidths=[3.4 * inch, 3.4 * inch])
            additional_table.setStyle(TableStyle(additional_table_styles))

            elements.append(additional_table)
            elements.append(Spacer(1, 24))  # Space before next section

    doc.build(elements)
    output.seek(0)
    return send_file(output, download_name="assessment_report.pdf", as_attachment=True, mimetype="application/pdf")

#View Total Participnats
@app.route('/view-total-participant')
def view_total_participant():
    activity_name = request.args.get("activity_name")
    admin = Admin.query.filter_by(username=session['admin']).first()

    if activity_name:
        activity_name = urllib.parse.unquote(activity_name)

    # If no specific activity is provided, show all participants
    if activity_name == "all":
        participants = Participants.query.all()
        activity_name = "All Activities"
    else:
        participants = Participants.query.filter_by(activity_name=activity_name).all()

    if not participants:
        return f"No participants found for {activity_name}", 404

    return render_template("view_total_participant.html", activity_name=activity_name, participants=participants, admin=admin)

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

@app.route('/admin/settings')
def admin_settings():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    participants = Participants.query.all()
# Get the most recent 5 logins
    recent_logins = AdminLoginActivity.query.filter_by(admin_id=admin.id)\
                        .order_by(AdminLoginActivity.timestamp.desc())\
                        .limit(5).all()

    # Get ALL login activity
    all_logins = AdminLoginActivity.query.filter_by(admin_id=admin.id)\
                    .order_by(AdminLoginActivity.timestamp.desc()).all()

    return render_template(
        'admin_settings.html',
        admin=admin,
        participants=participants,
        recent_logins=recent_logins,
        all_logins=all_logins
    )

@app.route('/admin/profile')
def admin_profile():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    participants = Participants.query.all()

    return render_template('admin_profile.html', admin=admin, participants=participants, current_time=datetime.now().timestamp())

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

    # Handle profile picture upload
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure directory exists
        file.save(file_path)

        admin.profile_image = f"/static/uploads/{filename}"  # Save path in DB

        print("Saved profile picture path:", admin.profile_image)  # Debugging print

    try:
        db.session.commit()
        return jsonify({"success": True, "profile_picture": admin.profile_image})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/admin/results')
def admin_results():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))
    
    admin = Admin.query.filter_by(username=session['admin']).first()
    
    try:
        assessments = AssessmentResponse.query.all()
        print(f"Fetched {len(assessments)} assessments")  # Debugging
    except Exception as e:
        print("Database error:", e)
        return "Database connection failed"

    categories = [
        "About the topic/s", "About the materials", "About the facilitator/s",
        "About the food and venue", "About Save The Children Staff Support"
    ]

    # Store ratings per category with question numbers
    category_data = {category: [] for category in categories}

    for assessment in assessments:
        if assessment.category in category_data:
            try:
                category_data[assessment.category].append({
                    "question_number": assessment.assessment_number,
                    "rating": int(assessment.response)  # Ensure it's an int
                })
            except ValueError:
                print(f"Invalid response value for {assessment.assessment_number}")
           
    print("Category Data:", category_data)

    return render_template( 'admin_results.html', admin=admin, category_data=category_data)

# Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin'))

@app.route('/instructions')
def instructions(): 
    return render_template("instructions.html")

@app.route('/participant', methods=['GET', 'POST'])
def participant():
    if request.method == 'POST':
        try:
            name = request.form['name']
            activity_name = request.form['activity_name']
            venue = request.form['venue']
            school = request.form['school']
            district = request.form['district']
            facilitator_name = request.form['facilitator_name']
            address = request.form['address']
            date_str = request.form['date']
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            new_participant = Participants(
                name=name,
                activity_name=activity_name,
                venue=venue,
                school=school,
                district=district,
                facilitator_name=facilitator_name,
                address=address,
                date=date
            )

            db.session.add(new_participant)
            db.session.commit()

             # ✅ Store user ID in session for assessment_questions route
            session['participant_id'] = new_participant.id

            print("✅ Data saved successfully!")  # Debugging line

            # Redirect to child form after submission
            return redirect(url_for('assessment_questions'))

        except Exception as e:
            print(f"❌ Error inserting data: {e}")  # Debugging line

    return render_template("assessment.html")

@app.route('/assessment_questions', methods=['GET', 'POST'])
def assessment_questions():
    participant_id = session.get('participant_id')

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
                return redirect(url_for('thank_you'))  # Redirect to Thank You page
        
        except Exception as e:
            db.session.rollback()
            flash(f"Error saving responses: {e}", "danger")

    # Retrieve the current question
    assessment = db.session.query(Assessment).filter_by(id=current_assessment_number).first()

    return render_template('questionnaire.html', 
                           assessment=assessment, 
                           is_last_question=is_last_question, 
                           questions_by_category=questions_by_category, additional_question=additional_questions)

@app.route('/search_participant', methods=['GET'])
def search_participant():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify([])  # Return empty list if query is empty

    # Search for participants by name or activity
    participants = Participants.query.filter(
        (Participants.name.ilike(f"%{query}%")) | 
        (Participants.activity_name.ilike(f"%{query}%"))
    ).all()

    # Convert results to JSON format
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
    return render_template('thankyou.html')

# Run App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0', port=5001, debug=True)

