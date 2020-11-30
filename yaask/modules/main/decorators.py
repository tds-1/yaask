from functools import wraps

from flask import flash, redirect, url_for
from flask.ext.login import current_user


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.email_verified is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('users.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function