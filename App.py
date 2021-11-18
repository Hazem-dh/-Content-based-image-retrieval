import os
from flask import Flask,request, render_template
from flask_pymongo import PyMongo
from flask import send_from_directory
from utilis import PretrainedModel

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/cbir_database"
dir = "static/uploads"
if not os.path.isdir(dir):
    os.mkdir(dir)
app.config['UPLOAD_FOLDER'] = dir
db = PyMongo(app).db
model = PretrainedModel(database=db)


@app.route('/', methods=['GET', 'POST'])
def testing():
    if request.method == 'POST':
        file = request.files['query_img']
        nb_pic = request.form['nbrpic']
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(save_path)
        files = model.get_images(save_path,int(nb_pic))
        return render_template("Webapp.html", uploaded_image=file.filename, answers=files)
    else:
        return render_template('Webapp.html')


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)

