from flask import Flask, render_template
from database import Database 

app = Flask(__name__)


db = Database()

@app.route('/')
def home():
    try:
        data = db.add_visit()
        if data == None:
            return render_template('index.html',
                                 error="Database connection failed",
                                 total_visits=0,
                                 last_visit="N/A")

        return render_template("index.html", 
                               total_visits = data["total"],
                               last_visit = data["last_time"],
                               error = None)
        
    except Exception as e:
        return render_template('index.html',
                             error=str(e),
                             total_visits=0,
                             last_visit="N/A")


if __name__ == '__main__':
    db.setup()
    app.run(debug=True, host='0.0.0.0', port=8000)
