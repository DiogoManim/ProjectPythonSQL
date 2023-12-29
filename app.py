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



@APP.route('/routes/<nome>')
def route(nome):
    count= '''SELECT
    COUNT (*) contador 
    FROM
        Paragens
    JOIN
        Horarios ON idParagem = paragemID
    WHERE
        Replace(linhaID, "Bexp", "Bx") = ?'''
    
    query = '''SELECT nome as Name , cor as Color
                FROM Linhas
                Where nome = ?
                '''
    paragens = '''
    SELECT
    nomeDaParagem as Name
    FROM
        Paragens
    JOIN
        Horarios ON idParagem = paragemID
    WHERE
        Replace(linhaID, "Bexp", "Bx") = ?
    
    '''
    routes = db.execute(query,(nome,)).fetchall()
    stations = db.execute(paragens,(nome,)).fetchall()
    contador = db.execute(count, (nome,)).fetchall()
    if not routes:
        abort(404)  # or handle it in another way, e.g., render an error template

    return render_template('routes.html', routes=routes, stations= stations, contador= contador)

 


@APP.route('/routes-search/<color>/')
def color_search(color):
    # Use a parameterized query to avoid SQL injection
    query = '''
        SELECT nome as Name, cor as Color
        FROM Linhas
        WHERE cor = ?
    '''

    paragens = '''
        select nomeDaParagem as Name
        from Paragens 
        join Horarios on idParagem = paragemID
        where Horarios.linhaID = 
        (Select linhaID from Linhas where cor = ?);
                
    '''
    count ='''
        select Count(*) contador 
        from Paragens 
        join Horarios on idParagem = paragemID
        where Horarios.linhaID = 
        (Select linhaID from Linhas where cor = ?);
        '''
    
    routes = db.execute(query, (color,)).fetchall()
    stations = db.execute(paragens,(color,)).fetchall()
    contador = db.execute(count, (color,)).fetchall()

    if not routes:
        abort(404)  # or handle it in another way, e.g., render an error template

    return render_template('routes-search.html', color=color, routes=routes, stations= stations, contador=contador)


#  Pagina das paragens
@APP.route('/stops/')
def list_stops():
    stops = db.execute(
    '''
    SELECT idParagem as ID, zonaIdOrigem as Zone, nomeDaParagem as Name
    FROM Paragens
    ORDER BY ID
    ''').fetchall()
    return render_template('stops-list.html',stops=stops)

@APP.route('/stops/<ID>/')
def stop(ID):
    station = '''SELECT
    nomeDaParagem AS Name,
    zonaIdOrigem AS Zone,
    idParagem AS ID
    FROM Paragens
    WHERE ID = ?'''
    
    query = '''
    SELECT
    REPLACE(linhaID, 'Bexp', 'Bx') AS Route
FROM
    Horarios
JOIN
    Paragens ON idParagem = paragemID
WHERE
    idParagem = ?
ORDER BY Route;

    '''
    paragens = db.execute(query, (ID,)).fetchall()
    stations = db.execute(station, (ID,)).fetchall()
    if not paragens:
        abort(404)  # or handle it in another way, e.g., render an error template

    return render_template('stops.html', ID=ID, paragens=paragens, stations = stations)


@APP.route('/stops_by_name/<Name>/')
def stop_search_By_Name(Name):
    station = '''SELECT
    nomeDaParagem AS Name,
    zonaIdOrigem AS Zone,
    idParagem AS ID
    FROM Paragens
    WHERE Name = ?'''
    
    query = '''
    SELECT
    REPLACE(linhaID, 'Bexp', 'Bx') AS Route
FROM
    Horarios
JOIN
    Paragens ON idParagem = paragemID
WHERE
    nomeDaParagem = ?
ORDER BY Route;

    '''
    paragens = db.execute(query, (Name,)).fetchall()
    stations = db.execute(station, (Name,)).fetchall()
    if not paragens:
        abort(404)  # or handle it in another way, e.g., render an error template

    return render_template('stops.html', Name=Name, paragens=paragens, stations = stations)

# Pagina dos tickets
@APP.route('/tickets/')
def list_ticket_prices():
    tickets = db.execute(
    '''
    SELECT tituloID as Ticket, preco as Price
    FROM Titulos
    GROUP BY Ticket, Price
    HAVING COUNT(*) > 1
    ''').fetchall()
    if not tickets:
        abort(404)
    return render_template('tickets-price-list.html', tickets=tickets)

@APP.route('/tickets/<zone>/')
def search_by_Zone(zone):
    preco = '''
               SELECT DISTINCT preco as Price , tituloID as Ticket
               FROM Titulos
               WHERE tituloID = ?
            '''
    query =  '''
            Select  tituloID as Ticket,  preco as Price, zonaIdOrigem , zonaIdDestino
            FROM Titulos
            Where Ticket = ?
        '''
    zonas = db.execute(query, (zone,)).fetchall()
    precos = db.execute(preco, (zone,)).fetchall()
    if not (zonas and precos) :
        abort(404)
    return render_template('tickets-search.html', precos=precos, zonas=zonas)


@APP.route('/schedule/')
def schedule():
    query = '''
    select  distinct Replace(linhaID, "Bexp", "Bx") as Route 
    from Viagens
    order by Route
    '''
    viagens = db.execute(query).fetchall()

    if not (viagens) :
        abort(404)
    return render_template('schedule.html', viagens=viagens)

@APP.route('/schedule-search/<Route>')
def schedule_search(Route):
    route_query= '''SELECT DISTINCT REPLACE(linhaID, 'Bexp', 'Bx') AS route
                    FROM Viagens
                    WHERE REPLACE(linhaID, 'Bexp', 'Bx') = ?
                '''
    query = '''
            select horaDePartida as Departures
            from Viagens
            where replace(linhaID, "Bexp", "Bx") = ?
            
            '''
    routes= db.execute(route_query, (Route,)).fetchall()
    horas = db.execute(query, (Route,)).fetchall()
    if not (horas) :
        abort(404)
    return render_template('schedule-search.html', routes=routes, horas=horas)




