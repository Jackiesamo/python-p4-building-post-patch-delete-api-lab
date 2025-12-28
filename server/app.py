
#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# ----------------------
# HOME
# ----------------------
@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

# ----------------------
# GET bakeries
# ----------------------
@app.route('/bakeries', methods=['GET'])
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(bakeries, 200)

# ----------------------
# GET + PATCH bakery
# ----------------------
@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.get(id)

    if not bakery:
        return make_response({"error": "Bakery not found"}, 404)

    if request.method == 'PATCH':
        data = request.form  # ✅ FIX

        if 'name' in data:
            bakery.name = data['name']

        db.session.commit()
        return make_response(bakery.to_dict(), 200)

    return make_response(bakery.to_dict(), 200)

# ----------------------
# GET baked goods by price
# ----------------------
@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_serialized = [bg.to_dict() for bg in baked_goods]
    return make_response(baked_goods_serialized, 200)

# ----------------------
# GET most expensive baked good
# ----------------------
@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(baked_good.to_dict(), 200)

# ----------------------
# POST baked good
# ----------------------
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form  # ✅ FIX

    baked_good = BakedGood(
        name=data['name'],
        price=data['price'],
        bakery_id=data['bakery_id']
    )

    db.session.add(baked_good)
    db.session.commit()

    return make_response(baked_good.to_dict(), 201)

# ----------------------
# DELETE baked good
# ----------------------
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if not baked_good:
        return make_response({"error": "Not found"}, 404)

    db.session.delete(baked_good)
    db.session.commit()

    return make_response({}, 200)

# ----------------------
if __name__ == '__main__':
    app.run(port=5555, debug=True)
