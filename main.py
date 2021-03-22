from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>光锥之内就是命运</h1>"


@app.route('/spoken')
def spoken():
    return """<h1 style='color:blue'>Spoken</h1></br><a href="https://play.google.com/store/apps/details?id=com.depplenny.spoken">Android</a>"""

if __name__ == "__main__":
    app.run()


   