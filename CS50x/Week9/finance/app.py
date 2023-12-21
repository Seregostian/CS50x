import os
import re
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    # Create a table for index
    rows = db.execute("SELECT symbol, SUM(shares) FROM transactions WHERE user_id=:user_id GROUP BY symbol HAVING SUM(shares) > 0", user_id=session["user_id"])

    # Creates a place to save the informations
    holdings = []
    all_total = 0

    for row in rows:
        stock = lookup(row['symbol'])
        sum_value = (stock["price"] * row["SUM(shares)"])
        holdings.append({"symbol": stock["symbol"], "name": stock["name"], "shares": row["SUM(shares)"], "price": usd(stock["price"]), "total": usd(sum_value)})
        all_total += stock["price"] * row["SUM(shares)"]

    rows = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"])
    cash = rows[0]["cash"]
    all_total += cash

    return render_template("index.html", holdings=holdings, cash=usd(cash), all_total=usd(all_total))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        #Getting inputs from form
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        stock = lookup(symbol)

        #Input Validation
        if not symbol:
            return apology("Provide a symbol")

        elif not stock:
            return apology("Symbol not found")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Shares should be a integer!")

        if shares <= 0:
            return apology("Shares cannot be negativ")
        #User validation
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = cash[0]["cash"]
        #Counting share value
        transaction = shares * stock["price"]
        date = datetime.datetime.now()
        typ = "Buy"

        if user_cash < transaction:
            return apology("Not enough money")

        else:
            #Adding changes for buying
            db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash - transaction, user_id)
            db.execute("INSERT INTO history (user_id, name, price, shares, symbol, time, type) VALUES (?, ?, ?, ?, ?, ?, ?)", user_id, stock["name"],  stock["price"], shares, stock["symbol"], date, typ)
            flash("Thanks for buy!")
            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    #Calling items from
    history_db = db.execute("SELECT type, name, symbol, shares, price, time FROM history WHERE user_id = ?", user_id)
    return render_template("history.html", history_db=history_db, usd=usd)


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

    # https://i.imgur.com/equNkNw.png


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        if not symbol:
            return apology("Please enter symbol")

        elif not stock:
            return apology("There is no Symbol")
        else:
            return render_template("quoted.html", stock=stock, usd=usd)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Invalid form!", 400)
        if not password:
            return apology("Invalid form!", 400)
        if not confirmation:
            return apology("Invalid form!", 400)

        if password != confirmation:
            return apology("Password did not match!", 400)

        # Check username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("Username is not available!", 400)

        # https://docs.python.org/3/library/re.html
        if not re.search("[!@#$%^&*()]", password):
            return apology(
                "Password must contain special characters such as: !@#$%^&*()", 400
            )

        if not re.search("[0-9]", password):
            return apology("Password must contain digits!", 400)

        if not len(password) > 5:
            return apology("Passowrd must have more than 5 characters!", 400)

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        session["user_id"] = rows[0]["id"]

        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    userid = session["user_id"]
    if request.method == "GET":
        data = db.execute(
            "SELECT symbol FROM portfolio WHERE user_id = ?", userid)
        return render_template("sell.html", data=data)
    else:
        # check empty fields
        sell_symbol = request.form.get('symbol')
        sell_shares = float(request.form.get('shares'))
        if not sell_symbol or not sell_shares or sell_shares <= 0 or sell_shares == " ":
            return apology('stop submitting empty field')
        # check if user has stock and if user has shares more than sell order
        user_shares = db.execute(
            "SELECT shares FROM portfolio WHERE user_id=? AND symbol = ?", userid, sell_symbol)
        if len(user_shares) != 1 or sell_shares > float(user_shares[0]['shares']):
            return apology('Impossible Amount')

        # all data verified
        # lookup share price at Market
        data = lookup(sell_symbol.upper())
        # assign required variables
        row = db.execute("SELECT cash FROM users WHERE id = ?", userid)
        price = float(data['price'])
        transaction_val = sell_shares * price
        cash = float(row[0]["cash"])
        date = datetime.datetime.now()
        t_type = "SELL"
        # update transaction to database
        # transactions table
        db.execute("INSERT INTO transactions (user_id,symbol,shares,price,type,date) VALUES (?,?,?,?,?,?)",
                   userid, sell_symbol, sell_shares, price, t_type, date)
        # cash database
        updated_cash = cash + transaction_val
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   updated_cash, userid)
        # portfolio database
        if user_shares[0]['shares'] == sell_shares:
            db.execute(
                "DELETE FROM portfolio WHERE user_id = ? AND symbol = ?", userid, sell_symbol)
        else:
            row = db.execute(
                "SELECT shares FROM portfolio WHERE user_id = ? AND symbol = ?", userid, sell_symbol)
            share_in_hand = row[0]["shares"]
            new_shares = share_in_hand - sell_shares
            # update no of shares
            db.execute("UPDATE portfolio SET shares = ? WHERE user_id = ? AND SYMBOL = ? ",
                       new_shares, userid, sell_symbol)

        return redirect('/')

#DISCLAIMER: Instead of doing 'check' i did 'submit' by accident, and i got a green check mark????
#Is it a bug? an error? is that intended to work as such? that's odd. I mean it got approved but still
#My buy and sell functions were getting errors, how is that a green check mark?
