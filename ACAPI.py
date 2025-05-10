import requests
import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Paths to the relevant JSON files for items
GAMEPLAY_ITEMS_FILE = "econ_gameplay_items.json"
AVATAR_ITEMS_FILE = "econ_avatar_items.json"
MINING_ORES_FILE = "econ_mining_ores.json"
RESEARCH_NODES_FILE = "econ_research_nodes.json"
STASH_UPGRADES_FILE = "econ_stash_upgrades.json"
METADATA_FILE = "metadata.json"

# Load JSON data from file
def load_json_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return {}

# Load all the required JSON files related to items
gameplay_items = load_json_data(GAMEPLAY_ITEMS_FILE)
avatar_items = load_json_data(AVATAR_ITEMS_FILE)
mining_ores = load_json_data(MINING_ORES_FILE)
research_nodes = load_json_data(RESEARCH_NODES_FILE)
stash_upgrades = load_json_data(STASH_UPGRADES_FILE)
metadata = load_json_data(METADATA_FILE)

# Integrity Check (bypass logic)
def integrity_check():
    IntegrityCheck = requests.get("https://ac-main.b-cdn.net/data/game-data-prod.zip")
    if IntegrityCheck.ok:
        return {
            "PhotonAppID": 125,
            "PhotonVoiceID": 126,
            "HardCurrency": 1000,
            "SoftCurrency": 5000,
            "RP": 250
        }
    else:
        return {"error": "Integrity check failed"}

@app.route("/v2/storage/integrity-check", methods=["GET"])
def check_integrity():
    data = integrity_check()
    return jsonify(data)

@app.route("/v2/storage/econ_gameplay_items", methods=["GET"])
def get_gameplay_items():
    return jsonify(gameplay_items)

@app.route("/v2/storage/econ_avatar_items", methods=["GET"])
def get_avatar_items():
    return jsonify(avatar_items)

@app.route("/v2/storage/econ_mining_ores", methods=["GET"])
def get_mining_ores():
    return jsonify(mining_ores)

@app.route("/v2/storage/econ_research_nodes", methods=["GET"])
def get_research_nodes():
    return jsonify(research_nodes)

@app.route("/v2/storage/econ_stash_upgrades", methods=["GET"])
def get_stash_upgrades():
    return jsonify(stash_upgrades)

@app.route("/v2/storage/metadata", methods=["GET"])
def get_metadata():
    return jsonify(metadata)


user_inventory = {
    "user123": {
        "hard_currency": 1000,
        "soft_currency": 5000,
        "rp": 250,
        "items": []
    }
}

@app.route("/v2/storage/user/<user_id>/items", methods=["GET", "POST"])
def manage_user_items(user_id):
    if user_id not in user_inventory:
        return jsonify({"error": "User not found"}), 404
    
    if request.method == "GET":
        return jsonify(user_inventory[user_id]["items"])
    
    if request.method == "POST":
        item_data = request.json
        user_inventory[user_id]["items"].append(item_data)
        return jsonify({"status": "item added"}), 200

# Start the server
if __name__ == "__main__":
    app.run(debug=True)
