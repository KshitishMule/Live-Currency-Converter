from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "bf2408f600831ffaa97117a7"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

# Fetch all supported currencies once at app start
def get_currency_list():
    url = f"{BASE_URL}/codes"
    response = requests.get(url)
    data = response.json()
    if data.get('result') == 'success':
        return sorted(data['supported_codes'])  # List of [code, name]
    else:
        return []

CURRENCIES = get_currency_list()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]
        amount = float(request.form["amount"])

        response = requests.get(f"{BASE_URL}/latest/{from_currency}")
        data = response.json()

        if data.get("result") == "success":
            rate = data["conversion_rates"].get(to_currency)
            if rate:
                converted = round(amount * rate, 2)
                result = f"✅ {amount} {from_currency} = {converted} {to_currency}"
            else:
                result = f"❌ Currency '{to_currency}' not found."
        else:
            result = "❌ Error fetching exchange rates."

    return render_template("index.html", currencies=CURRENCIES, result=result)

if __name__ == "__main__":
    app.run(debug=True)
