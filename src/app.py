from flask import Flask, render_template
import requests
import os

app = Flask(__name__)
url_API = "https://www.thecocktaildb.com/api/json/v1/1/search.php?f=a"


def guardar_img(file_name, url):
    response = requests.get(url, stream=True)

    root_directory = os.path.dirname(os.path.abspath(__file__))
    static_directory = os.path.join(root_directory, "static/images")
    file_path = os.path.join(static_directory, file_name)

    with open(file_path, "wb") as file:
        for data in response.iter_content():
            file.write(data)

    response.close()


@app.route("/")
def index():
    response = requests.get(url_API)
    response_json = response.json()
    drinks = response_json.get("drinks", "")

    data = []
    for drink in drinks:
        data_drink = [drink.get("strDrink", ""),
                      drink.get("strCategory", ""),
                      drink.get("strGlass", "")]
        data.append(data_drink)

    return render_template("index.html", data=data)


@app.route("/detalles/<nombre>")
def detalle(nombre):
    response = requests.get(url_API)
    response_json = response.json()
    drinks = response_json.get("drinks", "")

    for drink in drinks:
        if drink.get("strDrink", "") == nombre:
            break
    
    data = [drink.get("strDrink", ""),
            drink.get("strCategory", ""),
            drink.get("strGlass", ""),
            drink.get("strInstructions", ""),
            drink.get("strIngredient1", ""),
            drink.get("strIngredient2", ""),
            drink.get("strIngredient3", ""),
            drink.get("strIngredient4", ""),
            drink.get("strIngredient5", "")]
    
    guardar_img(nombre + ".jpg", drink.get("strDrinkThumb"))

    return render_template("detalles.html", data=data, src=nombre + ".jpg")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
