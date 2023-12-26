import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    stats = db.execute('''
    SELECT * FROM
      (SELECT COUNT(*) linhaID FROM Linhas)
    JOIN
      (SELECT COUNT(*) viagemID FROM Viagens)
    JOIN
      (SELECT COUNT(*) zonaIdOrigem FROM Zonas)
    JOIN 
      (SELECT COUNT(*) idParagem FROM Paragens)
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html',stats=stats)

# Routes
@APP.route('/routes/')
def list_routes():
    routes = db.execute(
      '''
      SELECT nome as Name, cor as Color
      FROM Linhas
      ORDER BY Name
      ''').fetchall()
    if not routes:
        abort(404)  # or handle it in another way, e.g., render an error template

    return render_template('routes-list.html', routes=routes)

@APP.route('/routes/A')
def route_A():
    routes = db.execute(
      '''
      SELECT nome as Name, cor as Color
      FROM Linhas
      WHERE nome = 'A'
      ''').fetchall()
    if not routes:
        abort(404)  # or handle it in another way, e.g., render an error template

    return render_template('routes-list.html', routes=routes)

@APP.route('/routes/B')
def route_B():
    routes = db.execute(
      '''
      SELECT nome as Name, cor as Color
      FROM Linhas
      WHERE nome = 'B'

      ''').fetchall()
    if not routes:
        abort(404)  # or handle it in another way, e.g., render an error template

    return render_template('routes-list.html', routes=routes)   

@APP.route('/routes/Bx')
def route_Bx():
    routes = db.execute(
      '''
      SELECT nome as Name, cor as Color
      FROM Linhas
      WHERE nome = 'Bx'

      ''').fetchall()
    if not routes:
        abort(404)  # or handle it in another way, e.g., render an error template

    return render_template('routes-list.html', routes=routes)

@APP.route('/routes/C')
def route_C():
    routes = db.execute(
      '''
      SELECT nome as Name, cor as Color
      FROM Linhas
      WHERE nome = 'C'

      ''').fetchall()
    if not routes:
        abort(404)  # or handle it in another way, e.g., render an error template

    return render_template('routes-list.html', routes=routes)

@APP.route('/routes/D')
def route_D():
    routes = db.execute(
      '''
      SELECT nome as Name, cor as Color
      FROM Linhas
      WHERE nome = 'D'
      ''').fetchall()
    if not routes:
        abort(404)  # or handle it in another way, e.g., render an error template

    return render_template('routes-list.html', routes=routes)

@APP.route('/routes/E')
def route_E():
    routes = db.execute(
      '''
      SELECT nome as Name, cor as Color
      FROM Linhas
      WHERE nome = 'E'
      ''').fetchall()
    if not routes:
        abort(404)  # or handle it in another way, e.g., render an error template

    return render_template('routes-list.html', routes=routes)

@APP.route('/routes/F')
def route_F():
    routes = db.execute(
      '''
      SELECT nome as Name, cor as Color
      FROM Linhas
      WHERE nome = 'F'
      ''').fetchall()
    if not routes:
        abort(404)  # or handle it in another way, e.g., render an error template

    return render_template('routes-list.html', routes=routes)

@APP.route('/stops/')
def paragens():
    stops = db.execute(
        '''
        Select nomeDaParagem as Name
        From Paragens
        Order by Name
        ''').fetchall()
    if not stops:
        abort(404)  # or handle it in another way, e.g., render an error template
    return render_template('stops-list.html', stops=stops)
