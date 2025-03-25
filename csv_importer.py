import csv
from typing import Generator

from objects.user import User


class CsvImporter:
    def __init__(self, user_created_counter: Generator[int, int, None] = None):
        self.reader = None
        self.user_created_counter = user_created_counter

    def import_data(self, filename, db_connection) -> bool:
        with open(filename, 'r') as file:
            self.reader = csv.reader(file)
            line_gen = self.line_reader()
            header = next(line_gen)  # maybe handle different order in the future
            try:
                while True:
                    line = next(line_gen)
                    user = User(
                        url=line[0],
                        email=line[1],
                        first_name=line[2],
                        last_name=line[3]
                    )
                    user.save(db_connection)
                    self.user_created_counter.send(1)
            except StopIteration as e:
                return True
            except Exception as e:
                print(f'Something went wrong: {e}')
                return False

    def line_reader(self) -> Generator[list[str], None, False]:
        if self.reader is None:
            return False
        for line in self.reader:
            yield line
        return False
