import sqlite3, csv
from flask import g

DATABASE = 'database.db'

#-----Database setup and shutdown-----

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def init_db():
    print("initializing database")

    query = """CREATE TABLE IF NOT EXISTS cars
                            (id integer UNIQUE, make text, model text, 
                            year integer, type text)"""

    query_db(query)


def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
#-----CRUD Functions-----
        
def create_car(car_id, make, model, year, body_type):
    query = '''INSERT INTO cars (id, make, model, year, type)
            VALUES(?, ?, ?, ?, ?);'''
            
    params = (car_id, make, model, year, body_type)
    
    query_db(query, params)
    
def select_all():
    query = "SELECT * FROM cars"
    rows = query_db(query)
    return rows
    
def select_one(car_id):
    query = "SELECT * FROM cars WHERE id=?"
    
    params = (car_id,)
    
    results = query_db(query, params)
    
    return results[0]

def select_by_attr(make, model='ALL', body_type='ALL'):
    query = "SELECT * FROM cars WHERE make=?"
    params = [make]
    
    if model != 'ALL':
        query += " AND model=?"
        params += [model]
        
    results = query_db(query, params)
    
    return results

def update(car_id, make, model, year, body_type):
    query = '''UPDATE cars SET 
        make=?,
        model=?,
        year=?,
        type=?
        WHERE id=?
        '''
    params = (make, model, year, body_type, car_id)
    query_db(query, params)
    pass
    
def delete(car_id):
    query = "DELETE FROM cars WHERE id=?"
    params = (car_id,)
    query_db(query, params)
    
def reset():
    query = "DROP TABLE IF EXISTS cars"
    query_db(query)
    init_db()

def get_makes():
    query = "SELECT DISTINCT make FROM cars"
    res = query_db(query)
    makes = ['ALL']
    makes += [row[0] for row in res]
    return makes


def get_models(make):
    query = "SELECT DISTINCT model FROM cars WHERE make=?"
    res = query_db(query, (make,))
    models = ['ALL']
    models += [row[0] for row in res]
    return models


def get_years():
    query = "SELECT DISTINCT years FROM cars"
    res = query_db(query)
    return res


def get_types(make, model):
    query = """SELECT DISTINCT type FROM cars WHERE
        make=? AND model=?"""
    res = query_db(query,(make,model))
    types = ['ALL']
    types += [row[0] for row in res]

    return types

def load_csv(fn):
    with open(fn) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        car_count = 0
        keys = []

        for row in csv_reader:
            if line_count == 0:
                
                for i in range(len(row)):
                    keys.append(row[i].replace(' ', '_'))
                    
                line_count += 1
        
            else:
        
                car_id = row[0]
                
                if car_id.isnumeric():
                    
                    car = {}
                    
                    if (len(row) < len(keys)):
                        continue
                    
                    for i in range(len(row)):
                        try:
                            car[keys[i]] = row[i]
                        except (IndexError):
                            #print("hit the except at line: ", line_count)
                            pass
                        
                    create_car(
                        car_id,
                        car['Make'],
                        car['Model'],
                        car['Year'],
                        car['Body_type'],
                        )
            
                    car_count += 1
            
                line_count += 1
                
        print("loaded", car_count, "cars from", fn)
    
    
    
    