from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

class User():
    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password
class Product:
    def __init__(self, id, name, description, category, quantity, price, manufacturer, supplier):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.quantity = quantity
        self.price = price
        self.manufacturer = manufacturer
        self.supplier = supplier

@app.route("/")
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            return render_template("index.html", logged_in=True)
        else:
            return render_template("index.html", logged_in=False)
    else:
        return render_template("index.html", logged_in=False)
def load_users():
    with open('users.csv', 'r') as file:
        lines = file.readlines()
        users = []
        for line in lines:
            parts = line.strip().split(',')
            user_id = int(parts[0])
            username = parts[1]
            password = parts[2]
            users.append(User(user_id, username,password))
        return users
    
def load_products():
    try:
        with open("products.csv", 'r') as file:
            lines = file.readlines()
            products = []
            for line in lines:
                parts = line.strip().split(',')
                product_id = int(parts[0])
                name = parts[1]
                description = parts[2]
                category = parts[3]
                quantity = int(parts[4])
                price = float(parts[5])
                manufacturer = parts[6]
                supplier = parts[7]
                products.append(Product(product_id, name, description, category, quantity, price, manufacturer, supplier))
            return products
    except FileNotFoundError:
        return []

def save_products(products):
    with open("products.csv", 'w') as file:
        for product in products:
            file.write(f"{product.id},{product.name},{product.description},{product.category},{product.quantity},{product.price},{product.manufacturer},{product.supplier}\n")


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if validate_user(username, password):
        print(True)
        return redirect('/home')
    return render_template('login.html')


def validate_user(username, password):
    print('user input',username)
    print('user input',password)
    with open('users.csv', 'r') as file:
        lines = file.readlines()
        for line in lines:
            print('row content',line)
            parts = line.strip().split(',') 
            if parts[1] == username and parts[2] == password:
                return True
    return False

@app.route('/users')
def users():   
    global users
    users = load_users()
    return render_template('users.html', users=users)
@app.route('/home')
def home():
    return render_template('home.html', redirect_from=request.args.get('redirect_from', ''))

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    global products
    products = load_products()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        quantity = int(request.form.get('quantity'))
        price = float(request.form.get('price'))
        manufacturer = request.form.get('manufacturer')
        supplier = request.form.get('supplier')
        product_id = len(products) + 1
        new_product = Product(product_id, name, description, category, quantity, price, manufacturer, supplier)
        products.append(new_product)
        save_products(products) 
        return redirect(url_for('home', redirect_from='inventory'))
    
    return render_template('inventory.html', products=products)

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    global products
    product = next((p for p in products if p.id == product_id), None)
    
    if request.method == 'POST' and product:
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.category = request.form.get('category')
        product.quantity = int(request.form.get('quantity'))
        product.price = float(request.form.get('price'))
        product.manufacturer = request.form.get('manufacturer')
        product.supplier = request.form.get('supplier')
        save_products(products)
        return redirect(url_for('home', redirect_from='inventory'))
    
    return render_template('edit-product.html', product=product)

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    global products
    products = [product for product in products if product.id != product_id]
    save_products(products)
    return redirect(url_for('home', redirect_from='inventory')) 



def save_users():
    with open('users.csv', 'w', newline='') as file:
        writer = csv.writer(file) 
        for user in users:
            writer.writerow([user.id, user.username,user.password])

@app.route('/users')
def users_list():
    global users
    users = load_users()
    return render_template('users.html', users=users)

@app.route('/create_user', methods=['POST'])
def create_user():
    global users
    username = request.form.get('username')
    password = request.form.get('password')
    user_id = len(users) + 1
    new_user = User(user_id, username,password)
    users.append(new_user)
    save_users()
    return redirect(url_for('home', redirect_from='users'))

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    global users
    users = [user for user in users if user.id != user_id]
    save_users()
    return redirect(url_for('home', redirect_from='users')) 

if __name__ == "__main__":
    app.run(debug=True)
