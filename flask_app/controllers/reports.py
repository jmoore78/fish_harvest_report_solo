from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.report import Report
from flask_app.models.user import User

#--------Authorization--------

#----render form route 
@app.route('/new/report')
def new_report():
    if 'user_id' not in session: # needs to be logged in to access this page. this is my if check to verify below allowing access. 
        return redirect('/logout')
    data = {
        "id":session['user_id'] # sent to html to display the user name
    }
    return render_template('new_report.html', user=User.get_by_id(data)) # written in user.py to pull the id from the users table we want to display.

#----post route "get form info and do something with it" 
@app.route('/create/report',methods=['POST']) # now the form processing can begin since the route was created
def create_report():
    if 'user_id' not in session: # authorization - needs to be logged in to access this page. this is my if check to verify below allowing access. 
        return redirect('/logout')
    if not Report.validate_report(request.form):
        return redirect('/new/report') # redirecting back to enter the recipe info in correctly
    data = {
        "fish_type": request.form['fish_type'],
        "weight_ounces": int(request.form['weight_ounces']),
        "length_inches": int(request.form['length_inches']),
        "date_caught": request.form["date_caught"],
        "location": request.form["location"],
        "bait_used": request.form["bait_used"],
        "user_id": session["user_id"] 
    }
    Report.save(data)
    return redirect ('/dashboard')

#----render form route
@app.route('/edit/report/<int:id>')
def edit_report(id):
    if 'user_id' not in session: # authorization - needs to be logged in to access this page. this is my if check to verify below allowing access. 
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("edit_report.html", edit=Report.get_report_by_id(data), user=User.get_by_id(user_data)) # edit will be used on the edit_report.html page

#----now do something with the edit info
@app.route('/update/report', methods=['POST'])
def update_report():
    if 'user_id' not in session: # authorization - needs to be logged in to access this page. this is my if check to verify below allowing access. 
        return redirect('/logout')
    if not Report.validate_report(request.form):
        return redirect('/new/report') # redirecting back to enter the recipe info in correctly
    data = {
        "fish_type": request.form['fish_type'],
        "weight_ounces": int(request.form['weight_ounces']),
        "length_inches": int(request.form['length_inches']),
        "date_caught": request.form["date_caught"], 
        "location": request.form["location"],
        "bait_used": request.form["bait_used"],
        "id": request.form["id"]
    }
    Report.update(data) # class method written first in report model as a specific query of UPDATE
    return redirect('/dashboard')


@app.route('/show/report/<int:id>') 
def show_report(id):
    if 'user_id' not in session: # needs to be logged in to access this page. this is my if check to verify below allowing access. 
        return redirect('/logout')
    user_data = {
        "id": session['user_id']
    }
    return render_template("show_reports.html", user=User.get_by_id(user_data), reports=Report.get_all_with_user()) # edit will be used on the edit_report.html page


@app.route('/destroy/report/<int:id>')
def destroy_report(id):
    if 'user_id' not in session: # authorization - needs to be logged in to access this page. this is my if check to verify below allowing access. 
        return redirect('/logout')
    data = {
        "id": id
    }
    Report.destroy(data)
    return redirect('/dashboard')
