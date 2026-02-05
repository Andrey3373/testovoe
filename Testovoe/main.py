"""
Скрипт для анализа макроэкономических данных.
"""
import argparse
import csv
import sys
from pathlib import Path
from collections import defaultdict


def read_csv_files(file_paths):
    """
    Читает CSV файлы и возвращает список записей.
    
    Args:
        file_paths: Список путей к CSV файлам
        
    Returns:
        Список словарей с данными
    """
    data = []
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            print(f"Ошибка: файл '{file_path}' не найден", file=sys.stderr)
            sys.exit(1)
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Ошибка при чтении файла '{file_path}': {e}", file=sys.stderr)
            sys.exit(1)
    
    return data


def calculate_average_gdp(data):
    """
    Вычисляет средний ВВП по странам.
    
    Args:
        data: Список словарей с данными
        
    Returns:
        Словарь со средним ВВП по странам (отсортированный по убыванию)
    """
    country_gdp = defaultdict(list)
    
    for row in data:
        country = row.get('country', '').strip()
        gdp = row.get('gdp', '').strip()
        
        if country and gdp:
            try:
                country_gdp[country].append(float(gdp))
            except ValueError:
                continue
    
    # Вычисляем средний ВВП и сортируем по убыванию
    average_gdp = {}
    for country, gdp_values in country_gdp.items():
        average_gdp[country] = sum(gdp_values) / len(gdp_values)
    
    # Сортируем по значению ВВП в убывающем порядке
    sorted_gdp = dict(sorted(
        average_gdp.items(),
        key=lambda x: x[1],
        reverse=True
    ))
    
    return sorted_gdp


def format_table(data):
    """
    Форматирует данные в виде таблицы.
    
    Args:
        data: Словарь со значениями для таблицы
        
    Returns:
        Отформатированная таблица
    """
    if not data:
        return "Нет данных для отчета"
    
    # Определяем ширину столбцов
    headers = ['country', 'gdp']
    countries = list(data.keys())
    
    # Расчет ширины для столбца страны
    country_width = max(
        len(headers[0]),
        max(len(c) for c in countries) if countries else 1
    )
    
    # Расчет ширины для столбца ВВП
    gdp_width = max(
        len(headers[1]),
        max(len(f"{v:.2f}") for v in data.values()) if data else 1
    )
    
    col_widths = [country_width, gdp_width]
    
    # Формируем таблицу
    lines = []
    
    # Разделитель
    separator = '+' + '+'.join('-' * (w + 2) for w in col_widths) + '+'
    
    # Заголовок
    header_line = '| ' + ' | '.join(
        h.center(col_widths[i]) for i, h in enumerate(headers)
    ) + ' |'
    
    lines.append(separator)
    lines.append(header_line)
    lines.append(separator)
    
    # Данные
    for country, gdp in data.items():
        row = (
            f'| {country:<{col_widths[0]}} '
            f'| {gdp:>{col_widths[1]}.2f} |'
        )
        lines.append(row)
    
    lines.append(separator)
    
    return '\n'.join(lines)


def main():
    """Главная функция скрипта."""
    parser = argparse.ArgumentParser(
        description='Анализ макроэкономических данных'
    )
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Пути к CSV файлам для анализа'
    )
    parser.add_argument(
        '--report',
        default='average-gdp',
        help='Название отчета (по умолчанию: average-gdp)'
    )
    
    args = parser.parse_args()
    
    # Читаем данные
    data = read_csv_files(args.files)
    
    if not data:
        print("Ошибка: не найдено данных в файлах", file=sys.stderr)
        sys.exit(1)
    
    # Формируем отчет в зависимости от типа
    if args.report == 'average-gdp':
        result = calculate_average_gdp(data)
        print(format_table(result))
    else:
        print(f"Ошибка: неизвестный тип отчета '{args.report}'", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
