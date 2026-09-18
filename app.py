from flask import Flask, render_template
from models import db, Animal, Crop
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///farm.db"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def dashboard():
    stats = {
        "total_animals": Animal.query.count(),
        "sick_animals": Animal.query.filter_by(health_status="Sick").count(),
        "total_crops": Crop.query.count(),
        "active_staff": 0,
    }
    return render_template("dashboard.html", stats=stats)


@app.route("/animals")
def animals():
    all_animals = Animal.query.order_by(Animal.id.desc()).all()
    return render_template("animals/animals.html", animals=all_animals)

@app.route("/animals/add", methods=["GET", "POST"])
def add_animal():
    if request.method == "POST":
        birth_date = None
        if request.form.get("birth_date"):
            birth_date = datetime.strptime(request.form["birth_date"], "%Y-%m-%d").date()

        animal = Animal(
            name=request.form["name"],
            species=request.form["species"],
            breed=request.form.get("breed"),
            gender=request.form.get("gender"),
            birth_date=birth_date,
            weight_kg=float(request.form["weight_kg"]) if request.form.get("weight_kg") else None,
            health_status=request.form.get("health_status", "Healthy"),
            notes=request.form.get("notes"),
        )
        db.session.add(animal)
        db.session.commit()
        return redirect(url_for("animals"))

    return render_template("animals/add_animal.html")
@app.route("/animals/<int:animal_id>/edit", methods=["GET", "POST"])
def edit_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    if request.method == "POST":
        birth_date = None
        if request.form.get("birth_date"):
            birth_date = datetime.strptime(request.form["birth_date"], "%Y-%m-%d").date()

        animal.name = request.form["name"]
        animal.species = request.form["species"]
        animal.breed = request.form.get("breed")
        animal.gender = request.form.get("gender")
        animal.birth_date = birth_date
        animal.weight_kg = float(request.form["weight_kg"]) if request.form.get("weight_kg") else None
        animal.health_status = request.form.get("health_status", "Healthy")
        animal.notes = request.form.get("notes")
        db.session.commit()
        return redirect(url_for("animals"))

    return render_template("animals/add_animal.html", animal=animal)
@app.route("/animals/<int:animal_id>/delete", methods=["POST"])
def delete_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    db.session.delete(animal)
    db.session.commit()
    return redirect(url_for("animals"))

@app.route("/crops")
def crops():
    all_crops = Crop.query.order_by(Crop.id.desc()).all()
    return render_template("crops/crops.html", crops=all_crops)
@app.route("/crops/add", methods=["GET", "POST"])
def add_crop():
    if request.method == "POST":
        planting_date = None
        if request.form.get("planting_date"):
            planting_date = datetime.strptime(request.form["planting_date"], "%Y-%m-%d").date()

        harvest_date = None
        if request.form.get("expected_harvest_date"):
            harvest_date = datetime.strptime(request.form["expected_harvest_date"], "%Y-%m-%d").date()

        crop = Crop(
            name=request.form["name"],
            field_location=request.form.get("field_location"),
            area_acres=float(request.form["area_acres"]) if request.form.get("area_acres") else None,
            planting_date=planting_date,
            expected_harvest_date=harvest_date,
            status=request.form.get("status", "Planted"),
            yield_amount_kg=float(request.form["yield_amount_kg"]) if request.form.get("yield_amount_kg") else None,
            notes=request.form.get("notes"),
        )
        db.session.add(crop)
        db.session.commit()
        return redirect(url_for("crops"))

    return render_template("crops/add_crop.html", crop=None)


@app.route("/crops/<int:crop_id>/edit", methods=["GET", "POST"])
def edit_crop(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    if request.method == "POST":
        planting_date = None
        if request.form.get("planting_date"):
            planting_date = datetime.strptime(request.form["planting_date"], "%Y-%m-%d").date()

        harvest_date = None
        if request.form.get("expected_harvest_date"):
            harvest_date = datetime.strptime(request.form["expected_harvest_date"], "%Y-%m-%d").date()

        crop.name = request.form["name"]
        crop.field_location = request.form.get("field_location")
        crop.area_acres = float(request.form["area_acres"]) if request.form.get("area_acres") else None
        crop.planting_date = planting_date
        crop.expected_harvest_date = harvest_date
        crop.status = request.form.get("status", "Planted")
        crop.yield_amount_kg = float(request.form["yield_amount_kg"]) if request.form.get("yield_amount_kg") else None
        crop.notes = request.form.get("notes")
        db.session.commit()
        return redirect(url_for("crops"))

    return render_template("crops/add_crop.html", crop=crop)


@app.route("/crops/<int:crop_id>/delete", methods=["POST"])
def delete_crop(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    db.session.delete(crop)
    db.session.commit()
    return redirect(url_for("crops"))
if __name__ == "__main__":
    app.run(debug=True)