import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Check with session for the id
    user_id = session["user_id"]
    # Get shares and prices from table
    stocks = db.execute("SELECT symbol, SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP by symbol", user_id)
    # Get money amout from table
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    total = cash
    # Loop through for total
    total = sum(stock["price"] * stock["shares"] for stock in stocks)
    # render template
    return render_template("index.html", stocks=stocks, cash=cash, usd=usd, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        # Check for fractional numbers or strings
        try:
            shares = float(request.form.get("shares"))
        except ValueError:
            return apology("Please enter a valid number.")

        if shares % 1 != 0:
            return apology("Please do not use fractional numbers.")

        if not symbol:
            return apology("Select a stock")
        # API
        stock = lookup(symbol.upper())
        # Check for right input
        if stock is None:
            return apology("Stock did not exist")

        if not shares > 0:
            return apology("Type in a positive number")
        # Complete value of transaction
        tvalue = shares * stock["price"]
        # get user id
        user_id = session["user_id"]
        # Select cash from user
        ucash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        ucash = ucash_db[0]["cash"]
        # Check balance
        if ucash < tvalue:
            return apology("Check credit balance")
        # Updatecash
        updatec = ucash - tvalue
        # update in db
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updatec, user_id)
        # Datetime from Datetime lib for timestamp
        date = datetime.datetime.now()
        # Insert into table
        new_user = db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                              user_id, stock["symbol"], shares, stock["price"], date)
        # Show text if transaction was succesfully
        flash("Your transaction was succesfully!")
        # Redirect to main page after buy
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions_db = db.execute("SELECT * FROM transactions WHERE user_id = :id", id=user_id)
    return render_template("history.html", transactions=transactions_db, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        #
        if not symbol:
            return apology("Select a stock")
        # Get API data
        stock = lookup(symbol.upper())
        # Return apology if stock not found
        if stock is None:
            return apology("Stock did not exist")
        return render_template("quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"], usd=usd)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Render the new register page
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Get Input
        user = request.form.get("username")
        pw = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Check for correct input
        if not user:
            return apology("Type in a username")
        if not pw:
            return apology("Type in a password")
        if pw != confirmation:
            return apology("Passwords did not match")
        if not confirmation:
            return apology("Please confirmate")

    # generate the passwordhash
    pwhash = generate_password_hash(pw)
    # Insert in DB
    try:
        new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", user, pwhash)
    except:
        return apology("User already exists")

    # Directly forward login after registration
    session["user_id"] = new_user
    # Redirect
    return redirect("/sell")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        # API request
        stock = lookup(symbol.upper())
        # Check for correct input
        if not symbol:
            return apology("Select a stock")

        if stock is None:
            return apology("Stock did not exist")

        if not shares > 0:
            return apology("Type in a positive number")

        tvalue = shares * stock["price"]
        # Get user id from session
        user_id = session["user_id"]
        # Get cash from db
        ucash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        ucash = ucash_db[0]["cash"]
        # Get shares from db
        ushares = db.execute(
            "SELECT shares FROM transactions WHERE user_id = :id AND symbol = :symbol GROUP BY symbol", id=user_id, symbol=symbol)
        ushares_complete = ushares[0]["shares"]
        # usercash + transactioncash
        updatec = ucash + tvalue
        # Check if there are enough shares
        if not shares < ushares_complete:
            return apology("Insufficient share balance")
        # update cash in db
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updatec, user_id)
        # timestamp
        date = datetime.datetime.now()
        # Insert into table
        new_user = db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                              user_id, stock["symbol"], (-1)*shares, stock["price"], date)
        # Show text if transaction was succesfully
        flash("Your Stock was sold!")
        # Redirect to main page after buy
        return redirect("/")

    else:
        user_id = session["user_id"]
        symbols_user = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = :id GROUP BY symbol HAVING SUM(shares) > 0", id=user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in symbols_user])


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add cash to your account"""
    if request.method == "GET":
        return render_template("addcash.html")
    else:
        new_cash = int(request.form.get("new_cash"))

        if not new_cash:
            return apology("Type in a number")
        # Get the session id
        user_id = session["user_id"]

        ucash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)

        ucash = ucash_db[0]["cash"]

        updatec = ucash + new_cash

        db.execute("UPDATE users SET cash = ? WHERE id = ?", updatec, user_id)
        flash("Cash was succesfully added!")
        return redirect("/")


@app.route("/deletecash", methods=["GET", "POST"])
@login_required
def deletecash():
    """Add cash to your account"""
    if request.method == "GET":
        return render_template("deletecash.html")
    else:
        new_cash = int(request.form.get("new_cash"))

        if not new_cash:
            return apology("Type in a number")
        # Get the session id
        user_id = session["user_id"]

        ucash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        ucash = ucash_db[0]["cash"]

        updatec = ucash - new_cash

        db.execute("UPDATE users SET cash = ? WHERE id = ?", updatec, user_id)
        flash("Cash was succesfully deleted!")
        return redirect("/")