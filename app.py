from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Sample data for clothing items
clothing_items = [
    {"id": 1, "name": "Casual T-Shirt", "category": "Tops", "price": 150, "available": True, "size": ["S", "M", "L"], "color": "Blue", "stock": 25},
    {"id": 2, "name": "Formal Shirt", "category": "Shirts", "price": 250, "available": True, "size": ["M", "L", "XL"], "color": "White", "stock": 10},
    {"id": 3, "name": "Jeans", "category": "Bottoms", "price": 300, "available": True, "size": ["M", "L", "XL"], "color": "Black", "stock": 20},
    {"id": 4, "name": "Jacket", "category": "Outerwear", "price": 450, "available": False, "size": ["L", "XL"], "color": "Grey", "stock": 0},
    {"id": 5, "name": "Summer Dress", "category": "Dresses", "price": 350, "available": True, "size": ["S", "M"], "color": "Yellow", "stock": 15},
    {"id": 6, "name": "Hoodie", "category": "Outerwear", "price": 400, "available": True, "size": ["M", "L", "XL"], "color": "Red", "stock": 18},
    {"id": 7, "name": "Cargo Pants", "category": "Bottoms", "price": 320, "available": True, "size": ["M", "L"], "color": "Green", "stock": 12},
    {"id": 8, "name": "Blazer", "category": "Outerwear", "price": 550, "available": True, "size": ["M", "L"], "color": "Black", "stock": 8},
    {"id": 9, "name": "Tank Top", "category": "Tops", "price": 100, "available": True, "size": ["S", "M"], "color": "White", "stock": 30},
    {"id": 10, "name": "Sweatpants", "category": "Bottoms", "price": 200, "available": True, "size": ["M", "L", "XL"], "color": "Grey", "stock": 22}
]

# Helper function to get a new ID
def get_new_id():
    if clothing_items:
        return max(item["id"] for item in clothing_items) + 1
    return 1

# Clothing list endpoint with Create option
class ClothingList(Resource):
    def get(self):
        return {"error": False, "message": "success", "count": len(clothing_items), "items": clothing_items}

# AddClothing resource
class AddClothing(Resource):
    def post(self):
        data = request.json
        new_id = get_new_id()
        
        new_item = {
            "id": new_id,
            "name": data.get("name"),
            "category": data.get("category"),
            "price": data.get("price"),
            "available": data.get("available", True),
            "size": data.get("size", ["M"]),
            "color": data.get("color", "Unknown"),
            "stock": data.get("stock", 0)
        }
        clothing_items.append(new_item)
        
        return {"error": False, "message": "Item created successfully", "item": new_item}, 201

# Clothing detail endpoint with Read, Update, and Delete options
class ClothingDetail(Resource):
    def get(self, item_id):
        item = next((item for item in clothing_items if item["id"] == item_id), None)
        if not item:
            return {"error": True, "message": "Item not found"}, 404
        return {"error": False, "message": "success", "item": item}

# UpdateClothing resource
class UpdateClothing(Resource):
    def put(self, item_id):
        data = request.json
        item = next((item for item in clothing_items if item["id"] == item_id), None)
        if not item:
            return {"error": True, "message": "Item not found"}, 404
        
        # Update item data
        item.update({
            "name": data.get("name", item["name"]),
            "category": data.get("category", item["category"]),
            "price": data.get("price", item["price"]),
            "available": data.get("available", item["available"]),
            "size": data.get("size", item["size"]),
            "color": data.get("color", item["color"]),
            "stock": data.get("stock", item["stock"])
        })
        
        return {"error": False, "message": "Item updated successfully", "item": item}

# DeleteClothing resource
class DeleteClothing(Resource):
    def delete(self, item_id):
        global clothing_items
        clothing_items = [item for item in clothing_items if item["id"] != item_id]
        
        return {"error": False, "message": "Item deleted successfully"}

# Registering resources with endpoints
api.add_resource(ClothingList, "/clothing")  # Untuk GET
api.add_resource(AddClothing, '/clothing/add')  # Untuk POST
api.add_resource(ClothingDetail, "/clothing/<int:item_id>")  # Untuk GET
api.add_resource(UpdateClothing, '/clothing/update/<int:item_id>')  # Untuk PUT
api.add_resource(DeleteClothing, '/clothing/delete/<int:item_id>')  # Untuk DELETE

if __name__ == "__main__":
    app.run(debug=True)
