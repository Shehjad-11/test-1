from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.routes import bp
from app.routes.forms import ProjectForm, ApplicationForm, SubmissionForm, MessageForm, FeedbackForm
from app.models import Project, Application, Submission, Message, Notification, User
from app.services.notification_service import NotificationService
from datetime import datetime
import json

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    # Get recent projects for homepage
    recent_projects = Project.query.filter_by(status='open').order_by(Project.created_at.desc()).limit(6).all()
    return render_template('index.html', projects=recent_projects)

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'company':
        return redirect(url_for('main.company_dashboard'))
    else:
        return redirect(url_for('main.developer_dashboard'))

@bp.route('/company-dashboard')
@login_required
def company_dashboard():
    if current_user.role != 'company':
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    projects = current_user.projects.order_by(Project.created_at.desc()).all()
    
    # Calculate stats
    total_projects = len(projects)
    active_projects = len([p for p in projects if p.status in ['open', 'shortlisting', 'submission']])
    completed_projects = len([p for p in projects if p.status == 'completed'])
    
    return render_template('company/dashboard.html', 
                         projects=projects,
                         total_projects=total_projects,
                         active_projects=active_projects,
                         completed_projects=completed_projects)

@bp.route('/developer-dashboard')
@login_required
def developer_dashboard():
    if current_user.role != 'developer':
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    applications = current_user.applications.order_by(Application.applied_at.desc()).all()
    
    # Calculate stats
    total_applications = len(applications)
    shortlisted = len([a for a in applications if a.status == 'shortlisted'])
    submissions = len([a for a in applications if a.submission])
    wins = len([a for a in applications if a.submission and a.submission.is_winner])
    
    return render_template('developer/dashboard.html',
                         applications=applications,
                         total_applications=total_applications,
                         shortlisted=shortlisted,
                         submissions=submissions,
                         wins=wins)

@bp.route('/projects')
def projects():
    page = request.args.get('page', 1, type=int)
    skill_filter = request.args.get('skill', '')
    status_filter = request.args.get('status', 'open')
    
    query = Project.query.filter_by(status=status_filter)
    
    if skill_filter:
        query = query.filter(Project.required_skills.contains(skill_filter))
    
    projects = query.order_by(Project.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False)
    
    return render_template('projects/list.html', projects=projects, skill_filter=skill_filter)

@bp.route('/project/<int:id>')
def project_detail(id):
    project = Project.query.get_or_404(id)
    
    # Check if current user has applied
    user_application = None
    if current_user.is_authenticated and current_user.role == 'developer':
        user_application = Application.query.filter_by(
            project_id=id, developer_id=current_user.id).first()
    
    return render_template('projects/detail.html', 
                         project=project, 
                         user_application=user_application)

@bp.route('/create-project', methods=['GET', 'POST'])
@login_required
def create_project():
    if current_user.role != 'company':
        flash('Only companies can create projects.', 'error')
        return redirect(url_for('main.index'))
    
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            company_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            required_skills=form.required_skills.data,
            deadline=form.deadline.data,
            winner_reward=form.winner_reward.data,
            participation_reward=form.participation_reward.data,
            max_shortlist=form.max_shortlist.data
        )
        
        db.session.add(project)
        db.session.commit()
        
        flash('Project created successfully!', 'success')
        return redirect(url_for('main.company_dashboard'))
    
    return render_template('projects/create.html', form=form)

@bp.route('/apply/<int:project_id>', methods=['GET', 'POST'])
@login_required
def apply_project(project_id):
    if current_user.role != 'developer':
        flash('Only developers can apply to projects.', 'error')
        return redirect(url_for('main.project_detail', id=project_id))
    
    project = Project.query.get_or_404(project_id)
    
    # Check if already applied
    existing_application = Application.query.filter_by(
        project_id=project_id, developer_id=current_user.id).first()
    
    if existing_application:
        flash('You have already applied to this project.', 'warning')
        return redirect(url_for('main.project_detail', id=project_id))
    
    if project.status != 'open':
        flash('This project is no longer accepting applications.', 'error')
        return redirect(url_for('main.project_detail', id=project_id))
    
    form = ApplicationForm()
    if form.validate_on_submit():
        application = Application(
            project_id=project_id,
            developer_id=current_user.id,
            cover_letter=form.cover_letter.data
        )
        
        db.session.add(application)
        db.session.commit()
        
        # Send notification to company
        NotificationService.create_notification(
            project.company_id,
            'New Application',
            f'{current_user.username} applied to your project "{project.title}"',
            'application'
        )
        
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('main.project_detail', id=project_id))
    
    return render_template('projects/apply.html', form=form, project=project)

@bp.route('/project/<int:project_id>/manage')
@login_required
def manage_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if project.company_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    applications = project.applications.order_by(Application.applied_at.desc()).all()
    shortlisted = [app for app in applications if app.status == 'shortlisted']
    submissions = project.submissions.all()
    
    return render_template('projects/manage.html', 
                         project=project, 
                         applications=applications,
                         shortlisted=shortlisted,
                         submissions=submissions)

@bp.route('/shortlist/<int:application_id>')
@login_required
def shortlist_application(application_id):
    application = Application.query.get_or_404(application_id)
    project = application.project
    
    if project.company_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    # Check if we can still shortlist
    current_shortlisted = Application.query.filter_by(
        project_id=project.id, status='shortlisted').count()
    
    if current_shortlisted >= project.max_shortlist:
        flash('Maximum shortlist limit reached.', 'error')
        return redirect(url_for('main.manage_project', project_id=project.id))
    
    application.status = 'shortlisted'
    db.session.commit()
    
    # Update project status if needed
    if project.status == 'open':
        project.status = 'shortlisting'
        db.session.commit()
    
    # Send notification to developer
    NotificationService.create_notification(
        application.developer_id,
        'Shortlisted!',
        f'You have been shortlisted for project "{project.title}"',
        'shortlist'
    )
    
    flash('Application shortlisted successfully!', 'success')
    return redirect(url_for('main.manage_project', project_id=project.id))

@bp.route('/submit/<int:application_id>', methods=['GET', 'POST'])
@login_required
def submit_work(application_id):
    application = Application.query.get_or_404(application_id)
    
    if application.developer_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    if application.status != 'shortlisted':
        flash('You must be shortlisted to submit work.', 'error')
        return redirect(url_for('main.project_detail', id=application.project_id))
    
    # Check if already submitted
    if application.submission:
        flash('You have already submitted work for this project.', 'warning')
        return redirect(url_for('main.project_detail', id=application.project_id))
    
    form = SubmissionForm()
    if form.validate_on_submit():
        submission = Submission(
            application_id=application_id,
            project_id=application.project_id,
            github_url=form.github_url.data,
            demo_url=form.demo_url.data,
            figma_url=form.figma_url.data,
            description=form.description.data
        )
        
        db.session.add(submission)
        
        # Update project status if this is the first submission
        if application.project.status == 'shortlisting':
            application.project.status = 'submission'
        
        db.session.commit()
        
        # Send notification to company
        NotificationService.create_notification(
            application.project.company_id,
            'New Submission',
            f'{current_user.username} submitted work for "{application.project.title}"',
            'submission'
        )
        
        flash('Work submitted successfully!', 'success')
        return redirect(url_for('main.project_detail', id=application.project_id))
    
    return render_template('projects/submit.html', form=form, application=application)

@bp.route('/submission/<int:submission_id>/feedback', methods=['GET', 'POST'])
@login_required
def submission_feedback(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    
    if submission.project.company_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    form = FeedbackForm()
    if form.validate_on_submit():
        submission.score = form.score.data
        submission.feedback = form.feedback.data
        db.session.commit()
        
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('main.manage_project', project_id=submission.project_id))
    
    # Pre-populate form if feedback exists
    if submission.score:
        form.score.data = submission.score
        form.feedback.data = submission.feedback
    
    return render_template('projects/feedback.html', form=form, submission=submission)

@bp.route('/declare-winner/<int:submission_id>')
@login_required
def declare_winner(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    project = submission.project
    
    if project.company_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    # Mark as winner
    submission.is_winner = True
    project.status = 'completed'
    
    # Update reputation scores
    winner_profile = submission.application.developer_user.developer_profile
    if winner_profile:
        winner_profile.reputation_score += 10
    
    # Give participation rewards to all shortlisted candidates
    shortlisted_apps = Application.query.filter_by(
        project_id=project.id, status='shortlisted').all()
    
    for app in shortlisted_apps:
        if app.submission:
            dev_profile = app.developer_user.developer_profile
            if dev_profile:
                dev_profile.reputation_score += 2
    
    db.session.commit()
    
    # Send notifications
    NotificationService.create_notification(
        submission.application.developer_id,
        'Congratulations! You Won!',
        f'You won the project "{project.title}" and earned ${project.winner_reward}!',
        'winner'
    )
    
    flash('Winner declared successfully!', 'success')
    return redirect(url_for('main.manage_project', project_id=project.id))

@bp.route('/messages')
@login_required
def messages():
    # Get all conversations for current user
    sent_messages = Message.query.filter_by(sender_id=current_user.id).all()
    received_messages = Message.query.filter_by(recipient_id=current_user.id).all()
    
    # Group by conversation partner
    conversations = {}
    for msg in sent_messages + received_messages:
        partner_id = msg.recipient_id if msg.sender_id == current_user.id else msg.sender_id
        if partner_id not in conversations:
            conversations[partner_id] = []
        conversations[partner_id].append(msg)
    
    # Sort conversations by latest message
    for partner_id in conversations:
        conversations[partner_id].sort(key=lambda x: x.sent_at, reverse=True)
    
    return render_template('messages/list.html', conversations=conversations)

@bp.route('/notifications')
@login_required
def notifications():
    notifications = NotificationService.get_user_notifications(current_user.id)
    return render_template('notifications/list.html', notifications=notifications)

@bp.route('/api/notifications/mark-read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    success = NotificationService.mark_as_read(notification_id, current_user.id)
    return jsonify({'success': success})

@bp.route('/api/notifications/unread-count')
@login_required
def unread_notifications_count():
    count = NotificationService.get_unread_count(current_user.id)
    return jsonify({'count': count})