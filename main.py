from csv_importer import CsvImporter
from db_connect import connect_to_db
from generators.sum_generator import sum_generator
from generators.user_generator import user_generator
from objects.user import User, get_all_users


def main() -> None:
    db_connection = connect_to_db('database.db')
    if db_connection is None:
        print('Fatal Error')
        return

    User.create_table(db_connection)
    user_gen = user_generator()
    sum_gen = sum_generator()
    next(sum_gen)
    for i in range(0, 10):
        sum_gen.send(1)
        user = next(user_gen)
        user.save(db_connection)

    generated_users = sum_gen.send(0)
    print(f'Generated: {generated_users} users')
    sum_gen.send(-generated_users)

    csv_importer = CsvImporter(sum_gen)
    csv_importer.import_data('import.csv', db_connection)

    imported_users = sum_gen.send(0)
    print(f'Imported: {imported_users} users')

    all_users = get_all_users(db_connection)
    print(',\n'.join(str(user) for user in all_users))


if __name__ == '__main__':
    main()
