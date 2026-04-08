from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["consultancy_db"]
collection = db["clients"]

# 🔹 HOME
# 🔹 HOME (UPDATED WITH SEARCH)
@app.route('/')
def index():
    search = request.args.get('search')

    if search:
        clients = list(collection.find({
            "$or": [
                {"name": {"$regex": search, "$options": "i"}},
                {"phone": {"$regex": search, "$options": "i"}},
                {"service": {"$regex": search, "$options": "i"}}
            ]
        }))
    else:
        clients = list(collection.find())

    return render_template('index.html', clients=clients)

# 🔹 ADD
@app.route('/add', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "phone": request.form['phone'],
            "service": request.form['service'],
            "requirement": request.form['requirement']
        }
        collection.insert_one(data)
        return redirect('/')
    
    return render_template('form.html', client=None)

# 🔹 EDIT
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_client(id):
    client_data = collection.find_one({"_id": ObjectId(id)})

    if request.method == 'POST':
        updated_data = {
            "name": request.form['name'],
            "phone": request.form['phone'],
            "service": request.form['service'],
            "requirement": request.form['requirement']
        }
        collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        return redirect('/')

    return render_template('form.html', client=client_data)

# 🔹 DELETE
@app.route('/delete/<id>')
def delete_client(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect('/')

# 🔹 RUN
if __name__ == '__main__':
    app.run(debug=True)