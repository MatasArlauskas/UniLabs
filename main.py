import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# API konfigūracija
API_KEY = "ux8u1HjyN6pxKkkq9ZcycDPNo6bzr027"
API_URL = "https://api.apilayer.com/exchangerates_data/latest"

def get_exchange_rates(base="EUR", symbols=None):
    """Gauna valiutų kursų duomenis iš API"""

    headers = {
        "apikey": API_KEY
    }

    params = {
        "base": base
    }

    # Pridėti simbolius, jei jie nurodyti
    if symbols:
        params["symbols"] = symbols

    # Išsiųsti GET užklausą į API
    response = requests.get(API_URL, headers=headers, params=params)

    # Patikrinti ar užklausa sėkminga
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API užklausa nepavyko, kodas: {response.status_code}", "message": response.text}


def save_to_file(data, filename="api.json"):
    """Išsaugo JSON duomenis į nurodytą failą"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Duomenys išsaugoti į {filename}")


@app.route('/', methods=['GET', 'POST'])
def index():
    """Pagrindinis puslapis, kuris atvaizduoja API duomenis"""

    # Numatytosios reikšmės
    base = "EUR"
    symbols = "USD,GBP,JPY,AUD,CAD,CHF,CNY,SEK,NZD,PLN"

    # Jei forma pateikta, naudoti vartotojo reikšmes
    if request.method == 'POST':
        base = request.form.get('base', base)
        symbols = request.form.get('symbols', symbols)

    # Gauti duomenis
    data = get_exchange_rates(base, symbols)

    # Išsaugoti duomenis į failą
    save_to_file(data)

    # Spausdinti duomenis konsolėje
    print("API duomenys:")
    print(json.dumps(data, indent=4))

    # Perduoti duomenis į šabloną
    return render_template('index.html', data=data, base=base, symbols=symbols)


if __name__ == '__main__':
    # Užtikrinti, kad templates katalogas egzistuoja
    import os
    if not os.path.exists('templates'):
        os.makedirs('templates')

    # Sukurti HTML šabloną, jei jo dar nėra
    if not os.path.exists('templates/index.html'):
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html lang="lt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Valiutų kursų API</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f7fa;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            padding: 30px;
        }
        .form-container {
            margin-bottom: 30px;
            padding: 20px;
            background-color: #f1f5f9;
            border-radius: 8px;
        }
        .form-row {
            display: flex;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }
        .form-group {
            flex: 1;
            min-width: 200px;
            margin-right: 20px;
            margin-bottom: 15px;
        }
        .form-group:last-child {
            margin-right: 0;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #455a64;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 12px 20px;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #2980b9;
        }
        .result-container {
            background-color: #fff;
            border-radius: 8px;
        }
        .rates-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .rates-table th, .rates-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e1e5e9;
        }
        .rates-table th {
            background-color: #f1f5f9;
            font-weight: 600;
            color: #455a64;
        }
        .rates-table tr:hover {
            background-color: #f9fafb;
        }
        .info-row {
            display: flex;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        .info-item {
            flex: 1;
            min-width: 200px;
            padding: 10px;
            background-color: #e3f2fd;
            border-radius: 5px;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        .info-item:last-child {
            margin-right: 0;
        }
        .error-message {
            background-color: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 5px solid #c62828;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Valiutų kursų API</h1>

        <div class="form-container">
            <form method="POST">
                <div class="form-row">
                    <div class="form-group">
                        <label for="base">Bazinė valiuta:</label>
                        <input type="text" id="base" name="base" value="{{ base }}" placeholder="Pvz.: EUR, USD">
                    </div>
                    <div class="form-group">
                        <label for="symbols">Valiutos (atskirtos kableliais):</label>
                        <input type="text" id="symbols" name="symbols" value="{{ symbols }}" placeholder="Pvz.: USD,GBP,JPY">
                    </div>
                </div>
                <button type="submit">Gauti valiutų kursus</button>
            </form>
        </div>

        <div class="result-container">
            {% if data %}
                {% if data.get('error') %}
                    <div class="error-message">
                        <h3>Klaida:</h3>
                        <p>{{ data.error }}</p>
                        {% if data.get('message') %}
                            <p>{{ data.message }}</p>
                        {% endif %}
                    </div>
                {% else %}
                    <div class="info-row">
                        <div class="info-item">
                            <strong>Bazinė valiuta:</strong> {{ data.base }}
                        </div>
                        <div class="info-item">
                            <strong>Data:</strong> {{ data.date }}
                        </div>
                        <div class="info-item">
                            <strong>Paskutinis atnaujinimas:</strong> {{ data.timestamp }}
                        </div>
                    </div>

                    <h2>Valiutų kursai</h2>
                    {% if data.rates %}
                        <table class="rates-table">
                            <thead>
                                <tr>
                                    <th>Valiuta</th>
                                    <th>Kursas</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for currency, rate in data.rates.items() %}
                                <tr>
                                    <td>{{ currency }}</td>
                                    <td>{{ rate }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    {% else %}
                        <p>Nerasta valiutų kursų duomenų.</p>
                    {% endif %}
                {% endif %}
            {% else %}
                <p>Nėra duomenų.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>''')

    # Paleisti Flask aplikaciją
    app.run(debug=True)

