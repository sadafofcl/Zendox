from flask import Flask, request, render_template, redirect,session
import sqlite3 as sql
import datetime

app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route("/")
def index():
    if 'z-user' in session:
        if session['z-user'] != "":
            return redirect("/" + session['z-user'] + "/edit/home")
        else:
            return render_template("index.htm")
    else:
        return render_template("index.htm")
# =====================================================   LOGIN  ===================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        a = request.form["name"]
        b = request.form["password"]
        con = sql.connect("db.db")
        res = con.execute('SELECT * FROM login WHERE store = ?;',[a]).fetchall()
        con.close()
        if res == []:
            return render_template("error.html",e="No USER Found")
        else:
            if res[0][3] == b:   
                session['z-user'] = a
                return redirect("/" + session['z-user'] + "/edit/home")
            else:
                return render_template("error.html",e="wrong password")
    else:
        if 'z-user' in session:
            if session['z-user'] != "":
                return redirect("/" + session['z-user'] + "/edit/home")
            else:
                return render_template("login.htm")
        else:
            return render_template("login.htm")

#  ===================================================== store SIGNUP ===================================================

@app.route("/create-store", methods=['GET', 'POST'])
def create_store():
    if request.method == 'POST':
        if "s-c-email" in session:
            img = "https://img1.wsimg.com/isteam/ip/7fc6e18a-828b-4048-abe3-8dd7aad63ecd/pexels-thorn-yang-168765-0001.jpg/:/rs=w:719"
            txt = "CUTTING EDGE"
            text = "Now taking online orders. Order today and get 15% 0ff your first order. Hurry while supplies last!"
            a = request.form["store"]
            b = request.form["password"]
            con = sql.connect("db.db")
            res = con.execute('SELECT * FROM login WHERE store = ?;',[a]).fetchall()
            if res == []:
                con.execute('INSERT INTO login(id,email,store,password) VALUES(?,?,?,?);',[datetime.datetime.now(),session['s-c-email'],a,b])
                con.commit()
                con.execute('INSERT INTO store(sid,name,img,txt,theme,text) VALUES(?,?,?,?,?,?);',[datetime.datetime.now(),a,img,txt,"1",text])
                con.commit()
                con.close()
                session["z-user"] = a
                return redirect("/")
            else:
                con.close()
                return render_template("error.html",e="Stor already exist")
        else:
            return redirect("/")
    else:
        if 'z-user' in session:
            if session['z-user'] != "":
                return redirect("/" + session['z-user'] + "/edit/home")
            else:
                return render_template("s_signup.html")
        else:
            return render_template("s_signup.html")

@app.route("/e-store", methods=['GET', 'POST'])
def e_store():
    if request.method == 'POST':
        a = request.form["email"]
        con = sql.connect("db.db")
        cc = con.execute('SELECT * FROM login WHERE email = ?;',[a]).fetchall()
        con.close()
        if cc == []:
            session["s-c-email"] = a
            return redirect("/create-store")
        else:
            return render_template("error.html",e="emial already in use")
    else:
        redirect("/")







# ==============================================  STORE  ================================================

@app.route("/<store>")
def user(store):
    con = sql.connect("db.db")
    res = con.execute('SELECT * FROM store WHERE name = ?;',[store]).fetchall()
    if res == []:
        con.close()
        return render_template("error.html",e="Store not found")
    else:
        stor = con.execute('SELECT * FROM products WHERE sid = ?;',[res[0][0]]).fetchall()
        con.close()
        print(res[0][4])
        if res[0][4] == "1":
            return render_template("/store/1.htm",data=res,items=stor,store=store)
        else:
            return render_template("/store/1.htm",data=res,items=stor,store=store)

#  ================================================   product   ========================================

@app.route("/<store>/product/<id>", methods=['GET', 'POST'])
def stor_product(store,id):
    if request.method == 'POST':
        if session['s-user'] != "":
            a = request.form["id"]
            b = request.form["sid"]
            c = request.form["name"]
            d = request.form["img"]
            ee = request.form["price"]
            con = sql.connect("db.db")
            con.execute('INSERT INTO orders(id,sid,store,name,img,value,email) VALUES(?,?,?,?,?,?,?);',[a,b,store,c,d,ee,session['s-user']])
            con.commit()
            con.close()
            return redirect("/"+ store)
        else:
            return render_template("error.html",e="please create an account first")
    
    else:
        con = sql.connect("db.db")
        res = con.execute('SELECT * FROM store WHERE name = ?;',[store]).fetchall()
        if res == []:
            con.close()
            return render_template("error",e="page not found")
        else:
            stor = con.execute('SELECT * FROM products WHERE sid = ? AND id = ?;',[res[0][0],id]).fetchall()
            con.close()
            if stor != []:
                if res[0][4] == "1":
                    return render_template("/store/p1.htm",data=res,items=stor,qq="1",aaa=store)
                else:
                    return render_template("/store/p1.htm",data=res,items=stor,qq="2",aaa=store)
            else:
                return render_template('error.html',e="no product found",aaa=store)

#  ============================================   CART    ===============================================

@app.route("/<store>/user/cart")
def scart_product(store):
    if "s-user" in session:
        if session['s-user'] != "":
            con = sql.connect("db.db")
            rec = con.execute('SELECT * FROM store WHERE name = ?;',[store]).fetchall()
            con.close()
            con = sql.connect("db.db")
            res = con.execute('SELECT * FROM orders WHERE store = ? AND email = ?;',[store,session['s-user']]).fetchall()
            con.close()
            print(rec[0][4])
            if rec[0][4] == "1":
                return render_template("/store/cart.htm",aaa=store,data=res,qq="1")
            else:
                return render_template("/store/cart.htm",aaa=store,data=res,qq="2")
        else:
            return redirect("/" + store + "/user/signin")
    else:
        return redirect("/" + store + "/user/signup")
    

#   =====================================================================================================
#   =========================================   STOR USER  ==============================================
#   =====================================================================================================


@app.route("/<store>/user")
def stor_user(store):
    if "s-user" in session:
        if session['s-user'] != "":
            return render_template("/store/stor_user.htm",stor=store,qq="Logout",herf="user/logout")
        else:
            return render_template("/store/stor_user.htm",stor=store,qq="Login",herf="user/signin")
    else:
        return render_template("/store/stor_user.htm",stor=store,qq="Signup",herf="user/signup")
    
@app.route("/<store>/user/logout")
def stor_user_logout(store):
    if "s-user" in session:
        if session['s-user'] != "":
            session['s-user'] = ""
            return redirect("/" + store)
        else:
            return redirect("/" + store)
    else:
            return redirect("/" + store)

#   ===========================================   product  search   ==========================================


@app.route("/<store>/product/search",  methods=['GET', 'POST'])
def search_product(store):
    if request.method == 'POST':
        a = request.form['name']
        con = sql.connect("db.db")
        eq = con.execute('SELECT * FROM products;').fetchall()
        rec = con.execute('SELECT * FROM store WHERE name = ?;',[store]).fetchall()
        con.close()
        res = []
        for i in eq:
            if a.upper() in str(i[2]).upper():
                res.append(i)
        if rec[0][4] == "1":
            return render_template("/store/search.htm" ,data =res,aaa=store,qq="1")
        else:
            return  render_template("/store/search.htm" ,data =res,aaa=store,qq="2")
    else:
        con = sql.connect("db.db")
        rec = con.execute('SELECT * FROM store WHERE name = ?;',[store]).fetchall()
        con.close()
        if rec[0][4] == "1":
            return render_template("/store/search.htm",aaa=store,qq="1")
        else:
            return  render_template("/store/search.htm",aaa=store,qq="2")
    


#  #######################################################################################################
#  ================================================= STORE   EDIT ========================================
#  =======================================================================================================

               ###############################   SECURITY     ###############################

# =========================================    LooK    ==============================================

@app.route("/<store>/edit/home",  methods=['GET', 'POST'])
def home(store):
    if request.method == 'POST':
        a = request.form["img"]
        b = request.form["txt"]
        c = request.form["theme"]                                                                ##       #  #  #     DONE
        d = request.form["text"]
        con = sql.connect("db.db")
        con.execute("UPDATE store SET img = ?, txt = ?, theme = ?, text =? WHERE name = ?;",[a,b,c,d,store])
        con.commit()
        con.close()
        return redirect("/")

    else:
        if 'z-user' in session:
            if session['z-user'] != "":
                con = sql.connect("db.db")
                req = con.execute('SELECT * FROM store WHERE name = ?;',[store]).fetchall()[0]
                return render_template("home.htm",aaa=store,data=req)
            else:
                return redirect("/")
        else:
            return redirect("/")

#   ==========================================   ORDERS    ================================

@app.route("/<store>/edit/orders")
def orders(store):
    if 'z-user' in session:
        if session['z-user'] != "":
            con = sql.connect("db.db")
            a = con.execute('SELECT * FROM orders WHERE store = ?;',[store]).fetchall()
            con.close()
            return render_template("orders.htm",aaa=store,data=a)
        else:
            return redirect("/")
    else:
        return redirect("/")

#   ==============================================  DELETE  OPRDERS   ======================================

@app.route("/<store>/delete-order/<sid>/<id>")
def del_orders(store,sid,id):
    if 'z-user' in session:
        if session['z-user'] != "":
            con = sql.connect("db.db")
            con.execute('DELETE FROM orders WHERE id =? AND sid =?;',[id,sid])
            con.commit()
            con.close()
            return redirect("/" + store + "/edit/home")
        else:
                return redirect("/")
    else:
        return redirect("/")

#  =========================================   PRODUCTS   =================================

@app.route("/<store>/edit/products")
def productss(store):
    if 'z-user' in session:
        if session['z-user'] != "":
            con = sql.connect("db.db")
            a = con.execute('SELECT * FROM store WHERE name = ?;',[store]).fetchall()
            req = con.execute('SELECT * FROM products WHERE sid = ?;',[a[0][0]]).fetchall() 
            con.close()
            return render_template("products.htm",aaa=store,data=req)
        else:
                return redirect("/")
    else:
        return redirect("/")

#  ==================================   Products  Add   ======================================

@app.route("/<store>/edit/products/add",  methods=['GET', 'POST'])
def productss_add(store):
    if request.method == 'POST':
        a = request.form["name"]
        b = request.form["img"]
        c = request.form["val"]
        d = request.form["dis"]
        con = sql.connect("db.db")
        eq = con.execute('SELECT sid FROM store WHERE name =?;',[store]).fetchall()[0][0]
        con.execute('INSERT INTO products(id,sid,name,img,price,description) VALUES(?,?,?,?,?,?)',[datetime.datetime.now(),eq,a,b,c,d]) 
        con.commit()                  
        con.close() 
        return redirect("/" + store + "/edit/products")
    else:
        if 'z-user' in session:
            if session['z-user'] != "":
                return render_template("products_add.htm",aaa=store)
            else:
                return redirect("/")
        else:
            return redirect("/")
    
#  ===================================    customers   =====================================

@app.route("/<store>/edit/customers")
def customers(store):
    if 'z-user' in session:
        if session['z-user'] != "":
            con = sql.connect("db.db")
            a = con.execute('SELECT * FROM store WHERE name = ?;',[store]).fetchall()
            req = con.execute('SELECT * FROM Slogin WHERE sid = ?;',[a[0][0]]).fetchall()                                                                  
            return render_template("customers.htm",aaa=store,data=req)
        else:
                return redirect("/")
    else:
        return redirect("/")

#  ==================================   PRODUCT EDIT   ======================================

@app.route("/<store>/edit/product/<id>", methods=['GET', 'POST'])
def product(store,id):
    if request.method == 'POST':
        a = request.form["name"]
        b = request.form["img"]
        c = request.form["val"]
        d = request.form["dis"]
        con = sql.connect("db.db")
        con.execute('UPDATE products SET name = ?, img = ?, price = ?, description = ?;',[a,b,c,d])                       # # #    PENDING    
        con.close() 
    else:
        if 'z-user' in session:
            if session['z-user'] != "":
                con = sql.connect("db.db")
                req = con.execute('SELECT * FROM products WHERE id = ?;',[id]).fetchall()[0]                      # # #    PENDING    
                con.close()   
                if req == []:
                    return render_template("error.html",e="no product found")
                else:
                    return render_template("product_edit.htm",aaa=store,data=req)
            else:
                return redirect("/")
        else:
            return redirect("/")

#   ==========================================   DELETE Product   =======================================

@app.route("/<store>/<sid>/DELETE-product/<id>")
def product_delete(store,sid,id):
    if 'z-user' in session:
        if session['z-user'] != "":
            con = sql.connect("db.db")
            con.execute('DELETE FROM products WHERE sid = ? AND id = ?;',[sid,id])   
            con.commit()
            con.close()                        
            return redirect("/" + store + "/edit/products")
        else:
                return redirect("/")
    else:
        return redirect("/")
  

# =============================================== STORE Personal SIGNUP ==========================================

            #####################################    update AVAILABLE    ##############################


@app.route("/<store>/user/signup", methods=['GET', 'POST'])
def store_personal_signup(store):
    if request.method == 'POST':
        a = request.form["email"]
        b = request.form["password"]
        c = request.form["address"]
        con = sql.connect("db.db")
        res = con.execute('SELECT * FROM Slogin WHERE email = ?;',[a]).fetchall()
        if res == []:
            req = con.execute("SELECT * FROM store WHERE name = ?;",[store]).fetchall()
            con.execute('INSERT INTO Slogin(sid,email,password,address) VALUES(?,?,?,?);',[req[0][0],a,b,c])
            con.commit()
            con.close()
            session['s-user'] = a
            return redirect("/" + store)
        else:
            con.close()
            return render_template("/store/error.html",e="email already exist",aaa=store) 
        
    else:
        if 's-user' in session:
            if session['s-user'] != "":
                return redirect("/" + store)
            else:
                return render_template("/store/signup.html",aaa=store)
        else:
                return render_template("/store/signup.html",aaa=store)


# =============================================== STORE Personal Log-IN ==========================================

            #####################################    update AVAILABLE    ##############################

@app.route("/<store>/user/signin", methods=['GET', 'POST'])
def store_personal_login(store):
    if request.method == 'POST':
        a = request.form["email"]
        b = request.form["password"]
        con = sql.connect("db.db")
        res = con.execute('SELECT * FROM Slogin WHERE email = ?;',[a]).fetchall()
        con.close()
        if res == []:
            return render_template("error.html",e="no user found",aaa=store) 
        else:
            if b == res[0][2]:
                session['s-user'] = a
                return redirect("/" + store)
            else:
                return render_template("error.html",e="wrong password",aaa=store) 
        
    else:
        if 's-user' in session:
            if session['s-user'] != "":
                return redirect("/" + store)
            else:
                return render_template("/store/login.html",aaa=store)
        else:
            return render_template("/store/login.html",aaa=store)




@app.route("/<store>/logout")
def logout(store):
    if "z-user" in session:
        session['z-user'] = ""
        return redirect("/")
    else:
        return redirect("/")

#404 Page not found
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html',e= "Page Not Found"), 404


