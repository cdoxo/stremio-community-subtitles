from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from datetime import datetime
import pycountry
from ..models import User, Role
from ..forms import LoginForm, RegistrationForm, ChangePasswordForm, ResetPasswordRequestForm, ResetPasswordForm
from ..extensions import db
from ..languages import LANGUAGES, LANGUAGE_DICT
from ..email import send_confirmation_email, send_password_reset_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'GET' and request.args.get('next'):
        session['next_url'] = request.args.get('next')
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.active:
            flash('Please confirm your email address before logging in. Check your inbox for the confirmation email.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Update user login tracking
        user.last_login_at = user.current_login_at
        user.current_login_at = datetime.utcnow()
        user.last_login_ip = user.current_login_ip
        user.current_login_ip = request.remote_addr
        user.login_count = user.login_count + 1 if user.login_count else 1
        db.session.commit()
        
        login_user(user, remember=form.remember_me.data)
        current_app.logger.info(f"User {user.username} logged in")

        next_page = session.pop('next_url', None) or request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    form.preferred_language.choices = LANGUAGES
    
    # Set default language based on browser preference
    if not form.is_submitted():
        supported_iso_639_1_codes = []
        for code_639_2, _ in LANGUAGES:
            try:
                lang = pycountry.languages.get(alpha_3=code_639_2)
                if lang and hasattr(lang, 'alpha_2'):
                    supported_iso_639_1_codes.append(lang.alpha_2)
            except KeyError:
                current_app.logger.warning(f"pycountry could not find ISO 639-1 for supported language {code_639_2}.")

        if supported_iso_639_1_codes:
            browser_pref_1 = request.accept_languages.best_match(supported_iso_639_1_codes)
            if browser_pref_1:
                try:
                    lang_obj = pycountry.languages.get(alpha_2=browser_pref_1)
                    if lang_obj and hasattr(lang_obj, 'alpha_3'):
                        best_match_2 = lang_obj.alpha_3
                        if best_match_2 in LANGUAGE_DICT:
                            form.preferred_language.data = best_match_2
                        else:
                            current_app.logger.info(f"Browser preferred lang {browser_pref_1} (->{best_match_2}) not in supported app languages.")
                    else:
                        current_app.logger.warning(f"pycountry found {browser_pref_1} but it has no alpha_3 code.")
                except KeyError:
                    current_app.logger.warning(f"pycountry could not convert browser lang code {browser_pref_1} to ISO 639-2.")
        else:
            current_app.logger.warning("No supported ISO 639-1 codes derived for browser preference matching.")
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, 
                    preferred_language=form.preferred_language.data, active=False)
        user.set_password(form.password.data)
        user.generate_manifest_token()
        
        # Add default user role
        user_role = Role.query.filter_by(name='User').first()
        if not user_role:
            user_role = Role(name='User', description='Standard user')
            db.session.add(user_role)
        
        user.roles.append(user_role)
        
        db.session.add(user)
        db.session.commit()
        
        # Send confirmation email
        send_confirmation_email(user)
        
        flash('A confirmation email has been sent to your email address. Please check your inbox to activate your account.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('auth.change_password'))
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been updated', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/change_password.html', title='Change Password', form=form)

@auth_bp.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Send password reset email
            send_password_reset_email(user)
            flash('Check your email for instructions to reset your password', 'info')
        else:
            # Don't reveal that the email doesn't exist for security reasons
            flash('If that email address is in our database, we have sent a password reset link', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)

@auth_bp.route('/resend-confirmation')
def resend_confirmation():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    return render_template('auth/resend_confirmation.html', title='Resend Confirmation Email')

@auth_bp.route('/resend-confirmation', methods=['POST'])
def resend_confirmation_post():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    email = request.form.get('email')
    if not email:
        flash('Email is required.', 'danger')
        return redirect(url_for('auth.resend_confirmation'))
    
    user = User.query.filter_by(email=email).first()
    if user and not user.email_confirmed:
        send_confirmation_email(user)
        flash('A new confirmation email has been sent. Please check your inbox.', 'info')
    else:
        # Don't reveal if the email exists or is already confirmed for security reasons
        flash('If that email address is in our database and not confirmed, we have sent a new confirmation link.', 'info')
    
    return redirect(url_for('auth.login'))

@auth_bp.route('/confirm-email/<token>')
def confirm_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user_id = User.verify_email_confirmation_token(token)
    if not user_id:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.login'))
    
    if user.email_confirmed:
        flash('Your email has already been confirmed.', 'info')
        return redirect(url_for('auth.login'))
    
    user.email_confirmed = True
    user.email_confirmed_at = datetime.utcnow()
    user.active = True
    db.session.commit()
    
    flash('Your email has been confirmed. You can now log in.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user_id = User.verify_reset_password_token(token)
    if not user_id:
        flash('The reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', title='Reset Password', form=form, token=token)
