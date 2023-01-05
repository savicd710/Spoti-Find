from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def echo():
    return render_template('index.html')

@app.route('/playlist')
def playlist():
    return render_template('playlist.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

#debugger to edit while running
if __name__ == "__main__":
    app.run(debug=True)