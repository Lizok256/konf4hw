import unittest
import os
import struct
import csv
from main import Assembler  # Предположим, что ваш код сохранен в файле assembler.py


class TestAssembler(unittest.TestCase):
    def setUp(self):
        # Создаем временные файлы для тестирования
        self.input_file = 'test_input.asm'
        self.output_file = 'test_output.bin'
        self.log_file = 'test_log.csv'

        # Записываем тестовые данные в входной файл
        with open(self.input_file, 'w') as f:
            f.write("10 99 0 0 0 0\n")
            f.write("50 31 0 0 0 0\n")
            f.write("# Это комментарий\n")
            f.write("41 60 0 0 0 0\n")
            f.write("\n")  # Пустая строка
            f.write("27 89 0 0 0 0\n")

    def tearDown(self):
        # Удаляем временные файлы после тестирования
        for file in [self.input_file, self.output_file, self.log_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_assemble_creates_binary_file(self):
        assembler = Assembler(self.input_file, self.output_file, self.log_file)
        assembler.assemble()

        # Проверяем, что бинарный файл создан
        self.assertTrue(os.path.exists(self.output_file))

        # Проверяем содержимое бинарного файла
        with open(self.output_file, 'rb') as f:
            content = f.read()
            # Проверяем, что содержимое соответствует ожидаемому
            expected_bytes = struct.pack("BBBBBB", 10, 99, 0, 0, 0, 0) + \
                             struct.pack("BBBBBB", 50, 31, 0, 0, 0, 0) + \
                             struct.pack("BBBBBB", 41, 60, 0, 0, 0, 0) + \
                             struct.pack("BBBBBB", 27, 89, 0, 0, 0, 0)
            self.assertEqual(content, expected_bytes)

    def test_assemble_creates_log_file(self):
        assembler = Assembler(self.input_file, self.output_file, self.log_file)
        assembler.assemble()

        # Проверяем, что лог-файл создан
        self.assertTrue(os.path.exists(self.log_file))

        # Проверяем содержимое лог-файла
        with open(self.log_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(rows[0], ["A", "B", "C", "D", "E", "F"])  # Заголовок
            self.assertEqual(rows[1], ['10', '99', '0', '0', '0', '0'])
            self.assertEqual(rows[2], ['50', '31', '0', '0', '0', '0'])
            self.assertEqual(rows[3], ['41', '60', '0', '0', '0', '0'])
            self.assertEqual(rows[4], ['27', '89', '0', '0', '0', '0'])

    def test_assembler_ignores_comments_and_empty_lines(self):
        assembler = Assembler(self.input_file, self.output_file, self.log_file)
        assembler.assemble()

        # Проверяем, что бинарный файл создан и содержит только нужные инструкции
        with open(self.output_file, 'rb') as f:
            content = f.read()
            expected_bytes = struct.pack("BBBBBB", 10, 99, 0, 0, 0, 0) + \
                             struct.pack("BBBBBB", 50, 31, 0, 0, 0, 0) + \
                             struct.pack("BBBBBB", 41, 60, 0, 0, 0, 0) + \
                             struct.pack("BBBBBB", 27, 89, 0, 0, 0, 0)
            self.assertEqual(content, expected_bytes)

        #