import subprocess, csv

from flask import Flask, render_template, request, jsonify

from helpers import get_products, get_product_by_sku, insertCsvToMySQL
from constatns import scripts

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        insertCsvToMySQL()
    return render_template("index.html", scripts=scripts)


@app.route("/run_script", methods=["POST"])
def run_script():
    script_filename = request.json["script_filename"]
    script_path = f"scripts/{script_filename}"

    script = next((s for s in scripts if s["filename"] == script_filename), None)
    if script:
        try:
            subprocess.run(["python", script_path], check=True)
            script["status"] = "Finished successfully"
        except subprocess.CalledProcessError:
            script["status"] = "There is error with this script"
    else:
        return jsonify({"message": "Script not found."}), 404

    return jsonify({"message": "Script execution completed.", "script": script}), 201


@app.route("/second", methods=["POST", "GET"])
def second_page():
    runned_scripts = request.form.get("scripts").split(",")
    print(runned_scripts)
    context = []

    for script in runned_scripts:
        context.append(get_products(script))

    return render_template("second.html", context=context)


@app.route("/next", methods=["POST", "GET"])
def results():
    data = []
    for i in request.form:
        file_name = i.split("|")[0]
        sku = i.split("|")[-1]
        data.append(get_product_by_sku(file_name, sku))

    file_path = "data/output.csv"

    keys = data[0].keys()

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    return render_template("results.html")


if __name__ == "__main__":
    app.run(debug=True)
