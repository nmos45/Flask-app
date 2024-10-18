from flask import Flask, render_template, session, redirect, url_for, g, request
from forms import PlatformChoice,RegistrationForm,LoginForm,ReviewForm
from flask_session import Session
from database import get_db,close_db
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import re

# Important features:
# movie score adapts to average reviews scores
# Password Validation
# Censored Reviews


app = Flask(__name__)
app.config["SECRET_KEY"] = "this is my secret key"
app.config ["SESSION_PERMANENT"] = False
app.config ["SESSION_TYPE"] = "filesystem"
Session(app)
app.teardown_appcontext(close_db)

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/all_films",methods = ['POST','GET'])
def all_films():
    form=PlatformChoice()
    Platform = None
    caption = None
    message = None
    if form.validate_on_submit():
        db = get_db()
        choice = form.choice.data
        Country = form.Country.data
        if choice == "Netflix" and Country == "ALL":
            Platform = db.execute("""SELECT * FROM Netflix;""" ).fetchall()
            caption =  "Netflix catalog"
        elif choice == "Netflix" and Country != "ALL":
            Platform = db.execute("""SELECT * FROM Netflix
                                  WHERE country like ? ;""",('%' + Country + '%',) ).fetchall()
            caption =  "Netflix catalog"

        elif choice == 'Amazon Prime' and Country == "ALL":
            Platform  = db.execute("""SELECT * FROM Amazon;""" ).fetchall()
            caption="Amazon prime catalog"
        elif choice == 'Amazon Prime' and Country != "ALL":
            Platform  = db.execute("""SELECT * FROM Amazon
                                   WHERE country like ?;""",('%' + Country + '%',) ).fetchall()
            caption="Amazon prime catalog"
            
        elif choice == 'Disney' and Country == "ALL":
            Platform  = db.execute("""SELECT * FROM Disney;""" ).fetchall()
            caption="Disney+ catalog"
        elif choice == 'Disney' and Country != "ALL":
            Platform  = db.execute("""SELECT * FROM Disney
                                    WHERE country like ?;""",('%' + Country + '%',) ).fetchall()            
            caption="Disney+ catalog" 
            
        if not Platform:
                message = "Unfortunately there are No films here currently"

    return render_template("all_films.html",caption=caption,Platform=Platform,form=form,message=message)



@app.route("/streaming_platforms/<film>",methods = ['POST','GET'])
def streaming_platforms(film):
    db = get_db()
    movie_score()
    platform = None
    message = None
    Netflix = db.execute("""SELECT * FROM Netflix JOIN NetflixCast
                    ON Netflix.title = NetflixCast.title WHERE  Netflix.title = (?);""",(film,)).fetchall()
    Amazon = db.execute("""SELECT * FROM Amazon JOIN AmazonCast
                    ON Amazon.title = AmazonCast.title WHERE  Amazon.title = (?);""",(film,)).fetchall()
    Disney = db.execute("""SELECT * FROM Disney JOIN DisneyCast
                    ON Disney.title = DisneyCast.title WHERE  Disney.title = (?);""",(film,)).fetchall()
    if Netflix:
        platform = Netflix
        message = film
    elif Amazon:
        platform = Amazon
        message = film
    elif Disney:
        platform = Disney
        message = film
    return render_template("movies.html",platform=platform,message=message)


@app.route("/register", methods=["GET", "POST"] )
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data
        special_chars = ["*","!","£","%",'^']
        db = get_db()
        conflict_user = db.execute("""SELECT * FROM users
                                    WHERE user_id = ?;""", (user_id,)).fetchone()
        if conflict_user is not None:
            form.user_id.errors.append("User name already taken")
        # https://www.javatpoint.com/password-validation-in-python ----- regular expressions from here
        elif  not re.search("[A-Z]", password): 
            form.password.errors.append("Must contain an uppercase Character")
        elif not re.search("[0-9]", password):  
            form.password.errors.append("Password must contain a number")
        elif not re.search("[*!£%^]", password):
            form.password.errors.append(f"Password must contain one of these Characters {special_chars}")
        else:
            db.execute("""INSERT INTO users (user_id, password)
              VALUES (?, ?);""", (user_id, generate_password_hash(password)))
            db.commit()
            return redirect(url_for("login"))       
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"] )
def login():
    form = LoginForm()
    message = ""
    if form.validate_on_submit(): 
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        user = db.execute("""SELECT * FROM users
                            WHERE user_id = ?;""", (user_id,)).fetchone()
        if user is None:
            form.user_id.errors.append("No such user name!")
        elif not check_password_hash(user["password"], password):
                form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            if check_password_hash(user["password"], password):
                session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

def appropriate(review):
    review = review.split()
    new_review = ""
    infile = open("censored.txt",'r')
    infile = infile.readlines()
    censored_words = [line.strip() for line in infile]
    for word in review:
        word = word.lower()
        if word in censored_words:
            new_review += '*' * len(word) + ' '
        else:
            new_review += word + ' '
    return new_review



def movie_score():
    db = get_db()
    reviews = db.execute("""SELECT DISTINCT(film) From reviews;""").fetchall()
    for review in reviews:
        film = review['film'] 
        total_score = db.execute("""SELECT SUM(score) FROM reviews
                             WHERE film = (?);""",(film,)).fetchone()
        num_entries = db.execute("""SELECT COUNT(score) FROM reviews
                             WHERE film = (?);""",(film,)).fetchone()
        total_score = total_score[0]
        num_entries = num_entries[0]
        if num_entries == 0:
            average_score = total_score
        else:
            average_score = round(total_score/num_entries,1)
        Netflix = db.execute("""SELECT * FROM Netflix
                         WHERE title = (?);""",(film,)).fetchall()
        Amazon = db.execute("""SELECT * FROM Amazon
                        WHERE title = (?);""",(film,)).fetchall()
        Disney = db.execute("""SELECT * FROM Disney
                        WHERE title = (?);""",(film,)).fetchall()
        if Netflix:
            db.execute("""UPDATE Netflix
           SET score = (?) WHERE title =  (?);""",(average_score,film))
            db.commit()
        elif Amazon:
            db.execute("""UPDATE Amazon
                   SET score = (?) WHERE title =  (?);""",(average_score,film))
            db.commit()
        elif Disney:
            db.execute("""UPDATE Disney
                   SET score = (?) WHERE title =  (?);""",(average_score,film))
            db.commit()



@app.route("/review",methods= ["POST","GET"])
@login_required 
def review():
    message = ""
    film = ""
    form = ReviewForm()
    if form.validate_on_submit():
        db=get_db()
        film = form.film.data
        review = form.review.data
        review  = appropriate(review)
        score = float(form.score.data)
        films = db.execute("""
    SELECT title FROM Netflix
    UNION 
    SELECT title FROM Amazon
    UNION 
    SELECT title FROM Disney
    WHERE title = ?;""", (film,)).fetchone()
        if films is not None:
            db.execute("""INSERT INTO reviews (user_id, review, film,score)
              VALUES (?, ?, ?,?);""", (session["user_id"], review, film,score))
            db.commit()
            movie_score()
            message = "Review has been added"
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("all_reviews")
            return redirect(next_page)
        else:
            message = "Film does not exist"
    return render_template("review.html",form=form, message=message,film=film)

@app.route("/favourites",methods = ["POST","GET"])
@login_required
def favourites():
    if "Watch Later" not in session:
        session["Watch Later"] = {}
    films = session["Watch Later"].split("&")
    return render_template("favourites.html",films=films)



@app.route("/watch_later/<film>",methods = ["POST","GET"])
@login_required
def watch_later(film):
    split_on = "&"
    if "Watch Later" not in session:
        session["Watch Later"] = {}
        session["Watch Later"] = film +  split_on
    elif film not in session["Watch Later"]:
        session["Watch Later"] = session["Watch Later"] +film + split_on
    return redirect( url_for("favourites"))



    
@app.route("/all_reviews",methods = ["POST","GET"])
@login_required
def all_reviews():
    reviews = " "
    db = get_db()
    reviews = db.execute(""" SELECT * FROM reviews;""").fetchall()
    return render_template("show_reviews.html", reviews=reviews, caption="Reviews")

@app.route("/show_specific_reviews/<film>",methods = ["POST","GET"])
def show_specific_reviews(film):
    db = get_db()
    reviews = db.execute(""" SELECT * FROM reviews
                         WHERE film = ?;""", (film,)).fetchall()
    return render_template("show_reviews.html", reviews=reviews, caption="Reviews")

@app.route("/Top_picks",methods = ["POST","GET"])
def Top_picks():
    db = get_db()
    top_picks = db.execute(""" SELECT * FROM Netflix UNION SELECT * 
                        FROM Amazon UNION SELECT * FROM Disney
                        ORDER BY score DESC;""").fetchall()
    return render_template("top_picks.html",top_picks=top_picks,caption="Our top films (Based on your Reviews)")

