#!/usr/bin/env python3
"""
Примеры запуска скрипта.

Примеры базовых вызовов для анализа макроэкономических данных.
"""

# Пример 1: Отчет по одному файлу
# python main.py --files Пример1.csv --report average-gdp

# Пример 2: Отчет по двум файлам
# python main.py --files Пример1.csv Пример2.csv --report average-gdp

# Пример 3: Отчет с использованием абсолютного пути
# python main.py --files C:\path\to\Пример1.csv C:\path\to\Пример2.csv --report average-gdp

# Пример 4: Запуск с параметром --report (по умолчанию average-gdp)
# python main.py --files Пример1.csv Пример2.csv

# Пример 5: Запуск из другого каталога
# cd C:\Users\Username\Desktop\
# python Testovoe Python/main.py --files "Testovoe Python/Пример1.csv" "Testovoe Python/Пример2.csv"
