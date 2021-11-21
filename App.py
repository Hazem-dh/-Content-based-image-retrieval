import os
from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask import send_from_directory
from utilis import PretrainedModel
from forms import MyForm
from werkzeug.utils import secure_filename
import uuid


app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.config["MONGO_URI"] = "mongodb://localhost:27017/cbir_database"
dir = "static/uploads"
if not os.path.isdir(dir):
    os.mkdir(dir)
app.config['UPLOAD_FOLDER'] = dir
db = PyMongo(app).db
model = PretrainedModel(database=db)


@app.route('/', methods=['GET', 'POST'])
def testing():
    form = MyForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(save_path)
        files = model.get_images(save_path, int(form.number.data))
        return render_template("Webapp.html", form=form, uploaded_image=filename, answers=files)
    else:
        return render_template('Webapp.html', form=form)


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)

