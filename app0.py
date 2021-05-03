from flask import Flask, request, jsonify
from flask_cors import CORS
#from my own code
from async_digikala import output

app=Flask(__name__)
CORS(app)

@app.route('/api',methods=['POST'])
def index():
    data = request.get_json()
    subject = data["subject"]
    num_pages = data["num_pages"]
    products = output(num_pages,subject)
    return jsonify(products= f"{products}")
    
        
if __name__ == '__main__':
    app.run(debug=True)
    