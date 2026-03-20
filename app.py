from flask import Flask, render_template, request, abort, send_from_directory
import json
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load products
PRODUCTS_DIR = "products"
products = []

def load_products():
    global products
    products = []
    for filename in os.listdir(PRODUCTS_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(PRODUCTS_DIR, filename), "r") as f:
                products.append(json.load(f))
    print(f"Loaded {len(products)} products")

load_products()

# Homepage
@app.route("/")
def home():
    return send_from_directory('static', 'index.html')

# Search page
@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    results = [
        p for p in products
        if query in p["name"].lower() or query in p["description"].lower()
    ]
    return render_template("search.html", query=request.args.get("q", ""), results=results)

# Dynamic product page
@app.route("/product/<int:product_id>")
def product_page(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        abort(404)
    return render_template("product.html", product=product)

if __name__ == "__main__":
    app.run(debug=True)