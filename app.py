from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def echo():
    return render_template('index.html')

#debugger to edit while running
if __name__ == "__main__":
    app.run(debug=True)