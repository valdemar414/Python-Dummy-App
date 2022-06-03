from flask import Flask, render_template, request, redirect, url_for
from models import db, PublicItem

app = Flask(__name__, template_folder="templates")
db.init_app(app)
db.create_all(app=app)

@app.route("/")
def index():
    return render_template("index.html", items=PublicItem.query.all())

@app.route("/create_item", methods=["GET", "POST"])
def create_item():
    if request.method == "GET":
        return render_template("create_item.html")
    if request.method == "POST":
        attrs = request.form
        item = PublicItem(**attrs)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for("list_items"))

@app.route("/list_items")
def list_items():
    items=PublicItem.query.all()
    empty = False
    if len(items) == 0:
        empty = True
    ctx = {
        "items": items,
        "empty": empty
    }
    return render_template("list_items.html", **ctx)

@app.route("/delete/item/<id>", methods=["POST"])
def delete_item(id):
    item = PublicItem.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("list_items"))

@app.route("/management")
def management():
    return "Management Page"

if __name__ == "__main__":
    app.run()
