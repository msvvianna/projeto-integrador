from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from ..services.auth import verify_session_adm, verify_session
from flaskr import db
from ..models.user import User

main = Blueprint('main', __name__)

value_one = (
    {'chart': {'type': 'donut', 'height': 400}, 'title': {'text': 'Eqp. disponiveis por modelo', 'align': 'center'},
     'series': [5, 10, 186, 27], 'colors': ['#1C7FAD', '#458E66', '#EF8F2F', '#FC6D6D'],
     'labels': ['HAND HELD', 'ZEBRA TC21', 'HONEYWELL CT60', 'HONEYWELL EDA61K'],
     'plotOptions': {'pie': {'customScale': 0.8}}})

value_two = ({
    'series': [
        {
            'name': 'Equipamentos',
            'data': [17, 31, 108, 49, 34, 91, 123]
        }
    ],
    'chart': {
        'type': 'line',
        'zoom': {
            'enabled': 0
        },
        'height': 400
    },
    'colors': ['#1C7FAD'],
    'dataLabels': {
        'enabled': 1
    },
    'stroke': {
        'curve': 'straight'
    },
    'title': {
        'text': 'Eqp. retirados em função do tempo (7 dias)',
        'align': 'center'
    },
    'xaxis': {
        'categories': [
            '20/9/2024', '21/9/2024', '22/9/2024', '23/9/2024', '24/9/2024',
            '25/9/2024', '26/9/2024'
        ]
    }
})

value_three = ({
    'series': [
        {
            'name': 'Equipamentos',
            'data': [3, 4, 7, 4, 2, 1, 3]
        }
    ],
    'chart': {
        'type': 'line',
        'zoom': {
            'enabled': 0
        },
        'height': 400
    },
    'colors': ['#FC6D6D'],
    'dataLabels': {
        'enabled': 1
    },
    'stroke': {
        'curve': 'straight'
    },
    'title': {
        'text': 'Eqp. em manutenção em função do tempo (7 dias)',
        'align': 'center'
    },
    'xaxis': {
        'categories': [
            '20/9/2024', '21/9/2024', '22/9/2024', '23/9/2024', '24/9/2024',
            '25/9/2024', '26/9/2024'
        ]
    }
})

value_four = ({
    'series': [{
        'name': 'Equipamentos',
        'data': [1, 3, 16, 8]
    }],
    'chart': {
        'type': 'bar',
        'height': 400
    },
    'colors': ['#1C7FAD', '#458E66', '#EF8F2F', '#FC6D6D'],
    'plotOptions': {
        'bar': {
            'columnWidth': '55%',
            'distributed': 'true',
        }
    },
    'dataLabels': {
        'enabled': 1
    },
    'legend': {
        'show': 0
    },
    'title': {
        'text': 'Eqp. em manutenção em função da marca',
        'align': 'center'
    },
    'xaxis': {
        'categories': [['HAND', 'HELD'], ['ZEBRA', 'TC21'], ['HONEYWELL', 'CT60'], ['HONEYWELL', 'EDA61K']],
    },
})

@main.route('/create_user')
def create_user():
    new_user = User(name="João", id_user="123456777", email="joaovitor25340@gmail.com", status='adm')
    new_user.set_password('123')
    db.session.add(new_user)
    db.session.commit()
    return "Usuário criado com sucesso!"

@main.route('/')
def index():
    flashes = session.pop('_flashes', [])
    session.clear()
    session['_flashes'] = flashes
    return render_template('index.html')

@main.route('/login',methods=['POST'])
def login():
    from ..services.auth import auth
    auth = auth(request.form['email'], request.form['senha'])
    if auth == 1:
        return redirect('/dashboardAdm')
    elif auth == 2:
        return redirect('/dashboard')
    session.pop('_flashes', None)
    flash('Email ou senha incorreto', 'error')
    return redirect('/')

@main.route('/dashboardAdm')
def adm_dashboard():
    if not verify_session_adm():
        return redirect('/')
    value_five = ({
        'series': [
            {
                'name': 'Equipamentos Retirados',
                'data': [17, 31, 108, 49, 34, 91, 123]
            },{
                'name': 'Equipamentos em Manutenção',
                'data': [3, 4, 7, 4, 2, 1, 3]
            },{
                'name': 'Equipamentos Disponíveis',
                'data': [5, 9, 7, 8, 13, 50, 17]
            }
        ],
        'chart': {
            'type': 'line',
            'zoom': {
                'enabled': 0
            },
            'height': 400
        },
        'colors': ['#1C7FAD', '#FC6D6D', '#458E66'],
        'dataLabels': {
            'enabled': 1
        },
        'stroke': {
            'curve': 'straight'
        },
        'title': {
            'text': 'Eqp. * em função do tempo (7 dias)',
            'align': 'center'
        },
        'xaxis': {
            'categories': [
                '20/9/2024', '21/9/2024', '22/9/2024', '23/9/2024', '24/9/2024',
                '25/9/2024', '26/9/2024'
            ]
        }
    })
    return render_template('pages/adm_dashboard.html', graph=[value_one, value_two, value_three, value_four, value_five])


@main.route('/equipamentosAdm')
def adm_equipamentos():
    if not verify_session_adm():
        return redirect('/')
    return render_template('pages/adm_equipamentos.html')


@main.route('/histRetirada')
def adm_hist_retirada():
    if not verify_session_adm():
        return redirect('/')
    return render_template('pages/adm_hist_retirada.html', graph=[value_one, value_two])

@main.route('/eqpManutencao')
def adm_eqp_manutencao():
    if not verify_session_adm():
        return redirect('/')
    return render_template('pages/adm_eqp_manutencao.html', graph=[value_three, value_four])

@main.route('/admUsuarios')
def adm_usuarios():
    if not verify_session_adm():
        return redirect('/')
    return render_template('pages/adm_usuarios.html')

@main.route('/dashboard')
def dashboard():
    if not verify_session():
        return redirect('/')
    return render_template('pages/user_dashboard.html', graph=[value_one])