import utils 


from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>光锥之内就是命运</h1>"


@app.route('/spoken', defaults={"page": 1})
@app.route('/spoken/<int:page>')
def spoken(page):
    # Making 0 to 1
    curr_page = page if page != 0 else 1 

    PAGE_SIZE = 6
    # TODO: should only get part of the /audio/
    output = utils.database_read('/audio/')
    
    if curr_page*PAGE_SIZE <= len(output):
        output_page = []  
        for i in range((curr_page-1)*PAGE_SIZE, curr_page*PAGE_SIZE, 1):
            output_page.append(output[i])
    else:
        output_page = []  
        for i in range(len(output)-PAGE_SIZE, len(output), 1):
            output_page.append(output[i])


    return render_template('spoken.html', output=output_page, curr_page=curr_page)









if __name__ == "__main__":
    app.run(debug=True)


   