from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime
from flask_app.models import user



class Report:
    db_name = "dfg_harvest_report"
    def __init__(self, data): # line up all the tables/table columns with the attributes that the class has.
        self.id = data['id']
        self.fish_type = data['fish_type']
        self.weight_ounces = data['weight_ounces']
        self.length_inches = data['length_inches']
        self.date_caught = data['date_caught']
        self.location = data['location']
        self.bait_used = data['bait_used']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id'] # using the foreign key in the reports table. this will be used to check for user access to edit/delete the reports only the specified user created.
        self.user = None

#--------class methods to interface with the database--------
    @classmethod
    def save(cls,data): # method is called in the new report route to save the new report
        query ="INSERT INTO reports ( fish_type , weight_ounces , length_inches , date_caught , location , bait_used , user_id ) VALUES ( %(fish_type)s , %(weight_ounces)s , %(length_inches)s , %(date_caught)s , %(location)s , %(bait_used)s , %(user_id)s );"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        return results 

    @classmethod
    def get_all(cls): # not used. renders all reports and stored as a dictionary for Jinja to loop through 
        query = "SELECT * FROM reports;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_reports = [] # be sure to do a Jinja loop in html for when this is called
        for row in results:
            all_reports.append( cls(row))
        return all_reports

################################################################################################################################
    @classmethod
    def get_all_with_user(cls): # used in the show route. renders all reports and stored as a dictionary for Jinja to loop through 
        query = "SELECT * from reports JOIN users on reports.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(f"RESULTS: {results}") 
        reports = [] # be sure to do a Jinja loop in html for when this is called
        for report in results:
            this_report = cls(report) # instantiate (reference) reports object (need a place to store the object info that is returned in the query)
            this_user = user.User.get_by_id({"id": report["users.id"]}) # instantiate (reference) user object (need a place to store the object info that is returned in the query)
            this_report.user = this_user # combining this_user to report with dot notation and variable value assignment
            reports.append(this_report) #appending (adding) the combined info into the reports list to be looped with Jinja in HTML.
        return reports

#         elif(this_report.date_caught > datetime.date(datetime.now())):
#            flash("check upcoming schedule", "show")

    @classmethod
    def get_one_with_user(cls,data): # not used
        query = "SELECT * from reports JOIN users ON reports.user_id = users.id WHERE reports.id = %(id)s;" # specific query with a single result, no need for a loop.
        result = connectToMySQL(cls.db_name).query_db(query,data)
        print(f"RESULTS: {result}")
        return result[0] # the result became a reports-driven query, so the "reported by" on the show page is "report.first_name".

####################################################################################################################################

    @classmethod
    def get_report_by_id(cls,data): # cls because its a class method, data because we need something to search by due to the conditional query. 
        query = "SELECT * FROM reports WHERE id = %(id)s;" # specific, doesn't need a loop to get Jinja to display the name
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(result[0]) # used to parce the info from this customized query

    @classmethod
    def update(cls,data):
        query = "UPDATE reports SET fish_type=%(fish_type)s, weight_ounces=%(weight_ounces)s, length_inches=%(length_inches)s, date_caught=%(date_caught)s, location=%(location)s, bait_used=%(bait_used)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM reports WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)



#--------static methods--------
    @staticmethod # validation method to check for duplicates AND check for pattern errors (also uses if checks). also uses booleans to generates the error message informing the user of the problem
    def validate_report(report):
        is_valid = True
        if len(report['fish_type']) < 3: # If checks to see if it is empty
            is_valid = False
            flash("Fish Type must be at least 3 characters","report")
        if len(report['weight_ounces']) < 1:
            is_valid = False
            flash("Weight in Ounces must be at least 1 character","report")
        if len(report['length_inches']) < 1:
            is_valid = False
            flash("Length in Inches must be at least 1 character","report")
        if report['date_caught'] == "": # If checks to see if it is empty
            is_valid = False
            flash("Please enter a date","report")
        if report['location'] == "":
            is_valid = False
            flash("Location cannot be empty","report")
        if report['bait_used'] == "":
            is_valid = False
            flash("Bait Used cannot be empty","report")
        return is_valid
