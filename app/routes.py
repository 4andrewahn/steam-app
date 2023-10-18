""" Specifies routing for the application"""
from flask import render_template, request, jsonify, flash
from app import app
from app import database as db_helper

created_procedure1 = False

@app.route("/delete/<int:game_id>", methods=['POST'])
def delete(game_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_game_by_id(game_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<int:game_id>", methods=['POST'])
def update(game_id):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        if "name" in data:
            db_helper.update_title_entry(game_id, data["name"])
            result = {'success': True, 'response': 'Status Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    if db_helper.insert_new_game(data['name']) == -1:
        flash('Name already exists!', 'error')
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/advanced")
def advancedQuery1():
    items = db_helper.run_advanced_query()
    return render_template("advance1.html", items=items)

@app.route("/advanced2")
def advancedQuery2():
    items = db_helper.run_advanced_query_2()
    return render_template("advance2.html", items=items)

@app.route("/procedure1")
def procedure1():
    items = db_helper.run_stored_procedure1()
    return render_template("procedure1.html", items=items)

@app.route("/procedure2")
def procedure2():
    items = db_helper.run_stored_procedure2()
    return render_template("procedure2.html", items=items)

@app.route("/search/<searchword>", methods=['POST', 'GET'])
def search(searchword="c"):
    print(searchword)
    items = db_helper.fetch_games(searchword)
    # print(items)
    return render_template("search.html", items=items)

@app.route("/")
def homepage():
    """ returns rendered homepage """
    if not db_helper.check_for_trigger():
        db_helper.create_trigger()

    if not db_helper.check_for_procedure(1):
        db_helper.create_stored_procedure1()

    if not db_helper.check_for_procedure(2):
        db_helper.create_stored_procedure2()

    items = db_helper.fetch_games()
    return render_template("index.html", items=items)
