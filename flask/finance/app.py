import os

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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # if they send POST request
    if request.method == "POST":
        """deposit more cash"""

        try:
            # get deposit value and check if it's valid
            deposit = request.form.get("deposit")

            if not deposit or not deposit.replace('.', '', 1).isdigit() or float(deposit) <= 0:
                return apology("You need to enter a valid amount")

            deposit = float(deposit)

        except (TypeError, ValueError):
            return apology("You need to enter a number")

        # update the cash value in users if the transaction is successful
        db.execute("""
                    UPDATE users
                    SET cash = cash + ?
                    WHERE id = ?
                    """, deposit, session["user_id"])

        # return to porfolio after the transaction
        return redirect("/")

    else:
        """Show portfolio of stocks"""

        # get all the stock info of the user from portfolio
        portfolio = db.execute("""
                               SELECT * FROM portfolio
                               WHERE user_id = ?
                               """, session["user_id"])
        # to store each stock info
        stocks = []
        # to calculate the total value for capital calculation later on
        total_value = 0
        # loop and ad each stock info into stocks list
        for stock in portfolio:
            symbol = stock["symbol"]
            shares = int(stock["shares"])
            price = float(lookup(symbol)["price"])  # we need the live price with correct format
            value = shares * price  # total stock value for each stock
            total_value += value  # total value for all the stocks

            stocks.append({
                "symbol": symbol,
                "shares": shares,
                "price": price,
                "value": value,
            })

        # get current cash info from users
        cash_q = db.execute("""
                            SELECT cash FROM users
                            WHERE id = ?
                            """, session["user_id"])

        # format it properly
        cash = float(cash_q[0]["cash"])

        # sum of total cash and all the stocks owned by the user
        capital = cash + total_value

        return render_template("index.html", stocks=stocks, cash=cash, capital=capital)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        # get the symbol
        symbol = request.form.get("symbol")
        if not symbol:  # check for empty
            return apology("You need to enter a symbol")
        # get the price info
        price = lookup(symbol)
        if not price:  # check if empty (not found)
            return apology("symbol was not found")
        # get the shares wanted
        shares = request.form.get("shares")
        try:
            shares = int(shares)
            if shares <= 0:  # if zero or negative
                return apology("You need to enter a positive number")
        except ValueError:  # if not number
            return apology("You need to enter a number")

        shares = int(shares)

        price = float(price["price"])

        value = shares * price
        # get current cash info
        cash = db.execute("""
                          SELECT cash FROM users
                          WHERE id = ?
                          """, session["user_id"])
        cash = float(cash[0]["cash"])
        if value > cash:  # if not enough cash
            return apology("You don't have enough money")

        # calculate new cash
        cash -= value
        # update cash
        db.execute("""
                UPDATE users
                SET cash = ?
                WHERE id = ?
                """, cash, session["user_id"])
        # add to logs
        db.execute("""
                    INSERT INTO logs (user_id, symbol, shares, price, trans_type)
                    VALUES(?, ?, ?, ?, ?)
                    """, session["user_id"], symbol, shares, price, 'BUY')
        # update portfolio
        db.execute("""
                INSERT INTO portfolio (user_id, symbol, shares)
                VALUES (?, ?, ?)
                ON CONFLICT (user_id, symbol)
                DO UPDATE SET shares = shares + excluded.shares
                """, session["user_id"], symbol, shares)

        # return to portfolio page
        return redirect("/")

    # Render the buy page if GET request
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # query all the transactions made by the user
    logs = db.execute("""
                      SELECT * FROM logs WHERE user_id = ?
                      """, session["user_id"])
    # if they haven't made any transactions yet
    if not logs:
        return apology("You haven't made any transactions yet")
    stocks = []
    for stock in logs:
        symbol = stock["symbol"]
        shares = int(stock["shares"])
        price = float(stock["price"])
        value = float(stock["price"]) * int(stock["shares"])
        trans_type = stock["trans_type"]
        timestamp = stock["timestamp"]
        stocks.append({
            "symbol": symbol,
            "shares": shares,
            "price": price,
            "value": value,
            "trans_type": trans_type,
            "timestamp": timestamp,
        })
    else:
        return render_template("history.html", stocks=stocks)


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
        rows = db.execute("""
                          SELECT * FROM users
                          WHERE username = ?
                          """, request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    # if the user is entering data
    if request.method == "POST":
        # get the symbol from user
        symbol = request.form.get("symbol")

        # if submit an empty field
        if symbol == "":
            return apology("You need to enter a symbol")

        try:
            # look up the symbol data and display on the quoted page
            symbol_info = lookup(symbol)
            if symbol_info == None:
                return apology("There is no company with such symbol")
            return render_template("quoted.html", infos=symbol_info)

        # if they use incorrect characters
        except ValueError:
            return apology("You need to enter a valid stock name")
        except TypeError:
            return apology("You need to enter a valid stock name")

    else:
        # open the page if they are visiting it for the first time
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # assign the username, password and confirmation entered by the user
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # if they don't enter a username
        if not username:
            return apology("You need to enter a valid username")

        # if they don't enter a passowrd
        if not password:
            return apology("You need to enter a password")

        # if they don't enter the passowrd confirmation
        elif confirmation != password:
            return apology("Your password does not match with the confirmation")

        # store user's username and password in the database
        try:

            # secure the password via a hash
            pass_hash = generate_password_hash(password)

            # store username and pass_hash in username and hash
            db.execute("""
                       INSERT INTO users (username, hash) VALUES(?, ?)
                       """, username, pass_hash)

        # if the username has already been taken before
        except ValueError:
            return apology("This username has already been taken")

        # keep the record of the user in the session
        rows = db.execute("""
                          SELECT * FROM users
                          WHERE username = ?
                          """, username)
        session["user_id"] = rows[0]["id"]

        # redirect to this route after registration is successful
        return redirect("/")

    # return to this route if they make GET request
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        # get the symbol
        symbol = request.form.get("symbol")
        if not symbol:  # if empty
            return apology("You need to chose a symbol")
        # get symbol info
        price = lookup(symbol)
        if not price:  # if not available
            return apology("No such symbol")
        # get shares amount
        shares = request.form.get("shares")
        try:
            shares = int(shares)
            if shares <= 0:  # if not positive
                return apology("You need to enter a positive value")
        except ValueError:
            return apology("You need to enter a number")
        # check user shares
        shares_held = db.execute("""
                                 SELECT shares FROM portfolio
                                 WHERE user_id = ?
                                 AND symbol = ?
                                 """, session["user_id"], symbol)
        if not shares_held:  # if empty/not found
            return apology("You don't have this share")

        shares_held = int(shares_held[0]["shares"])

        if shares > shares_held:  # if they try to sell more than what they have
            return apology("You don't have that many shares")
        price = float(price["price"])
        value = shares * price

        # deduct the shares from portfolio
        db.execute("""
                    INSERT INTO portfolio (user_id, symbol, shares)
                    VALUES (?, ?, ?)
                    ON CONFLICT (user_id, symbol)
                    DO UPDATE SET shares = shares - excluded.shares
                    """, session["user_id"], symbol, shares)
        # Check if shares are now 0, and delete the row from portfolio if true
        remaining_shares = db.execute("""
                                        SELECT shares FROM portfolio
                                        WHERE user_id = ? AND symbol = ?
                                        """, session["user_id"], symbol)

        if remaining_shares and remaining_shares[0].get("shares", 0) == 0:
            db.execute("""
                        DELETE FROM portfolio
                        WHERE user_id = ? AND symbol = ?
                        """, session["user_id"], symbol)
        # get current cash
        cash = db.execute("""
                            SELECT cash FROM users
                            WHERE id = ?
                            """, session["user_id"])
        if cash == None:  # if not found
            return apology("Your cash data could not be retrived")
        cash = float(cash[0]["cash"])
        # calculate new cash
        cash += value
        # update cash in users
        db.execute("""
                    UPDATE users
                    SET cash = ?
                    WHERE id = ?
                    """, cash, session["user_id"])
        # add transaction to logs
        db.execute("""
                    INSERT INTO logs (user_id, symbol, shares, price, trans_type)
                    VALUES(?, ?, ?, ?, ?)
                    """, session["user_id"], symbol, shares, price, 'SELL')

        return redirect("/")

    # if they are just visiting the page (making GET request)
    else:

        # get the stocks they have in their portfolio
        stocks = db.execute("""
                            SELECT * FROM portfolio
                            WHERE user_id = ?
                            """, session["user_id"])

        # show the stocks they have in the selector
        return render_template("sell.html", stocks=stocks)


@app.route("/old_password", methods=["GET", "POST"])
@login_required
def old_password():
    """Ask for old password"""

    if request.method == "POST":

        # ask for the old password and its confirmation, and assign them to a variable
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # user's hash info
        user_h = db.execute("""
                            SELECT hash FROM users
                            WHERE id = ?
                            """, session["user_id"])

        user_h = user_h[0]["hash"]

        # if a field is left empty
        if not password:
            return apology("You need to enter a password in the field")

        # if they don't match
        if password != confirmation:
            return apology("The password doesn't match confirmation")
        # check if they entered their password correctly
        if check_password_hash(user_h, password):
            # if successful, send them to 'new_password' page
            return redirect("/new_password")
        else:
            return apology("You didn't enter your password correctly")

    else:
        # when they visit the page
        return render_template("old_password.html")


@app.route("/new_password", methods=["GET", "POST"])
@login_required
def new_password():
    """ask for the new password"""

    if request.method == "POST":

        # ask for a new password and its confirmation, and assign them to a variable
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # if the field is empty
        if not password:
            return apology("You need to enter a password")

        # if they don't match
        if password != confirmation:
            return apology("Your password and confirmation don't match")

        # hash the pass for security
        pass_hash = generate_password_hash(password)

        # update the user info in users with the new hash
        db.execute("""
                   UPDATE users
                   SET hash = ?
                   WHERE id = ?
                   """, pass_hash, session["user_id"])

        # after success return them to portfolio page
        return redirect("/")

    else:
        # if they are visiting the page
        return render_template("new_password.html")
