from flask import Flask, request, jsonify
from flask_cors import CORS

#from my own code
from digikala import all_digikala, incredible_digikala, special_digikala
from digistyle import all_digistyle, special_digistyle
from timcheh import all_timcheh, special_timcheh, incredible_timcheh
from emalls import all_emalls, special_emalls ,shoplist_emalls
from banimode import all_banimode, special_banimode, incredible_banimode
from sheypoor import all_sheypoor


app=Flask(__name__)
CORS(app)

@app.route('/api/digikala/all',methods=['POST'])
def digikala1():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = all_digikala(num_pages,subject)
    return jsonify(products= f"{products}")

@app.route('/api/digikala/incredible')
def digikala2():
    products = incredible_digikala()
    return jsonify(products= f"{products}")

@app.route('/api/digikala/special',methods=['POST'])
def digikala3():
    data = request.get_json()
    num_pages = data["num_pages"]
    products = special_digikala(num_pages)
    return jsonify(products= f"{products}")

@app.route('/api/digistyle/all',methods=['POST'])
def digistyle1():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = all_digistyle(num_pages,subject)
    return jsonify(products= f"{products}")  

@app.route('/api/digistyle/special',methods=['POST'])
def digistyle2():
    data = request.get_json()
    num_pages = data["num_pages"]
    products = special_digistyle(num_pages)
    return jsonify(products= f"{products}")       

@app.route('/api/timcheh/all',methods=['POST'])
def timche1():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = all_timcheh(num_pages,subject)
    return jsonify(products= f"{products}")   

@app.route('/api/timcheh/special',methods=['POST'])
def timche2():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = special_timcheh(num_pages,subject)
    return jsonify(products= f"{products}")   

@app.route('/api/timcheh/incredible')
def timche3():
    products = incredible_timcheh()
    return jsonify(products= f"{products}")   

@app.route('/api/emalls/all',methods=['POST'])
def emalls1():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = all_emalls(num_pages,subject)
    return jsonify(products= f"{products}") 

@app.route('/api/emalls/special',methods=['POST'])
def emalls2():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = special_emalls(num_pages,subject)
    return jsonify(products= f"{products}")     

@app.route('/api/emalls/shoplist',methods=['POST'])
def emalls3():
    data = request.get_json()
    shoplist = data["shoplist"]
    products = shoplist_emalls(shoplist)
    return jsonify(products= f"{products}")         


@app.route('/api/banimode/all',methods=['POST'])
def banimode1():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = all_banimode(num_pages,subject)
    return jsonify(products= f"{products}") 


@app.route('/api/banimode/special',methods=['POST'])
def banimode2():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = special_banimode(num_pages,subject)
    return jsonify(products= f"{products}") 

@app.route('/api/banimode/incredible')
def banimode3():
    products = incredible_banimode()
    return jsonify(products= f"{products}") 

@app.route('/api/sheypoor/all',methods=['POST'])
def sheypoor1():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    county = data["county"]
    products = all_sheypoor(num_pages, subject, county)
    return jsonify(products= f"{products}") 

  
if __name__ == '__main__':
    app.run(debug=True)
    