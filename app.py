from flask import Flask, render_template, request, redirect, session
import joblib
import json
import os

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")


app = Flask(__name__)
app.secret_key = "secret123"

model = joblib.load("dnn_model.pkl")
encoder = joblib.load("label_encoder.pkl")

def extract_features(url):
    return [
        len(url),
        url.count('.'),
        url.count('-'),
        url.count('@'),
        url.count('?'),
        url.count('='),
        url.count('/')
    ]

USERS_FILE = "users.json"
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

@app.route("/", methods=["GET", "POST"])
def login():
    with open(USERS_FILE) as f:
        users = json.load(f)

    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if u in users and users[u] == p:
            session["user"] = u
            return redirect("/dashboard")

        if u not in users:
            users[u] = p
            with open(USERS_FILE, "w") as f:
                json.dump(users, f)
            session["user"] = u
            return redirect("/dashboard")

    return render_template("index.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    result = None
    unsafe = False   # 🚨 flag

    if request.method == "POST":
        url = request.form["url"]

        features = np.array([extract_features(url)])
        pred = model.predict(features)
        result = encoder.inverse_transform(pred)[0]

        print("URL:", url)
        print("Result:", result)

        # 👇 VERY IMPORTANT LOGIC
        if result.lower() in ["malicious", "spam", "unsafe"]:
            unsafe = True
            session.clear()  # auto logout

    return render_template(
        "dashboard.html",
        result=result,
        unsafe=unsafe
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/browser")
def browser():
    return render_template("browser.html")

if __name__ == "__main__":
    app.run()


if __name__ == "__main__":
   app.run()

