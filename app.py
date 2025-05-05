from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql

app=Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/add_products',methods=['POST','GET'])
def add_products():
    if request.method=="POST":
        pname=request.form['pname']
        price=int(request.form['price'])
        qty=int(request.form['qty'])
        lname=request.form['lname']
        con=sql.connect("inventory.db")
        cur=con.cursor()

        cur.execute("select P_ID from products where P_NAME=?",(pname,))
        if not cur.fetchone():
            cur.execute("insert into products(P_NAME,PRICE) values(?,?)",(pname,price))
            con.commit()
        cur.execute("select P_ID from products where P_NAME=?",(pname,))
        pid=cur.fetchone()[0]

        cur.execute("select L_ID FROM locations where L_NAME=?",(lname,))
        if not cur.fetchone():
            cur.execute("insert into locations(L_NAME) values(?)",(lname,))
            con.commit()
        
        cur.execute("select QTY from stocks where P_ID=? AND L_NAME=?",(pid,lname))
        row=cur.fetchone()
        if row:
            cur_qty=int(row[0])
            new_qty=cur_qty+qty
            cur.execute("update stocks set QTY=? where P_ID=? AND L_NAME=?",(new_qty,pid,lname))
        else:
            cur.execute("insert into stocks(P_ID,P_NAME,L_NAME,QTY) values (?,?,?,?)",(pid,pname,lname,qty))
        con.commit()
        con.close()

        flash("product added successfully","success")
        return redirect(url_for("view_products"))
    
    return render_template('add_products.html')

@app.route('/view_products')
def view_products():
    con=sql.connect("inventory.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from products")
    data=cur.fetchall()
    return render_template("view_products.html",datas=data)


@app.route('/edit_products/<string:pid>',methods=['POST','GET'])
def edit_products(pid):
    if request.method=="POST":
        pname=request.form['pname']
        price=request.form['price']
        con=sql.connect("inventory.db")
        cur=con.cursor()
        cur.execute("update products set P_NAME=?,PRICE=? where P_ID=?",(pname,price,pid))
        cur.execute("update stocks set P_NAME=? where P_ID=?",(pname,pid))
        con.commit()
        flash("product updated successfully","success")
        return redirect(url_for("view_products"))
    con=sql.connect("inventory.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from products where P_ID=?",(pid,))
    data=cur.fetchone()
    return render_template("edit_products.html",datas=data)

@app.route('/add_locations',methods=['POST','GET'])
def add_locations():
    if request.method=="POST":
        lname=request.form['lname']
        con=sql.connect("inventory.db")
        cur=con.cursor()
        cur.execute("insert into locations(L_NAME) values(?)",(lname,))
        con.commit()
        flash("locations successfully added","success")
        return redirect(url_for("add_locations"))
    return render_template('add_locations.html')

@app.route('/view_locations')
def view_locations():
    con=sql.connect("inventory.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from locations")
    data=cur.fetchall()
    return render_template("view_locations.html",datas=data)

@app.route('/edit_locations/<string:lid>',methods=['POST','GET'])
def edit_locations(lid):
    if request.method=="POST":
        new_lname=request.form['lname']
        con=sql.connect("inventory.db")
        cur=con.cursor()
        cur.execute("update locations set L_NAME=? where L_ID=?",(new_lname,lid))
        cur.execute("select L_NAME from locations where L_ID=?",(lid,))
        old_lname=cur.fetchone()[0]
        cur.execute("update stocks set L_NAME=? where L_NAME=?",(new_lname,old_lname))
        con.commit()
        flash("Location updated successfully","success")
        return redirect(url_for("view_locations"))
    con=sql.connect("inventory.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from locations where L_ID=?",(lid,))
    data=cur.fetchone()
    return render_template("edit_locations.html",datas=data)

@app.route('/view_stocks')
def view_stocks():
    con=sql.connect("inventory.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from stocks")
    data=cur.fetchall()
    return render_template("view_stocks.html",datas=data)

@app.route('/move_products',methods=['GET','POST'])
def move_products():
    if request.method=="POST":
        con=sql.connect("inventory.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        pname=request.form["pname"]
        cur.execute("select P_ID from products where P_NAME=?",(pname,))
        pid=cur.fetchone()[0]
        fromloc=request.form.get("fromloc") or None
        toloc=request.form.get("toloc") or None
        qty=int(request.form["qty"])
        if qty<=0:
           flash("Invalid Quantity:Please Provide Valid One","warning") 
           return redirect(url_for("move_products"))
        if not fromloc and not toloc:
            flash("Please provide either 'From' or 'To' location","warning") 
            return redirect(url_for("move_products"))
        if fromloc:
            cur.execute("select QTY from stocks where P_ID=? AND L_NAME=?",(pid,fromloc))
            res=cur.fetchone()
            if not res or res["QTY"]<qty:
                flash(f"Not enough stock in {fromloc} to move.","danger")
                return redirect(url_for("move_products"))
            new_qty=res["QTY"]-qty
            cur.execute("update stocks set QTY=? where P_ID=? AND L_NAME=?",(new_qty,pid,fromloc))
        if toloc:
            cur.execute("select QTY from stocks where P_NAME=? AND L_NAME=?",(pname,toloc))
            res=cur.fetchone()
            if res:
                new_qty=res[0]+qty
                cur.execute("update stocks set QTY=? where P_ID=? AND L_NAME=?",(new_qty,pid,toloc))
            else:
                cur.execute("insert into stocks(P_ID,P_NAME,L_NAME,QTY) VALUES(?,?,?,?)",(pid,pname,toloc,qty))

        cur.execute("insert into movements(P_ID,QTY,FROM_LOCATION,TO_LOCATION) VALUES(?,?,?,?)",(pid,qty,fromloc,toloc))
        con.commit()
        flash("product Moved successfully","success")
        return redirect(url_for("view_productmovements"))

    con=sql.connect("inventory.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select *from products")
    p_data=cur.fetchall()
    cur.execute("select *from locations")
    l_data=cur.fetchall()
    return render_template("move_products.html",products=p_data,locations=l_data)

@app.route('/view_productmovements')
def view_productmovements():
    con=sql.connect("inventory.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from movements")
    data=cur.fetchall()
    return render_template("view_productmovements.html",datas=data)

@app.route('/report',methods=['GET','POST'])
def report():
    con=sql.connect("inventory.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    data=[]
    if request.method=="POST":
        lname=request.form.get('lname')
        cur.execute("select * from stocks where L_NAME=?",(lname,))
        data=cur.fetchall()
        if not data:
            flash("There is NO STOCK Currently Availabe in this Warehouse","warning")
            return redirect(url_for("report"))

    cur.execute("select *from locations")
    l_data=cur.fetchall()
    return render_template("report.html",locations=l_data,datas=data)

@app.route('/product_report',methods=['GET','POST'])
def product_report():
    con=sql.connect("inventory.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    data=[]
    if request.method=="POST":
        pname=request.form.get('pname')
        cur.execute("select * from stocks where P_NAME=?",(pname,))
        data=cur.fetchall()
        if not data:
            flash("This Product is NOT AVAILABLE in any Warehouses","warning")
            return redirect(url_for("product_report"))

    cur.execute("select *from products")
    p_data=cur.fetchall()
    return render_template("product_report.html",products=p_data,datas=data)


if __name__=='__main__':
    app.secret_key="admin123"
    app.run(debug=True)