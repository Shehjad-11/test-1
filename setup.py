#!/usr/bin/env python3
"""
Setup script for CollabPlatform
Initializes the database and creates sample data
"""

from app import create_app, db
from app.models import User, CompanyProfile, DeveloperProfile, Project
from datetime import datetime, timedelta
import os

def setup_database():
    """Initialize database and create sample data"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Setting up CollabPlatform database...")
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Check if data already exists
        if User.query.first():
            print("⚠️  Database already has data. Skipping sample data creation.")
            return
        
        # Create sample users
        print("👥 Creating sample users...")
        
        # Admin user
        admin = User(username='admin', email='admin@collabplatform.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Company user
        company_user = User(username='techcorp', email='hr@techcorp.com', role='company')
        company_user.set_password('company123')
        db.session.add(company_user)
        
        # Developer users
        dev1 = User(username='john_dev', email='john@example.com', role='developer')
        dev1.set_password('dev123')
        db.session.add(dev1)
        
        dev2 = User(username='jane_designer', email='jane@example.com', role='developer')
        dev2.set_password('dev123')
        db.session.add(dev2)
        
        db.session.commit()
        print("✅ Sample users created")
        
        # Create profiles
        print("📝 Creating user profiles...")
        
        # Company profile
        company_profile = CompanyProfile(
            user_id=company_user.id,
            company_name='TechCorp Solutions',
            description='Leading technology solutions provider specializing in web and mobile applications.',
            website='https://techcorp.com',
            industry='Technology',
            size='51-200',
            location='San Francisco, CA'
        )
        db.session.add(company_profile)
        
        # Developer profiles
        dev1_profile = DeveloperProfile(
            user_id=dev1.id,
            full_name='John Developer',
            bio='Full-stack developer with 3 years of experience in modern web technologies.',
            skills='JavaScript, React, Node.js, Python, PostgreSQL, MongoDB',
            experience_level='intermediate',
            github_url='https://github.com/johndev',
            portfolio_url='https://johndev.portfolio.com'
        )
        db.session.add(dev1_profile)
        
        dev2_profile = DeveloperProfile(
            user_id=dev2.id,
            full_name='Jane Designer',
            bio='UI/UX Designer passionate about creating beautiful and functional user experiences.',
            skills='UI/UX Design, Figma, Adobe Creative Suite, Prototyping, User Research',
            experience_level='advanced',
            portfolio_url='https://janedesigner.com',
            linkedin_url='https://linkedin.com/in/janedesigner'
        )
        db.session.add(dev2_profile)
        
        db.session.commit()
        print("✅ User profiles created")
        
        # Create sample projects
        print("🚀 Creating sample projects...")
        
        projects_data = [
            {
                'title': 'E-commerce Mobile App Design',
                'description': 'Design a modern, user-friendly mobile app for our e-commerce platform. Should include user authentication, product browsing, shopping cart, and checkout flow. Looking for clean, modern design that works well on both iOS and Android.',
                'required_skills': 'UI/UX Design, Mobile Design, Figma, Prototyping, User Experience',
                'winner_reward': 1500.0,
                'participation_reward': 100.0,
                'days_from_now': 14
            },
            {
                'title': 'React Dashboard Development',
                'description': 'Build a responsive admin dashboard using React and modern JavaScript. Should include data visualization, user management, and real-time updates. Clean code and good documentation required.',
                'required_skills': 'React, JavaScript, HTML/CSS, Chart.js, REST APIs',
                'winner_reward': 2000.0,
                'participation_reward': 150.0,
                'days_from_now': 21
            },
            {
                'title': 'Logo and Brand Identity Design',
                'description': 'Create a complete brand identity package including logo, color palette, typography, and brand guidelines for a new tech startup. Modern, professional look required.',
                'required_skills': 'Logo Design, Brand Identity, Adobe Illustrator, Typography, Color Theory',
                'winner_reward': 800.0,
                'participation_reward': 50.0,
                'days_from_now': 10
            }
        ]
        
        for project_data in projects_data:
            project = Project(
                company_id=company_user.id,
                title=project_data['title'],
                description=project_data['description'],
                required_skills=project_data['required_skills'],
                deadline=datetime.utcnow() + timedelta(days=project_data['days_from_now']),
                winner_reward=project_data['winner_reward'],
                participation_reward=project_data['participation_reward'],
                max_shortlist=5
            )
            db.session.add(project)
        
        db.session.commit()
        print("✅ Sample projects created")
        
        print("\n🎉 Database setup complete!")
        print("\n📋 Sample Login Credentials:")
        print("   Company: hr@techcorp.com / company123")
        print("   Developer: john@example.com / dev123")
        print("   Designer: jane@example.com / dev123")
        print("   Admin: admin@collabplatform.com / admin123")
        print("\n🚀 Start the application with: python run.py")

if __name__ == "__main__":
    setup_database()