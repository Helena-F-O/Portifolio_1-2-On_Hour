from flask import Flask
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../pages'),
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets'),
    static_url_path='/assets'
)

from .routes import *

if __name__ == "__main__":
    app.run(debug=True)
