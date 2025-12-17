from flask import Flask, render_template
from database import Database 
from routes import setup_routes, setup_metrics

app = Flask(__name__)
db = Database()

setup_metrics(app)
setup_routes(app, db)

if __name__ == '__main__':
    db.setup()
    app.run(debug=True, host='0.0.0.0', port=8000)
