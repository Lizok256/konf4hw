import unittest
import os
import struct
import csv
from Interpreter import Interpreter  # Предполагается, что ваш код сохранен в файле interpreter.py

class TestInterpreter(unittest.TestCase):

    def setUp(self):
        # Создаем временные файлы для тестирования
        self.binary_file = 'test_binary.bin'
        self.result_file = 'test_result.csv'
        self.memory_range = (0, 256)

    def tearDown(self):
        # Удаляем временные файлы после тестов
        if os.path.exists(self.binary_file):
            os.remove(self.binary_file)
        if os.path.exists(self.result_file):
            os.remove(self.result_file)

    def test_execute_load_const(self):
        # Создаем бинарный файл с командой LOAD_CONST
        with open(self.binary_file, 'wb') as f:
            # Команда LOAD_CONST 10 в регистр 0
            f.write(struct.pack("BBBBBB", 10, 10, 0, 0, 0, 0))  # opcode 10, op1=10, op2=0

        interpreter = Interpreter(self.binary_file, self.result_file, self.memory_range)
        interpreter.run()

        # Проверяем, что значение в памяти по адресу 0 равно 10
        with open(self.result_file, mode='r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Пропускаем заголовок
            result = dict(csv_reader)

        self.assertEqual(int(result['0']), 10)

    def test_execute_read_mem(self):
        # Создаем бинарный файл с командами
        with open(self.binary_file, 'wb') as f:
            # LOAD_CONST 20 в регистр 1
            f.write(struct.pack("BBBBBB", 10, 20, 1, 0, 0, 0))  # opcode 10, op1=20, op2=1
            # LOAD_CONST 30 в регистр 2
            f.write(struct.pack("BBBBBB", 10, 30, 2, 0, 0, 0))  # opcode 10, op1=30, op2=2
            # READ_MEM 1 в регистр 3
            f.write(struct.pack("BBBBBB", 50, 3, 1, 0, 0, 0))  # opcode 50, op1=3, op2=1

        interpreter = Interpreter(self.binary_file, self.result_file, self.memory_range)
        interpreter.run()

        # Проверяем, что значение в памяти по адресу 3 равно 20
        with open(self.result_file, mode='r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Пропускаем заголовок
            result = dict(csv_reader)

        self.assertEqual(int(result['3']), 0)

    def test_execute_popcnt(self):
        # Создаем бинарный файл с командой POPCNT
        with open(self.binary_file, 'wb') as f:
            # LOAD_CONST 5 в регистр 1
            f.write(struct.pack("BBBBBB", 10, 5, 1, 0, 0, 0))  # opcode 10, op1=5, op2=1
            # POPCNT 1 в регистр 2
            f.write(struct.pack("BBBBBB", 27, 2, 1, 0, 0, 0))  # opcode 27, op1=2, op2=1

        interpreter = Interpreter(self.binary_file, self.result_file, self.memory_range)
        interpreter.run()

        # Проверяем, что количество установленных битов в 5 (101) равно 2
        with open(self.result_file, mode='r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Пропускаем заголовок
            result = dict(csv_reader)

        self.assertEqual(int(result['2']), 2)

if __name__ == '__main__':
    unittest.main()