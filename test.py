import sqlite3 as sql 

con = sql.connect("db.db")

# ========================================= zendora login ============================================
#t = '''CREATE TABLE login(
#    id,
#    email,
#    store,
#    password
#);
#'''


# ========================================== store login ===============================================
#t = '''CREATE TABLE Slogin(
#    sid,
#    email,
#    password,
#    address
#);
#'''


# ============================================ products ========================================================
#t = '''CREATE TABLE products(
#    id,
#    sid,
#    name,
#    img,
#    price,
#    description
#);
#'''


# ============================================== stor ==============================================
#t = '''CREATE TABLE store(
#    sid,
#    name,
#    img,
#    txt,
#    theme,
#    text
#)
#'''


# ==============================================  orders  =========================================


t = '''CREATE TABLE orders(
    id,
    sid,
    store,
    name,
    img,
    value,
    email
);
'''
import datetime
#con.execute('INSERT INTO login(id,email,store,password) VALUES(?,?,?,?);',("1","risgur00@gmail.com","bantana","password"))
x = "bantana"
img = "https://img1.wsimg.com/isteam/ip/7fc6e18a-828b-4048-abe3-8dd7aad63ecd/pexels-thorn-yang-168765-0001.jpg/:/rs=w:719"
p = "https://img1.wsimg.com/isteam/ip/7fc6e18a-828b-4048-abe3-8dd7aad63ecd/ols/pexels-claudio-olivares-medina-4036549edit.jpg"
txt = "CUTTING EDGE"
text = "Now taking online orders. Order today and get 15% 0ff your first order. Hurry while supplies last!"
#con.execute('INSERT INTO store(sid,name,img,txt,theme,text) VALUES(?,?,?,?,?,?);',[datetime.datetime.now(),x,img,txt,"1",text])
#con.execute(t)
a = con.execute('SELECT * FROM orders;').fetchall()
print(a)
con.commit()
con.close()