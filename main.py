import psycopg2


def connect_db():
    """Подключение к базе данных PostgreSQL."""
    return psycopg2.connect(
        dbname="",
        user="",  # Замените на ваше имя пользователя 567
        password="",  # Укажите ваш пароль
        host="",  # Укажите ваш хост
        port=""  # Порт PostgreSQL по умолчанию
    )


def add_category(name, description):
    """Добавление новой категории."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Categories (name, description) VALUES (%s, %s);", (name, description))
    conn.commit()
    cursor.close()
    conn.close()


def get_items_by_location(location_name):
    """Получение всех вещей по местоположению."""
    conn = connect_db()
    cursor = conn.cursor()
    query = """
    SELECT Items.description, Items.found_date, Categories.name AS category
    FROM Items
    JOIN Locations ON Items.location_id = Locations.location_id
    JOIN Categories ON Items.category_id = Categories.category_id
    WHERE Locations.name = %s;
    """
    cursor.execute(query, (location_name,))
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items


def update_item_status(item_id, new_status):
    """Обновление статуса вещи."""
    conn = connect_db()
    cursor = conn.cursor()
    query = "CALL update_item_status(%s, %s);"
    cursor.execute(query, (item_id, new_status))
    conn.commit()
    cursor.close()
    conn.close()


def delete_item(item_id):
    """Удаление вещи."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Items WHERE item_id = %s;", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()


def get_items():
    """Получение всех вещей."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT description, found_date, current_status FROM Items;")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items


def main():
    """Основная логика программы."""
    while True:
        print("\nВыберите действие:")
        print("1. Добавить категорию")
        print("2. Получить вещи по местоположению")
        print("3. Обновить статус вещи")
        print("4. Удалить вещь")
        print("5. Показать все вещи")
        print("6. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            name = input("Введите имя категории: ")
            description = input("Введите описание категории: ")
            add_category(name, description)
            print(f"Категория '{name}' добавлена.")

        elif choice == "2":
            location_name = input("Введите имя местоположения: ")
            items = get_items_by_location(location_name)
            print("Найденные вещи:")
            for item in items:
                print(f"Описание: {item[0]}, Дата: {item[1]}, Категория: {item[2]}")

        elif choice == "3":
            item_id = int(input("Введите ID вещи: "))
            new_status = input("Введите новый статус: ")
            update_item_status(item_id, new_status)
            print(f"Статус вещи с ID {item_id} обновлен на '{new_status}'.")

        elif choice == "4":
            item_id = int(input("Введите ID вещи для удаления: "))
            delete_item(item_id)
            print(f"Вещь с ID {item_id} удалена.")

        elif choice == "5":
            items = get_items()
            print("Все вещи:")
            for item in items:
                print(f"Описание: {item[0]}, Дата нахождения: {item[1]}, Статус: {item[2]}")

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
