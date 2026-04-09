from flask import render_template,json,jsonify,Flask

app=Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="testing")

if __name__=="__main__":
    app.run(debug=True)