from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, CompanyProfileForm, DeveloperProfileForm
from app.models import User, CompanyProfile, DeveloperProfile
import json

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.dashboard')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please complete your profile.', 'success')
        login_user(user)
        
        if user.role == 'company':
            return redirect(url_for('auth.company_profile'))
        else:
            return redirect(url_for('auth.developer_profile'))
    
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/company-profile', methods=['GET', 'POST'])
@login_required
def company_profile():
    if current_user.role != 'company':
        flash('Access denied.', 'error')
        return redirect(url_for('main.dashboard'))
    
    form = CompanyProfileForm()
    profile = current_user.company_profile
    
    if form.validate_on_submit():
        if profile is None:
            profile = CompanyProfile(user_id=current_user.id)
        
        profile.company_name = form.company_name.data
        profile.description = form.description.data
        profile.website = form.website.data
        profile.industry = form.industry.data
        profile.size = form.size.data
        profile.location = form.location.data
        
        db.session.add(profile)
        db.session.commit()
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    if profile:
        form.company_name.data = profile.company_name
        form.description.data = profile.description
        form.website.data = profile.website
        form.industry.data = profile.industry
        form.size.data = profile.size
        form.location.data = profile.location
    
    return render_template('auth/company_profile.html', title='Company Profile', form=form)

@bp.route('/developer-profile', methods=['GET', 'POST'])
@login_required
def developer_profile():
    if current_user.role != 'developer':
        flash('Access denied.', 'error')
        return redirect(url_for('main.dashboard'))
    
    form = DeveloperProfileForm()
    profile = current_user.developer_profile
    
    if form.validate_on_submit():
        if profile is None:
            profile = DeveloperProfile(user_id=current_user.id)
        
        profile.full_name = form.full_name.data
        profile.bio = form.bio.data
        profile.skills = form.skills.data
        profile.experience_level = form.experience_level.data
        profile.portfolio_url = form.portfolio_url.data
        profile.github_url = form.github_url.data
        profile.linkedin_url = form.linkedin_url.data
        
        db.session.add(profile)
        db.session.commit()
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    if profile:
        form.full_name.data = profile.full_name
        form.bio.data = profile.bio
        form.skills.data = profile.skills
        form.experience_level.data = profile.experience_level
        form.portfolio_url.data = profile.portfolio_url
        form.github_url.data = profile.github_url
        form.linkedin_url.data = profile.linkedin_url
    
    return render_template('auth/developer_profile.html', title='Developer Profile', form=form)