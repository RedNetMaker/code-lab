import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse

from flask import request

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.nodes = set()

        # Создание блока genesis
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Добавление новго узла в список узлов
        :param address: <str> Адрес узла'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        Проверка цепочки блоков на валидность
        :param chain: <list> Цепочка блоков
        :return: <bool> True если цепочка валидна, False если нет
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            # Проверка на правильность хэша
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Проверка на доказательство работы
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        Это алгоритм консенсуса: используйте этот алгоритм для определения правильной цепочки
        :return: <bool> True если цепочка заменена, False если нет
        """

        neighbours = self.nodes
        new_chain = None

        # Ищем цепочки, которые длинее нашей
        max_length = len(self.chain)

        # Сбор и проверка цепочек со всех узлов сети
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Проверка, не увеличилась ли длина и действительна ли цепочка
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Замена цепочки, если обнаружена действительная цепочка, которая длинее нашей
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash=None):
        """
        Создание нового блока и добавление его в цепочку
        :param proof: <int> Доказательство работы
        :param previous_hash: <str> Хеш предыдущего блока
        :return: <dict> Новый блок
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Сброс текущих транзакций
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Добавление новой транзакции в список текущих транзакций
        :param sender: <str> Отправитель
        :param recipient: <str> Получатель
        :param amount: <int> Сумма
        :return: <int> Индекс нового блока
        """
        
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Создание SHA-256 хеша блока
        :param block: <dict> Блок
        :return: <str> Хеш блока
        """

        # Мы должны убедиться, что словарь упорядочен, чтобы хеш был одинаковым для одного и того же блока
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Алгоритм Proof of Work
        - Найдите число p' такое, что hash(pp') содержит 4 ведущих нуля
        - p - предыдущее доказательство, p' - новое доказательство
        :param last_proof: <int> Доказательство работы предыдущего блока
        :return: <int> Доказательство работы
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Проверка: hash(last_proof, proof) содержит 4 ведущих нуля
        :param last_proof: <int> Доказательство работы предыдущего блока
        :param proof: <int> Доказательство работы
        :return: <bool> True если доказательство работы верно, False если нет
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

# block = {
#     'index': 1,
#     'timestamp': 1717756800,
#     'transactions': [
#         {
#             'sender': '0',
#             'recipient': '1',
#             'amount': 1,
#         }
#     ],
#     'proof': 100,
#     'previous_hash': '1234567890',
# }