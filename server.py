from flask_app import app
from flask_app.controllers import users, reports
# By enabling debug mode, the server will automatically reload if code changes, and will show an interactive debugger in the browser if an error occurs during a request.
if __name__=="__main__":
    app.run(debug=True) # The debugger allows executing arbitrary Python code from the browser. 
# It is protected by a pin, but still represents a major security risk. Do not run the development server or debugger in a production environment.