from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from web3 import Web3
import re
from web3.middleware import geth_poa_middleware
from contractinfo import abi, contract_address

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=contract_address, abi=abi)
account = ""

def check(password):
    if len(password) < 12:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        return False
    if re.search(r"password123|qwerty123", password, re.IGNORECASE):
        return False
    return True

@app.route("/", methods=["GET", "POST"])
def index():
    error_message = ""
    if request.method == "POST":
        if request.form["button"] == "Авторизация":
            return redirect(url_for("login"))
        elif request.form["button"] == "Регистрация":
            return redirect(url_for("register"))
    return render_template("index.html", error=error_message)

# Страница регистрации
@app.route("/register", methods=["GET", "POST"])
def register():
    error_message = ""
    if request.method == "POST":
        password = request.form["password"]
        if check(password):
            try:
                account = w3.geth.personal.new_account(password)
                w3.geth.personal.unlock_account("0x21a4B4Da72EAe9E579D8461aB4E729349B39c38C", 1)
                w3.eth.send_transaction({"to": account, "from": "0x21a4B4Da72EAe9E579D8461aB4E729349B39c38C", "value": 100000000000000000000000})
                return render_template("success.html", account=account)
            except Exception as e:
                error_message = "Ошибка регистрации: " + str(e)
        else:
            error_message = "Пароль недостаточно надежный"
    return render_template("register.html", error=error_message)

# Страница авторизации
@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = ""
    if request.method == "POST":
        publicKey = request.form["publicKey"]
        password = request.form["password"]
        try:
            w3.geth.personal.unlock_account(publicKey, password)
            return redirect(url_for("main", account=publicKey))
        except Exception as e:
            error_message = "Ошибка авторизации: " + str(e)
    return render_template("login.html", error=error_message)

# Страница с основными действиями
@app.route("/main", methods=["GET", "POST"])
def main():
    account = request.args.get("account")
    error_message = ""
    if request.method == "POST":
        if request.form["action"] == "Создать недвижимость":
            return redirect(url_for("create_estate", account=account))  # Передача ключа в create_estate
        elif request.form["action"] == "Создать объявление":
            return redirect(url_for("create_ad", account=account))  # Передача ключа в create_ad
        elif request.form["action"] == "Изменить недвижимость":
            return redirect(url_for("change_estate", account=account))  # Передача ключа в change_estate
        elif request.form["action"] == "Изменить объявление":
            return redirect(url_for("change_ad", account=account))  # Передача ключа в change_ad
        elif request.form["action"] == "Купить недвижимость":
            return redirect(url_for("buy_estate", account=account))  # Передача ключа в buy_estate
        elif request.form["action"] == "Вывести деньги":
            return redirect(url_for("withdraw", account=account))  # Передача ключа в withdraw
        elif request.form["action"] == "Пополнить баланс":
            return redirect(url_for("pay", account=account))  # Передача ключа в pay
        elif request.form["action"] == "Просмотреть недвижимость":
            return redirect(url_for("get_estates", account=account))  # Передача ключа в get_estates
        elif request.form["action"] == "Просмотреть объявления":
            return redirect(url_for("get_ad", account=account))  # Передача ключа в get_ad
        elif request.form["action"] == "Проверить баланс контракта":
            return redirect(url_for("get_balance", account=account))  # Передача ключа в get_balance
        elif request.form["action"] == "Проверить баланс аккаунта":
            return redirect(url_for("get_account_balance", account=account))  # Передача ключа в get_account_balance
    return render_template("main.html", account=account, error=error_message)

# Страница создания недвижимости
@app.route("/create_estate", methods=["GET", "POST"])
def create_estate():
    account = request.args.get("account")  # Получение публичного ключа из URL
    error_message = ""
    if request.method == "POST":
        if request.form["action"] == "Создать":
            try:
                address = request.form["address"]
                square = int(request.form["square"])
                type = int(request.form["type"])
                tx = contract.functions.createEstate(address, square, type).transact({
                    'from': account
                })
                error_message = "Недвижимость успешно создана"
            except Exception as e:
                error_message = "Ошибка создания недвижимости: " + str(e)
        else:
            if request.form["action"] == "Назад":
                return redirect(url_for("main", account=account))
    return render_template("create_estate.html", error=error_message)


@app.route("/create_ad", methods=["GET", "POST"])
def create_ad():
    account = request.args.get("account")  # Получение публичного ключа из URL
    error_message = ""
    if request.method == "POST":
        if request.form["action"] == "Создать":
            try:
               price = int(request.form["price"])
               idEstate = int(request.form["idEstate"])
               contract.functions.createAd(price, idEstate).transact({
                   'from': account
               })
               error_message = "Успешное создание объявления"
            except Exception as e:
               error_message = "Ошибка добавления недвижимости: " + str(e)
        else:
            if request.form["action"] == "Назад":
                return redirect(url_for("main", account=account))
    return render_template("create_ad.html", error=error_message)

# Страница изменения недвижимости
@app.route("/change_estate", methods=["GET", "POST"])
def change_estate():
    account = request.args.get("account")  # Получение публичного ключа из URL
    error_message = ""
    if request.method == "POST":
        if request.form["action"] == "Изменить":
            try:
                idEstate = int(request.form["idEstate"])
                contract.functions.updateEstateActive(idEstate).transact({
                    'from': account
                })
                error_message = "Объявление успешно обновлено"
            except Exception as e:
                error_message = "Ошибка обновления недвижимости: " + str(e)
        else:
            if request.form["action"] == "Назад":
                return redirect(url_for("main", account=account))
    return render_template("change_estate.html", error=error_message)

# Страница изменения объявления
@app.route("/change_ad", methods=["GET", "POST"])
def change_ad():
    account = request.args.get("account")  # Получение публичного ключа из URL
    error_message = ""
    if request.method == "POST":
        if request.form["action"] == "Изменить":
            try:
                idAD = int(request.form["idAD"])
                contract.functions.updateAdType(idAD).transact({
                    'from': account
                })
                error_message = "Успешное обновление объявления"
            except Exception as e:
                error_message = "Ошибка обновления объявления: " + str(e)
        else:
            if request.form["action"] == "Назад":
                return redirect(url_for("main", account=account))
    return render_template("change_ad.html", error=error_message)

# Страница покупки недвижимости
@app.route("/buy_estate", methods=["GET", "POST"])
def buy_estate():
    account = request.args.get("account")  # Получение публичного ключа из URL
    error_message = ""
    if request.method == "POST":
        if request.form["action"] == "Купить":
            try:
                idAD = int(request.form["idAD"])
                contract.functions.buyEstate(idAD).transact({
                    'from': account
                })
                error_message = "Недвижимость успешна куплена"
            except Exception as e:
                error_message = "Ошибка покупки недвижимости: " + str(e)
        else:
            if request.form["action"] == "Назад":
                return redirect(url_for("main", account=account))
    return render_template("buy_estate.html", error=error_message)

# Страница вывода денег
@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    account = request.args.get("account")  # Получение публичного ключа из URL
    error_message = ""
    if request.method == "POST":
        if request.form["action"] == "Вывести":
            try:
                amount = int(request.form["amount"])
                if amount > 0 and amount <= w3.eth.get_balance(contract_address):
                    contract.functions.withdraw(amount).transact({
                        'from': account,
                        'value': amount
                    })
                    error_message = "Деньги успешно выведены с баланса контракта"
                else:
                    error_message = "Некорректная сумма для вывода"
            except Exception as e:
                error_message = "Ошибка вывода средств: " + str(e)
        else:
            if request.form["action"] == "Назад":
                return redirect(url_for("main", account=account))
    return render_template("withdraw.html", error=error_message)

# Страница пополнения баланса
@app.route("/pay", methods=["GET", "POST"])
def pay():
    account = request.args.get("account")  # Получение публичного ключа из URL
    error_message = ""
    if request.method == "POST":
        if request.form["action"] == "Пополнить":
            try:
                amount = int(request.form["amount"])
                contract.functions.pay().transact({
                    'from': account,
                    'value': amount
                })
                error_message = "Деньги есть"
            except Exception as e:
                error_message = "Ошибка: " + str(e)
        else:
            if request.form["action"] == "Назад":
                return redirect(url_for("main", account=account))
    return render_template("pay.html", error=error_message)

# Страница просмотра недвижимости
@app.route("/get_estates")
def get_estates():
    account = request.args.get("account")  # Получение публичного ключа из URL
    error_message = ""
    try:
        available_estates = contract.functions.getEstates().call()  # Вызов функции из контракта
        estates = []
        for estate in available_estates:
            estates.append({
                "id": estate[5],
                "address": estate[0],
                "square": estate[1],
                "type": estate[2]
            })
        return render_template("get_estates.html", estates=estates, account=account, error=error_message)
    except Exception as e:
        error_message = "Ошибка получения информации о доступных недвижимостях: " + str(e)
    return render_template("get_estates.html", account=account, error=error_message)

# Страница просмотра объявлений
@app.route("/get_ad", methods=["GET", "POST"])
def get_ad():
    account = request.args.get("account")
    error_message = ""
    if request.method == "POST":
        try:
            open_ads = contract.functions.getOpenAdvertisements().call()  # Вызов правильной функции
            ads = []
            for ad in open_ads:
                ads.append({
                    "id": ad[1],
                    "price": ad[0],
                    "type": ad[5]
                })
            return render_template("get_ad.html", ads=ads, account=account, error=error_message)
        except Exception as e:
            error_message = "Ошибка получения информации о текущих объявлениях: " + str(e)
    return render_template("get_ad.html", account=account, error=error_message)




# Страница проверки баланса контракта
@app.route("/get_balance")
def get_balance():
    account = request.args.get("account")  # Получение публичного ключа из URL
    error_message = ""
    try:
        balance = contract.functions.balances(account).call()  # Вызов правильной функции
        return render_template("get_balance.html", balance=balance, account=account, error=error_message)
    except Exception as e:
        error_message = "Ошибка получения баланса на контракте: " + str(e)
    return render_template("get_balance.html", account=account, error=error_message)

# Страница проверки баланса аккаунта
@app.route("/get_account_balance")
def get_account_balance():
    account = request.args.get("account")  # Получение публичного ключа из URL
    error_message = ""
    try:
        balance = w3.eth.get_balance(account)  # Вызов функции из контракта
        return render_template("get_account_balance.html", balance=balance, account=account, error=error_message)
    except Exception as e:
        error_message = "Ошибка получения баланса на аккаунте: " + str(e)
    return render_template("get_account_balance.html", account=account, error=error_message)


if __name__ == "__main__":
    app.run(debug=True)

#0x9E7868b8f42839562a76cbA12688A4d29ca2Cf82
#Qwerty1111111!