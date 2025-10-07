"""
Flask Web Application for Job Sourcing Dashboard
Displays scraped EdJoin positions and allows resume uploads
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import json
import os
from datetime import datetime
import uuid
from candidate_matching import CandidateMatcher
from google_forms_integration import GoogleFormsSubmitter
from resume_handling import GoogleFormsWithResume, create_resume_upload_route
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Configuration
JOBS_FILE = "edjoin_jobs.json"
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# Admin Authentication
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')  # Change this password!

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize candidate matcher and Google Forms submitter
candidate_matcher = CandidateMatcher()
google_forms_submitter = GoogleFormsSubmitter()
resume_handler = GoogleFormsWithResume()

# Add resume upload route
app = create_resume_upload_route(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the admin panel.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def load_jobs():
    """Load jobs from JSON file with multiple fallback paths"""
    possible_paths = [
        JOBS_FILE,
        f"./{JOBS_FILE}",
        f"/app/{JOBS_FILE}",
        f"/app/app/{JOBS_FILE}"
    ]
    
    for file_path in possible_paths:
        try:
            print(f"DEBUG: Trying to load jobs from {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                jobs = json.load(f)
                print(f"DEBUG: Successfully loaded {len(jobs)} jobs from {file_path}")
                return jobs
        except FileNotFoundError:
            print(f"DEBUG: File not found: {file_path}")
            continue
        except Exception as e:
            print(f"DEBUG: Error loading from {file_path}: {e}")
            continue
    
    print("DEBUG: No jobs file found in any location")
    return []

def save_application(application_data):
    """Save job application to file"""
    applications_file = "applications.json"
    applications = []
    
    # Load existing applications
    if os.path.exists(applications_file):
        try:
            with open(applications_file, 'r', encoding='utf-8') as f:
                applications = json.load(f)
        except:
            applications = []
    
    # Add new application
    applications.append(application_data)
    
    # Save back to file
    with open(applications_file, 'w', encoding='utf-8') as f:
        json.dump(applications, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    """Main dashboard page - displays all jobs directly"""
    jobs = load_jobs()
    
    # Debug: Print job count
    print(f"DEBUG: Loading {len(jobs)} jobs for main route")
    
    # Group jobs by role
    jobs_by_role = {}
    for job in jobs:
        role = job.get('role', 'Other')
        if role not in jobs_by_role:
            jobs_by_role[role] = []
        jobs_by_role[role].append(job)
    
    return render_template('index.html', jobs=jobs, jobs_by_role=jobs_by_role)

@app.route('/educationedjoin2')
def educationedjoin2():
    """Main working route - displays all jobs"""
    jobs = load_jobs()
    
    # Debug: Print job count
    print(f"DEBUG: Loading {len(jobs)} jobs for educationedjoin2 route")
    
    # Group jobs by role
    jobs_by_role = {}
    for job in jobs:
        role = job.get('role', 'Other')
        if role not in jobs_by_role:
            jobs_by_role[role] = []
        jobs_by_role[role].append(job)
    
    return render_template('index.html', jobs=jobs, jobs_by_role=jobs_by_role)

@app.route('/api/jobs')
def api_jobs():
    """API endpoint for jobs data"""
    jobs = load_jobs()
    return jsonify(jobs)

@app.route('/debug')
def debug():
    """Debug endpoint to check data loading"""
    import os
    
    debug_info = {
        "jobs_count": len(load_jobs()),
        "current_directory": os.getcwd(),
        "files_in_dir": os.listdir('.'),
        "jobs_file_exists": os.path.exists(JOBS_FILE),
        "jobs_file_size": os.path.getsize(JOBS_FILE) if os.path.exists(JOBS_FILE) else 0
    }
    
    return jsonify(debug_info)

@app.route('/api/jobs/<role>')
def api_jobs_by_role(role):
    """API endpoint for jobs filtered by role"""
    jobs = load_jobs()
    filtered_jobs = [job for job in jobs if job.get('role', '').lower() == role.lower()]
    return jsonify(filtered_jobs)

@app.route('/job/<int:job_index>')
def job_detail(job_index):
    """Job detail page"""
    jobs = load_jobs()
    print(f"DEBUG: Job detail - job_index={job_index}, total_jobs={len(jobs)}")
    
    if not jobs:
        print("DEBUG: No jobs loaded, redirecting to main")
        flash('No jobs available. Please try again later.', 'error')
        return redirect(url_for('index'))
    
    if job_index >= 0 and job_index < len(jobs):
        job = jobs[job_index]
        return render_template('job_detail.html', job=job, job_index=job_index)
    else:
        print(f"DEBUG: Invalid job_index {job_index} for {len(jobs)} jobs")
        flash('Job not found', 'error')
        return redirect(url_for('index'))

@app.route('/apply/<int:job_index>', methods=['GET', 'POST'])
def apply_job(job_index):
    """Job application page"""
    jobs = load_jobs()
    print(f"DEBUG: Apply job - job_index={job_index}, total_jobs={len(jobs)}")
    
    if not jobs:
        print("DEBUG: No jobs loaded, redirecting to main")
        flash('No jobs available. Please try again later.', 'error')
        return redirect(url_for('index'))
    
    if job_index < 0 or job_index >= len(jobs):
        print(f"DEBUG: Invalid job_index {job_index} for {len(jobs)} jobs")
        flash('Job not found', 'error')
        return redirect(url_for('index'))
    
    job = jobs[job_index]
    print(f"DEBUG: Found job: {job.get('title', 'No title')}")
    
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()
        
        # Validate required fields
        if not name or not email:
            flash('Name and email are required', 'error')
            return render_template('apply.html', job=job, job_index=job_index)
        
        # Handle file upload
        resume_filename = None
        if 'resume' in request.files:
            file = request.files['resume']
            if file and file.filename and allowed_file(file.filename):
                # Generate unique filename
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                resume_filename = f"{uuid.uuid4()}.{file_extension}"
                file.save(os.path.join(UPLOAD_FOLDER, resume_filename))
            elif file and file.filename:
                flash('Invalid file type. Please upload PDF, DOC, or DOCX files only.', 'error')
                return render_template('apply.html', job=job, job_index=job_index)
        
        # Save application
        application_data = {
            'id': str(uuid.uuid4()),
            'job_title': job.get('title', ''),
            'job_url': job.get('url', ''),
            'job_role': job.get('role', ''),
            'applicant_name': name,
            'applicant_email': email,
            'applicant_phone': phone,
            'cover_letter': cover_letter,
            'resume_filename': resume_filename,
            'applied_at': datetime.now().isoformat()
        }
        
        save_application(application_data)
        
        flash('Application submitted successfully! We will review your application and get back to you soon.', 'success')
        return redirect(url_for('index'))
    
    return render_template('apply.html', job=job, job_index=job_index)

@app.route('/embed')
def embed():
    """Embeddable widget for external websites"""
    jobs = load_jobs()
    return render_template('embed.html', jobs=jobs)

@app.route('/embed-enhanced')
def embed_enhanced():
    """Enhanced embeddable widget with candidate registration"""
    jobs = load_jobs()
    return render_template('embed_enhanced.html', jobs=jobs)

@app.route('/candidate/register', methods=['GET', 'POST'])
def candidate_register():
    """Candidate registration page"""
    if request.method == 'POST':
        # Handle candidate registration
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        years_experience = int(request.form.get('years_experience', 0))
        education_level = request.form.get('education_level', '').strip()
        preferred_roles = request.form.getlist('preferred_roles')
        preferred_locations = request.form.get('preferred_locations', '').strip()
        skills = request.form.get('skills', '').strip()
        
        # Validate required fields
        if not name or not email:
            flash('Name and email are required', 'error')
            return render_template('candidate_register.html')
        
        # Handle resume upload
        resume_filename = None
        if 'resume' in request.files:
            file = request.files['resume']
            if file and file.filename and allowed_file(file.filename):
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                resume_filename = f"{uuid.uuid4()}.{file_extension}"
                file.save(os.path.join(UPLOAD_FOLDER, resume_filename))
        
        # Create candidate profile
        candidate_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'years_experience': years_experience,
            'education_level': education_level,
            'preferred_roles': preferred_roles,
            'preferred_locations': [loc.strip() for loc in preferred_locations.split(',') if loc.strip()],
            'skills': [skill.strip() for skill in skills.split(',') if skill.strip()],
            'resume_filename': resume_filename
        }
        
        # Save candidate and find matches
        candidate_id = candidate_matcher.save_candidate(candidate_data)
        matches = candidate_matcher.find_matches(candidate_id)
        
        # Handle resume upload and submit to Google Forms
        resume_file = request.files.get('resume')
        success, resume_url = resume_handler.submit_candidate_with_resume(candidate_data, resume_file)
        
        if success:
            flash(f'Registration successful! We found {len(matches)} matching positions for you.', 'success')
        else:
            flash('Registration completed, but there was an issue with form submission.', 'warning')
        
        return redirect(url_for('candidate_dashboard', candidate_id=candidate_id))
    
    return render_template('candidate_register.html')

@app.route('/candidate/<candidate_id>')
def candidate_dashboard(candidate_id):
    """Candidate dashboard showing their matches"""
    matches = candidate_matcher.get_candidate_matches(candidate_id)
    candidates = candidate_matcher.load_candidates()
    candidate = next((c for c in candidates if c.get('id') == candidate_id), None)
    
    if not candidate:
        flash('Candidate not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('candidate_dashboard.html', candidate=candidate, matches=matches)

@app.route('/api/candidate-matches/<candidate_id>')
def api_candidate_matches(candidate_id):
    """API endpoint for candidate matches"""
    matches = candidate_matcher.get_candidate_matches(candidate_id)
    return jsonify(matches)

@app.route('/api/job-candidates/<path:job_url>')
def api_job_candidates(job_url):
    """API endpoint for top candidates for a specific job"""
    candidates = candidate_matcher.get_top_candidates_for_job(job_url)
    return jsonify(candidates)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin_applications'))
        else:
            flash('Invalid password. Please try again.', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/admin/applications')
@admin_required
def admin_applications():
    """Admin page to view applications"""
    applications_file = "applications.json"
    applications = []
    
    if os.path.exists(applications_file):
        try:
            with open(applications_file, 'r', encoding='utf-8') as f:
                applications = json.load(f)
        except:
            pass
    
    return render_template('admin_applications.html', applications=applications)

@app.route('/admin/candidates')
@admin_required
def admin_candidates():
    """Admin page to view all candidates and matches"""
    candidates = candidate_matcher.load_candidates()
    matches = candidate_matcher.load_matches()
    return render_template('admin_candidates.html', candidates=candidates, matches=matches)

@app.route('/admin/refresh-jobs', methods=['POST'])
@admin_required
def refresh_jobs():
    """Manually refresh job positions"""
    try:
        import subprocess
        import sys
        
        # Run the production scraper
        result = subprocess.run(
            [sys.executable, 'production_scraper.py'], 
            capture_output=True, 
            text=True, 
            timeout=1800  # 30 minute timeout
        )
        
        if result.returncode == 0:
            # Reload jobs from updated file
            jobs = load_jobs()
            flash(f'Jobs refreshed successfully! Found {len(jobs)} positions.', 'success')
        else:
            flash(f'Error refreshing jobs: {result.stderr}', 'error')
            
    except subprocess.TimeoutExpired:
        flash('Job refresh timed out after 30 minutes', 'error')
    except Exception as e:
        flash(f'Error refreshing jobs: {str(e)}', 'error')
    
    return redirect(url_for('admin_applications'))

@app.route('/api/refresh-status')
def refresh_status():
    """Get current refresh status"""
    try:
        jobs = load_jobs()
        last_update = None
        
        if jobs:
            # Get the most recent scraping timestamp
            timestamps = [job.get('scraped_at') for job in jobs if job.get('scraped_at')]
            if timestamps:
                last_update = max(timestamps)
        
        return jsonify({
            'total_positions': len(jobs),
            'last_update': last_update,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
