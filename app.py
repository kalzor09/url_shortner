from flask import Flask ,  redirect , render_template ,request , url_for,flash,session
import random as rand
import string
from database.database_operations import DatabaseOperations

#CONSTANTS
DATABASE_NAME = "url_database.db"
app = Flask(__name__)
app.secret_key = "thisismysecretkeyfornow"

def random_string(size=5):
    chars = string.ascii_letters + string.digits
    random_str = ''.join(rand.choices(chars,k=size))
    return random_str

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random",methods=["GET","POST"])
def random():
    if request.method == "POST":
        actual_url = request.form["random"]
        short_url = random_string()
        DATABASE_OBJECT = DatabaseOperations(DATABASE_NAME)
        run = DATABASE_OBJECT.check_if_exists(short_url)
        while run:
            short_url = random_string()
            run = DATABASE_OBJECT.check_if_exists(short_url)
        db_ops  = DATABASE_OBJECT.insert_into_database(short_url,actual_url)
        DATABASE_OBJECT.close_connection()
        if db_ops==True:
            return render_template("generate.html",short_url=short_url)
        else:
            return render_template("random.html",error=True)
    else:
        return render_template("random.html")


@app.route("/custom",methods=["GET","POST"])
def custom():
    if request.method=="POST":
        actual_url = request.form["long"]
        short_url = request.form["short"]
        DATABASE_OBJECT = DatabaseOperations(DATABASE_NAME)
        run = DATABASE_OBJECT.check_if_exists(short_url)
        if run:
            return render_template("custom.html",error=True)
        else:
            DATABASE_OBJECT.insert_into_database(short_url,actual_url)
            DATABASE_OBJECT.close_connection()
            return render_template("generate.html",short_url=short_url)
    else:
        return render_template("custom.html")


@app.route("/<short_url>")
def full_site(short_url):
    # return f"Hello {shorturl}"
    DATABASE_OBJECT = DatabaseOperations(DATABASE_NAME)
    actual_url = DATABASE_OBJECT.get_actual_url(short_url)
    if actual_url:
        actual_url = actual_url[0]
        print("Redirecting...")
        return redirect(actual_url)
    else:
        return redirect(url_for("home"))

if __name__ == "__main__":
    # app = Flask(__main__)
    app.run(debug=True)