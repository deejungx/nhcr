from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template

if __name__ == '__main__':
    app.run()




# For small amount of inputs that fit in one batch, directly using __call__
# is recommended for faster execution, e.g., model(x), or model(x, training=False)

