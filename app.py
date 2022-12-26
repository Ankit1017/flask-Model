#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
from model import result_str
import pickle
import numpy as np

 
app = Flask(__name__)
model=pickle.load(open('model.pkl','rb'))
model1=pickle.load(open('model1.pkl','rb'))
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Image')
def Image():
    return render_template('Image.html')
@app.route('/friend')
def friend():
    return render_template('friend.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def index():
    return render_template('index.html')
 
@app.route('/Image/predict1', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        str=os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        x=str.replace(os.sep, '/')
        
        pred=result_str(x)
        
        return render_template('Image.html', filename=filename, prediction = pred)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
    
@app.route('/friend/predict2',methods=['POST','GET'])
def predict():
    int_features=[float(x) for x in request.form.values()]
    final=[np.array(int_features)]
    prediction=model.predict(final)
    print(prediction)
    output='{0:.{1}f}'.format(prediction[0], 2)
    if output>str(1):
        return render_template('friend.html',pred='Your Friend is in Danger.\nProbability of Ch*tiyaness is 1',bhai="kuch karna hain iska ab?")
    elif output>str(0.5):
        return render_template('friend.html',pred='Your Friend is in Danger.\nProbability of Ch*tiyaness is {}'.format(output),bhai="kuch karna hain iska ab?")
    elif output<str(0):
        return render_template('friend.html',pred='Your Friend is not in Danger.\nProbability of Ch*tiyaness is 0',bhai="Your Friend is Safe for now")
    else:
        return render_template('friend.html',pred='Your Friend is not in Danger.\nProbability of Ch*tiyaness is {}'.format(output),bhai="Your Friend is Safe for now")
    
    
    
@app.route('/about/predict',methods=['POST','GET'])
def pred():
    int_features=[float(x) for x in request.form.values()]
    final=[np.array(int_features)]
    print(final)
    prediction=model1.predict(final)/2
    output='{0:.{1}f}'.format(prediction[0], 2)
    return render_template('about.html',pred='Your salary is  {} lakhs/annum '.format(output))
    
        
    

if __name__ == "__main__":
    app.run()