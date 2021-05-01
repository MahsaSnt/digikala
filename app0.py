from flask import request, redirect,Flask,render_template,url_for,redirect,Response
from flask_bootstrap import Bootstrap
from flask import send_file
from async_digikala import output

app=Flask(__name__)
Bootstrap(app)

@app.route('/',methods=['GET','POST'])
def c():
    if request.method=="POST":
            total=int(request.form['total'])
            subject=request.form['subject']
            output(total,subject)
    return render_template('form.html') 
  
if __name__ == '__main__':
    app.run(debug=True)
    
#print(output(4,'گوشی'))  
    