import os
import csv
from typing import List, Dict


class CSVHandler:
    @staticmethod
    def count_files(directory: str) -> int:
        """Подсчитывает количество файлов в указанной директории"""
        return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

    @staticmethod
    def get_csv_path(directory: str, filename: str) -> str:
        """Возвращает полный путь к CSV-файлу"""
        return os.path.join(directory, filename)

    @staticmethod
    def read_csv(filepath: str) -> List[Dict]:
        """Читает CSV-файл с автоматическим определением кодировки"""
        encodings = ['utf-8', 'cp1251']
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as file:
                    return list(csv.DictReader(file))
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Не удалось прочитать файл {filepath} с кодировками: {encodings}")

    @staticmethod
    def validate_data(data: List[Dict]) -> bool:
        """Проверяет, что данные не пусты"""
        if not data:
            print("Внимание: данные пусты!")
            return False
        return True

    @staticmethod
    def sort_data(data: List[Dict], key: str, numeric: bool = False) -> List[Dict]:
        """Сортирует данные по указанному ключу"""
        return sorted(data, key=lambda x: int(x.get(key, 0)) if numeric else sorted(data, key=lambda x: x.get(key, ''))

                                                                             @ staticmethod

    def filter_by_date(data: List[Dict], date_field: str, threshold: str) -> List[Dict]:
        """Фильтрует данные по дате"""
        return [entry for entry in data if entry.get(date_field, '') > threshold]

    @staticmethod
    def save_to_csv(filepath: str, data: List[Dict]) -> None:
        """Сохраняет данные в CSV-файл"""
        if not data:
            raise ValueError("Нет данных для сохранения")

        # Получаем все возможные поля из данных
        fieldnames = list(set().union(*(d.keys() for d in data)))

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"Данные успешно сохранены в {filepath}")
        except PermissionError:
            print("Ошибка: Нет прав на запись. Закройте файл в других программах")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")


def main():
    # 1. Подсчет файлов в папке
    directory = r"C:\Users\gorsh\PycharmProjects\PythonProject"
    print(f"Количество файлов в директории: {CSVHandler.count_files(directory)}")

    # 2. Получение пути к CSV-файлу
    csv_file = CSVHandler.get_csv_path(directory, 'data.csv')

    # 3. Чтение данных из CSV
    try:
        data = CSVHandler.read_csv(csv_file)
        print(f"Файл {csv_file} успешно прочитан")
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        data = []

    # 4. Проверка данных
    if not CSVHandler.validate_data(data):
        exit()

    # 5. Обработка данных
    try:
        print("\nСортировка по номерному знаку:")
        for item in CSVHandler.sort_data(data, 'номерной знак'):
            print(item)

        print("\nСортировка по номеру (как число):")
        for item in CSVHandler.sort_data(data, 'N°', numeric=True):
            print(item)

        print("\nФильтрация по дате (после 13.05):")
        for item in CSVHandler.filter_by_date(data, 'дата', '13.05'):
            print(item)
    except KeyError as e:
        print(f"\nОшибка: Отсутствует ключ {e}")

    # 6. Добавление новой записи
    new_record = {
        'N°': '7',
        'дата': '2023-10-15',
        'время': '14:30',
        'номерной знак': 'XYZ1234',
        'марка автомобиля': 'Toyota'
    }
    data.append(new_record)

    # 7. Сохранение данных
    CSVHandler.save_to_csv(csv_file, data)


if __name__ == "__main__":
    main()
