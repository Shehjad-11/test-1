#!/usr/bin/env python3
"""
CollabPlatform - Fair Project Collaboration Platform
Run script for development and production
"""

import os
from app import create_app, db
from app.models import User, CompanyProfile, DeveloperProfile, Project, Application, Submission
from flask_migrate import upgrade

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'CompanyProfile': CompanyProfile,
        'DeveloperProfile': DeveloperProfile,
        'Project': Project,
        'Application': Application,
        'Submission': Submission
    }

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # Create database tables
    upgrade()
    
    # Create sample data if in development
    if app.config.get('ENV') == 'development':
        create_sample_data()

def create_sample_data():
    """Create sample data for development."""
    # Check if data already exists
    if User.query.first():
        return
    
    # Create admin user
    admin = User(username='admin', email='admin@collabplatform.com', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create sample company
    company_user = User(username='techcorp', email='hr@techcorp.com', role='company')
    company_user.set_password('company123')
    db.session.add(company_user)
    
    # Create sample developers
    dev1 = User(username='john_dev', email='john@example.com', role='developer')
    dev1.set_password('dev123')
    db.session.add(dev1)
    
    dev2 = User(username='jane_designer', email='jane@example.com', role='developer')
    dev2.set_password('dev123')
    db.session.add(dev2)
    
    db.session.commit()
    
    # Create company profile
    company_profile = CompanyProfile(
        user_id=company_user.id,
        company_name='TechCorp Solutions',
        description='Leading technology solutions provider',
        website='https://techcorp.com',
        industry='Technology',
        size='51-200',
        location='San Francisco, CA'
    )
    db.session.add(company_profile)
    
    # Create developer profiles
    dev1_profile = DeveloperProfile(
        user_id=dev1.id,
        full_name='John Developer',
        bio='Full-stack developer with 3 years experience',
        skills='JavaScript, React, Node.js, Python, PostgreSQL',
        experience_level='intermediate',
        github_url='https://github.com/johndev',
        portfolio_url='https://johndev.portfolio.com'
    )
    db.session.add(dev1_profile)
    
    dev2_profile = DeveloperProfile(
        user_id=dev2.id,
        full_name='Jane Designer',
        bio='UI/UX Designer passionate about user experience',
        skills='UI/UX Design, Figma, Adobe Creative Suite, Prototyping',
        experience_level='advanced',
        portfolio_url='https://janedesigner.com'
    )
    db.session.add(dev2_profile)
    
    db.session.commit()
    
    # Create sample project
    from datetime import datetime, timedelta
    
    project = Project(
        company_id=company_user.id,
        title='E-commerce Mobile App Design',
        description='Design a modern, user-friendly mobile app for our e-commerce platform. Should include user authentication, product browsing, shopping cart, and checkout flow.',
        required_skills='UI/UX Design, Mobile Design, Figma, Prototyping',
        deadline=datetime.utcnow() + timedelta(days=14),
        winner_reward=1500.0,
        participation_reward=100.0,
        max_shortlist=5
    )
    db.session.add(project)
    db.session.commit()
    
    print("Sample data created successfully!")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)