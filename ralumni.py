#all imports

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, url_for
import os
from werkzeug import secure_filename
import random

import pickle



#our own modules from this project


# configuration

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['csv'])

DEBUG = True
SECRET_KEY = 'bijur123'
PICKLED_FILE = 'pickled.ab'
WINNERS_FILE = 'winners.ab'
COUNTDOWN = 6

# thats it, now lets do our app

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
    try:
        f = open(os.path.join(UPLOAD_FOLDER,WINNERS_FILE),'r')
        g.winners = pickle.load(f)
        f.close()
    except EOFError:
        f = open(os.path.join(UPLOAD_FOLDER,WINNERS_FILE),'w')
        g.winners = []
        f.close()
    except IOError:
        f = open(os.path.join(UPLOAD_FOLDER,WINNERS_FILE),'w')
        g.winners = []
        f.close()
        
@app.after_request
def after_request(response):
    f = open(os.path.join(UPLOAD_FOLDER,WINNERS_FILE),'w')
    pickle.dump(g.winners,f)
    f.close()
    return response


# some constants we will users



@app.route('/')
def index():
    if os.path.exists(os.path.join(UPLOAD_FOLDER, PICKLED_FILE)):
        g.winners = []
        return render_template('play.html')
        
    else:
        
        return redirect(url_for('upload',message = "First upload the users list"))


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload',  methods=['GET','POST'])
def upload():
    if request.method <> 'POST':
        return render_template('upload.html', message="Upload your CSV file separated by ; here")
    else:
        try:
            os.remove(os.path.join(UPLOAD_FOLDER,PICKLED_FILE))
            os.remove(os.path.join(UPLOAD_FOLDER,WINNERS_FILE))
        except OSError:
            pass
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            makePickle(filename)
            return redirect(url_for('index', message="File uploaded and pickle made"))




@app.route('/play',  methods=['GET','POST'])
def play():

    f = open(os.path.join(UPLOAD_FOLDER,PICKLED_FILE),'r')
    students = pickle.load(f)
    f.close()
    
    numStudents = len(students)
    #if numStudents >= 1:
    p = random.randint(0,numStudents-1)
    #else:
    #    return redirect(url_for('upload.html', message="List of students Finished. Upload your CSV file separated by ; here"))
    
    winner = students[p]
        
    name = unicode(winner[0], errors='ignore')
    #email = unicode(winner[1],errors='ignore')
    email = winner[1]

    g.winners.append({'name':name, 'email': email})

    students.remove( [ winner[0], winner[1] ] )

    f = open(os.path.join(UPLOAD_FOLDER,PICKLED_FILE),'w')
    pickle.dump(students, f)
    f.close()
    
    return render_template('winner.html', name = name, email = email, num= COUNTDOWN)

def makePickle(filename):

    f = open(os.path.join(UPLOAD_FOLDER,filename),'r')
    a = f.readlines()

    final = []

    for i in a[0].split('\r'):
        entry = i.split(';')
        a = len(entry)
        if a == 2 :
            final.append(entry)

    f.close()

    f = open(os.path.join(UPLOAD_FOLDER,PICKLED_FILE),'w')
    pickle.dump(final, f)
    f.close()
        
if __name__ == '__main__':
    app.run(host='0.0.0.0')
 #    app.run()




