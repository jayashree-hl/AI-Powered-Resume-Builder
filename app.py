from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from functools import wraps
import os
import textwrap

app = Flask(__name__)
app.secret_key = "resume_builder_secret_2026"

# =========================
# DATABASE CONFIGURATION
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# DATABASE MODELS
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    linkedin = db.Column(db.String(200))
    education = db.Column(db.Text)
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    projects = db.Column(db.Text)
    summary = db.Column(db.Text)

with app.app_context():
    db.create_all()

# =========================
# LOGIN REQUIRED DECORATOR
# =========================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login to continue.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# =========================
# AI SUMMARY GENERATOR
# =========================
def generate_summary(name, skills, experience):
    skill_list = skills.strip()
    return (
        f"Results-driven professional with expertise in {skill_list}. "
        f"Demonstrated ability to deliver high-quality solutions with a strong commitment to innovation, "
        f"collaboration, and continuous learning. Proven track record in leveraging technical skills to drive "
        f"impactful outcomes and contribute meaningfully to team and organizational goals."
    )

# =========================
# HOME PAGE
# =========================
@app.route('/')
def home():
    user_name = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            user_name = user.name
    return render_template('index.html', user_name=user_name)

# =========================
# LOGIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash("Please fill in all fields.", "danger")
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password. Please try again.", "danger")
            return render_template('login.html')

    return render_template('login.html')

# =========================
# REGISTER
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not name or not email or not password:
            flash("Please fill in all fields.", "danger")
            return render_template('register.html')

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template('register.html')

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template('register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with this email already exists.", "warning")
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# =========================
# RESUME SUBMISSION
# =========================
@app.route('/submit', methods=['POST'])
@login_required
def submit():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    linkedin = request.form.get('linkedin', '').strip()
    education = request.form.get('education', '').strip()
    skills = request.form.get('skills', '').strip()
    experience = request.form.get('experience', '').strip()
    projects = request.form.get('projects', '').strip()

    summary = generate_summary(name, skills, experience)

    new_resume = Resume(
        user_id=session.get('user_id'),
        name=name, email=email, phone=phone, linkedin=linkedin,
        education=education, skills=skills,
        experience=experience, projects=projects, summary=summary
    )
    db.session.add(new_resume)
    db.session.commit()

    return render_template('preview.html',
        name=name, email=email, phone=phone, linkedin=linkedin,
        education=education, skills=skills,
        experience=experience, projects=projects, summary=summary
    )

# =========================
# DOWNLOAD PDF
# =========================
@app.route('/download', methods=['POST'])
@login_required
def download():
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    linkedin = request.form.get('linkedin', '')
    education = request.form.get('education', '')
    skills = request.form.get('skills', '')
    experience = request.form.get('experience', '')
    projects = request.form.get('projects', '')
    summary = request.form.get('summary', '')

    pdf_file = f"/tmp/resume_{name.replace(' ', '_')}.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)

    styles = getSampleStyleSheet()
    story = []

    # Name header
    name_style = ParagraphStyle('Name', fontSize=26, fontName='Helvetica-Bold',
                                 textColor=colors.HexColor('#1a1a2e'), spaceAfter=4)
    story.append(Paragraph(name, name_style))

    # Contact line
    contact_parts = []
    if email: contact_parts.append(f"✉ {email}")
    if phone: contact_parts.append(f"✆ {phone}")
    if linkedin: contact_parts.append(f"in {linkedin}")
    contact_style = ParagraphStyle('Contact', fontSize=10, fontName='Helvetica',
                                    textColor=colors.HexColor('#555555'), spaceAfter=14)
    story.append(Paragraph("   |   ".join(contact_parts), contact_style))

    divider_style = ParagraphStyle('Divider', fontSize=1, spaceAfter=14,
                                    backColor=colors.HexColor('#007bff'))

    def section_header(title):
        hdr = ParagraphStyle('SectionHdr', fontSize=12, fontName='Helvetica-Bold',
                              textColor=colors.HexColor('#007bff'), spaceAfter=6, spaceBefore=14,
                              borderPad=2)
        story.append(Paragraph(title.upper(), hdr))
        story.append(Spacer(1, 2))

    body_style = ParagraphStyle('Body', fontSize=10, fontName='Helvetica',
                                 textColor=colors.HexColor('#333333'), spaceAfter=6, leading=15)

    # Summary
    if summary:
        section_header("Professional Summary")
        story.append(Paragraph(summary, body_style))

    # Education
    if education:
        section_header("Education")
        story.append(Paragraph(education.replace('\n', '<br/>'), body_style))

    # Skills
    if skills:
        section_header("Skills")
        story.append(Paragraph(skills.replace('\n', '<br/>'), body_style))

    # Experience
    if experience:
        section_header("Experience")
        story.append(Paragraph(experience.replace('\n', '<br/>'), body_style))

    # Projects
    if projects:
        section_header("Projects")
        story.append(Paragraph(projects.replace('\n', '<br/>'), body_style))

    doc.build(story)
    return send_file(pdf_file, as_attachment=True,
                     download_name=f"{name.replace(' ', '_')}_Resume.pdf")

# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():
    session.clear()
    flash("You've been logged out successfully.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
