from flask import Flask, jsonify, request

from utils import convert_amount, load_rates, normalize_currency

app = Flask(__name__)


@app.route("/")
def root():
    return jsonify({"message": "Currency API"})


@app.route("/rates")
def get_rates():
    base = normalize_currency(request.args.get("base"))
    rates = load_rates(base)
    if not rates:
        return jsonify({"error": "не получилось получить курсы"}), 500
    return jsonify({"base": base or "USD", "rates": rates})


@app.route("/convert")
def convert():
    from_code = normalize_currency(request.args.get("from"))
    to_code = normalize_currency(request.args.get("to"))
    amount_param = request.args.get("amount")
    if not from_code or not to_code or not amount_param:
        return jsonify({"error": "нужно указать from, to и amount"}), 400
    try:
        amount = float(amount_param)
    except ValueError:
        return jsonify({"error": "amount должен быть числом"}), 400
    rates = load_rates(from_code)
    if not rates:
        return jsonify({"error": "не получилось получить курсы"}), 500
    rate = rates.get(to_code)
    if not rate:
        return jsonify({"error": "нет такого курса"}), 404
    result = convert_amount(amount, rate)
    return jsonify({"from": from_code, "to": to_code, "amount": amount, "result": result})


if __name__ == "__main__":
    app.run(debug=True)
