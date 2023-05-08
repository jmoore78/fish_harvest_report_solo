from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db_name = "dfg_harvest_report"
    def __init__(self, data): # line up all the tables/table columns with the attributes that the class has.
        self.id = data['id'] # here we defined an attribute called id, which is equal to the id that we will pass in
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#--------class methods to interface with the database (Web APIs)--------
    @classmethod
    def save(cls,data): # method is called in the registration route to save the new user. row ID is returned and used as the user ID
        query ="INSERT INTO users ( first_name , last_name , email , password ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s );"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        return results 

    @classmethod
    def get_all(cls): # not used here but maybe useful down the road or for other developers adding functionality
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        users = [] # will be used to store the row results as a list
        for row in results:
            users.append( cls(row)) # looping though the results to add (append) them to the users results list
        print(users)
        return users

    @classmethod
    def get_by_email(cls,data): # called in the login route method as part of the validation
        query = "SELECT * FROM users WHERE email = %(email)s;" 
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if len(result) < 1: 
            return False
        return cls(result[0])

    @classmethod # used on the dashboard route to display specific user that is logged in
    def get_by_id(cls,data): # cls because its a class method, data because we need something to search by. 
        query = "SELECT * FROM users where id = %(id)s;" # specific, doesn't need a loop to get Jinja to display the name
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(result[0]) # used to parce the info from this customized query

#--------static methods for validation (they don't change the class or instances)--------

#----registeration validation----
    @staticmethod # validation method to check for duplicates AND check for pattern errors (also uses if checks). also uses booleans to generates the error message informing the user of the problem
    def validate_registration(user):
        is_valid = True # setting the boolean value to True as a default value to check against.
        if len(user['first_name']) < 2: # Basic Form Validation
            is_valid = False
            flash("First Name must be at least 2 characters","register")
        if len(user['last_name']) < 2:
            is_valid = False
            flash("Last Name must be at least 2 characters","register")
        query = "SELECT * FROM users WHERE email = %(email)s;" # checks for unique values (email in this case) in the database to prevent duplicate registration.
        results = connectToMySQL(User.db_name).query_db(query,user) # using User.db_name as a way to access the class variable. Need to get the dictionary of user info to pass user in query_db(query,user)
        print(results)
        if len(results) > 0:
            is_valid = False
            flash("Email Already Taken","register")
        elif not EMAIL_REGEX.match(user['email']): # Pattern Validation: checks for specific patterns of the chosen value requirement. Email structure in this case.
            is_valid = False
            flash("Invalid Email","register")
        if len(user['password']) < 8:
            is_valid = False
            flash("Password must be least 8 characters","register")
        if user['password'] != user['confirm_password']: # verifies password entered and confirm password match
            is_valid = False # if not matched
            flash("Passwords must match","register")
        return is_valid

