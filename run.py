from app import create_app, db
from app.models import *
from flask import render_template, request, redirect, url_for

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
