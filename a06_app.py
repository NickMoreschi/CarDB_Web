#Reference https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
#Site to load locally http://127.0.0.1:5000/

from flask import Flask, render_template, request, redirect, jsonify
from multiprocessing import Process
app = Flask(__name__)
app.url_map.strict_slashes = False
import my_db

import os
from werkzeug.utils import secure_filename

#-----Initialization and shutdown-----

@app.before_first_request
def init():
    my_db.init_db()

@app.teardown_appcontext
def close(exception):
    my_db.close_connection()


#-----ROUTING-----
#root path
@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template("create.html")
    
    else: #POST
    
        car_id = request.form['car_id']
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        type = request.form['type']
        
        my_db.create_car(car_id, make, model, year, type)
    
        return redirect('/list/')

@app.route('/list/')
def listing():
    rows = my_db.select_all()

    for row in rows:
        print(row[0], row[1], row[2], row[3], row[4])
    return render_template("list.html", cars=rows)

@app.route('/list/<car_id>', methods=['GET', 'POST'])
def list_car(car_id):
    if request.method == 'GET':
        
        result = my_db.select_one(car_id)
        return render_template('create.html', car=result)
    else:
        
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        body_type = request.form['type']
        my_db.update(car_id, make, model, year, body_type)
        return redirect("/list/" + str(car_id))

@app.route('/delete/<car_id>')
def delete(car_id):
    my_db.delete(car_id)
    return redirect('/list/')

@app.route("/reset")
def reset():
    my_db.reset()
    return redirect('/')

@app.route('/import', methods=['GET', 'POST'])
def import_data():
    if request.method == "GET":
        return render_template("import.html")
    
    else:
        
        f = request.files['myfile']
        fname = secure_filename(f.fname)
        f.save(os.path.join('uploads', fname))
        my_db.load_csv(fname)
        
        return redirect('/list')
        
@app.route('/search')
def search():
    
    if not request.args:
        return render_template("search.html")

    else:
        
        make = request.args.get('make')
        model = request.args.get('model')
        body_type = request.args.get('type')
        print(make,model,body_type)
        
        if make=='ALL' and model=='ALL' and body_type=='ALL':
            rows = my_db.select_all()
            
        else:
            rows = my_db.select_by_attr(make, model, body_type)
        
        return render_template("list.html", cars=rows)

@app.route('/getcardata')
def getcardata():
    if not request.args:
        
        makes = my_db.get_makes()
        
        data = {
            "makes":makes
        }
        
        return jsonify(data)
    
    elif 'model' not in request.args:
        
        make = request.args.get('make')
        models = my_db.get_models(make)
        
        data = {
            "models":models
        }
        
        return jsonify(data)
    
    else:
        
        make = request.args.get('make')
        model = request.args.get('model')
        body_types = my_db.get_types(make, model)
        
        data = {
            "types":body_types
        }
        
        return jsonify(data)


server = Process(target=app.run)
server.start()
server.terminate()
server.join()
    
    
    
    
    