from flask import render_template, request, redirect, url_for, flash
from .forms import LoginForm, RegisterForm, EditProfileForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required
from .import bp as auth


@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "icon":int(form.icon.data),
                "password": form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
        except:
            flash('There was an unexpected error', 'danger')
            return render_template('auth/register.html.j2',form=form)
        
        # registered successfully 
        flash('You Registered Successfully','success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html.j2',form=form)


@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        u = User.query.filter_by(email=email).first()
        print(u)
        if u is not None and u.check_hashed_password(password):
            login_user(u)
            # Give User feeedback of success
            flash('You Logged in Successfully','success')
            return redirect(url_for('main.index'))
        else:
            # Give user Invalid Password Combo error
            flash('Invalid Username password combo','danger')
            return redirect(url_for('auth.login'))
    return render_template("auth/login.html.j2", form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user is not None:
        logout_user()
        flash('You logged out','warning')
        return redirect(url_for('auth.login'))


@auth.route('/edit_profile',methods=['GET','POST'])
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data={
            "first_name": form.first_name.data.title(),
            "last_name": form.last_name.data.title(),
            "email": form.email.data.lower(),
            "icon": int(form.icon.data) if int(form.icon.data) !=9000 else current_user.icon ,
            "password": form.password.data
        }
        user=User.query.filter_by(email=form.email.data.lower()).first()
        if user and current_user.email != user.email:
            flash('Email already in use','danger')
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            flash('Profile Updated','success')
            return redirect(url_for('main.index'))
        except:
            flash('There was an unexpected error', 'danger')
            return redirect('auth.edit_profile')
    # registered successfully 
    return render_template('auth/register.html.j2',form=form)