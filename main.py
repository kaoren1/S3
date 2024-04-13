from web3 import Web3
from web3.middleware import geth_poa_middleware
from contractinfo import abi, contract_address

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

def main():
    print(f"Баланс первого аккаунта: {w3.eth.get_balance('0xb6C02cfCc416017eEEC2F480a29203d3719CFe47')}")
    print(f"Баланс второго аккаунта: {w3.eth.get_balance('0x21a4B4Da72EAe9E579D8461aB4E729349B39c38C')}")
    print(f"Баланс третьего аккаунта: {w3.eth.get_balance('0x10E224409764ab398dc2959C3192bE79A29f9FCd')}")
    print(f"Баланс четвертого аккаунта: {w3.eth.get_balance('0x744faF7d8a18DC92bE688a33f6eCC61758CAB812')}")
    print(f"Баланс пятого аккаунта: {w3.eth.get_balance('0x148561CC62fD88167460D84f5671AF7b530Fba79')}")

if __name__ == '__main__':
    main()