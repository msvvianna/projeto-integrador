from flask import session,flash

from ..models.user import User

def auth(email, password):
    data = User.query.filter_by(email=email).first()
    if data and data.verify_password(password):
        session['name'] = data.name
        session['email']= email
        session['id_user'] = data.id_user
        session['status'] = data.status.value
        session.pop('_flashes', None)
        if data.status.value == 'adm':
            return 1
        return 2
    return False

def verify_session_adm():
    if session.get('id_user') is not None:
        if User.query.filter_by(id_user=session['id_user']).first().status.value != 'adm':
            session.pop('_flashes', None)
            flash('O usuario não tem permissão para acessar essa area', 'error')
            return False
        return True
    session.pop('_flashes', None)
    flash('Precisa estar logado para acessar o sistema', 'error')
    return False

def verify_session():
    if session.get('id_user') is not None:
        return True
    session.pop('_flashes', None)
    flash('Precisa estar logado para acessar o sistema', 'error')
    return False