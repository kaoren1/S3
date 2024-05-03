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

def register():
    try:
        account_created = False
        password = input("Введите пароль: ")
        while not account_created:
            if check(password):
                account = w3.geth.personal.new_account(password)
                w3.geth.personal.unlock_account("0x21a4B4Da72EAe9E579D8461aB4E729349B39c38C", "1")
                w3.eth.send_transaction(
                    {"to": account, "from": "0x21a4B4Da72EAe9E579D8461aB4E729349B39c38C", "value": 100000000000000000000000})
                print(f"Публичный ключ: {account}")
                account_created = True
                break
            else:
                print("Пароль недостаточно надежный")
                password = input("Введите пароль: ")
    except Exception as e:
        print("Ошибка регистрации: ", e)


def authorize():
    try:
        global account
        publicKey = input("Введите публичный ключ: ")
        password = input("Введите пароль: ")
        w3.geth.personal.unlock_account(publicKey, password)
        account = publicKey
        print("Авторизация успешна!\n")
        return True
    except Exception as e:
        print("Ошибка авторизации. Проверьте публичный ключ и пароль." , e)
        return False

def createEstate():
    try:
        address = input("Введите адрес: ")
        square = int(input("Введите площадь: "))
        type = int(input("Введите один из типо недвижимости:  1. House, 2. Flat, 3. Loft, 4. Dacha : "))
        tx = contract.functions.createEstate(address, square, type).transact({
            'from': account
        })
        print("Недвижимость успешно создана")

    except Exception as e:
        print("Ошибка создания недвижимости", e)

def createAD():
    try:
        price = int(input("Введите цену: "))
        idEstate = int(input("Введите номер недвижимости: "))

        contract.functions.createAd(price, idEstate).transact({
            'from': account
        })
        print("Успешное создание объявления")
    except Exception as e:
        print("Ошибка добавления недвижимости: ", e)

def changeEstate():
    try:
        idEstate = int(input("Введите номер недвижимости: "))
        contract.functions.updateEstateActive(idEstate).transact({
            'from': account
        })
        print("Объявление успешно обновлено")
    except Exception as e:
        print("Ошибка обновления недвижимости: ", e)

def changeAD():
    try:
        idAD = int(input("Введите номер объявления: "))
        contract.functions.updateAdType(idAD).transact({
            'from': account
        })
        print("Успешное обновление объявления")
    except Exception as e:
        print("Ошибка обновления объявления: ", e)

def buyEstate():
    try:
        idAD = int(input("Введите номер объявления: "))
        contract.functions.buyEstate(idAD).transact({
            'from': account
        })
        print("Недвижимость успешна куплена")
    except Exception as e:
        print("Ошибка покупки недвижимости: ", e)

def withdraw():
    try:
        amount = int(input("Введите количество средств: "))
        if(amount > 0) and (amount <= w3.eth.get_balance(contract_address)):
            contract.functions.withdraw(amount).transact({
            'from': account,
            'value': amount
            })
        print("Деньги успешно выведены с баланса контракта")
    except Exception as e:
        print("Ошибка вывода средств: ", e)


def pay():
    try:
        amount = int(input("Введите количество средств: "))
        contract.functions.pay().transact({
                'from': account,
                'value': amount
            })
        print("Деньги есть")
    except Exception as e:
        print("Ошибка: ", e)

def getEstates():
    try:
        available_estates = contract.functions.getAvailableEstates().call()
        for estate in available_estates:
            print(f"ID: {estate[5]}, Адрес: {estate[0]}, Площадь: {estate[1]}, Тип: {estate[2]}")
    except Exception as e:
        print("Ошибка получения информации о доступных недвижимостях: ", e)
def getAD():
    try:
        open_ads = contract.functions.getOpenAdvertisements().call()
        for ad in open_ads:
            print(f"ID: {ad[1]}, Цена: {ad[0]}, Тип объявления: {ad[5]}")
    except Exception as e:
        print("Ошибка получения информации о текущих объявлениях: ", e)
def getBalance(account):
    try:
        balance = contract.functions.balances(account).call()
        print(f"Баланс на контракте для {account}: {balance}")
    except Exception as e:
        print("Ошибка получения баланса на контракте: ", e)
def getAccountBalance(account):
    try:
        balance = w3.eth.get_balance(account)
        print(f"Баланс на аккаунте {account}: {balance}")
    except Exception as e:
        print("Ошибка получения баланса на аккаунте: ", e)

def main():
    print("Выберите действие: \n1. Авторизация \n2. Регистрация \n3. Выход")
    choise0 = int(input())
    while choise0 != 3:
        if (choise0 == 1):
            if(authorize()):
                print("Выберите действие: \n1. Создание недвижимости \n2. Создание объявления \n3. Измененее статуса недвижимости \n4. Изменение статуса объявления \n5. Покупка недвижимости \n6. Вывод средств \n7. Получение информации \n8. Пополнить баланс")
                choise1 = int(input())
                while choise1 != 9:
                    match (choise1):
                        case 1:
                            createEstate()
                        case 2:
                            createAD()
                        case 3:
                            changeEstate()
                        case 4:
                            changeAD()
                        case 5:
                            buyEstate()
                        case 6:
                            withdraw()
                        case 7:
                            print("Выберите действие: \n1. Информация о доступных недвижимостях \n2. Информация о текущих объявлениях \n3. Информация о балансе на смарт-контркате \n4. Посмотреть баланс аккаунта")
                            choise2 = int(input())
                            match choise2:
                                case 1:
                                    getEstates()
                                case 2:
                                    getAD()
                                case 3:
                                    getBalance(account)
                                case 4:
                                    getAccountBalance(account)
                        case 8:
                            pay()
                        case 9:
                            exit(0)
                    print("Выберите действие: \n1. Создание недвижимости \n2. Создание объявления \n3. Измененее статуса недвижимости \n4. Изменение статуса объявления \n5. Покупка недвижимости \n6. Вывод средств \n7. Получение информации \n8. Пополнить баланс")
                    choise1 = int(input())
        elif  (choise0 == 2):
            register()



if __name__ == '__main__':
    main()

#0x768A042bf04E6e0C7f884A92B062ed117215cf25
#Qwerty111111!
#0x9E7868b8f42839562a76cbA12688A4d29ca2Cf82
#Qwerty1111111!