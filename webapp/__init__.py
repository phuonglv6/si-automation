from flask import Flask

# CREATE APP OBJECT
## app the variable...
app = Flask(__name__)
# IMPORT views MODULE
## is not app the package...
from webapp import views

# The views are the handlers that respond
# to requests from web browsers or other
# clients.  In Flask, handlers are written
# as Python functions. :-) Woohoo!

# The import statement is at the end to
# avoid circular references.

# The views module needs the app variable
# defined in this script.