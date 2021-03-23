import utils 


from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>光锥之内就是命运</h1>"


@app.route('/spoken')
def spoken():
    output = utils.database_read('/audio/')
    return render_template('spoken.html', output=output)









if __name__ == "__main__":
    app.run(debug=True)


   