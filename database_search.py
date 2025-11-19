import db_connection


class DataSelect:

    conn = db_connection.MainConnection.return_main_connection()

    cursor = conn.cursor()

    def select_target_chapter(self, book_name, chapter):

        sqlString = (f"SELECT content FROM chapters where chapter_order ={chapter} and book_id = "
                     f"(Select Id from books where book_name = '{book_name}')")

        self.cursor.execute(sqlString)

        raw_data = self.cursor.fetchall()
        data = ""
        for raw_item in raw_data:
            for temp_item in raw_item:
                #data.append(temp_item)
                data = temp_item

        return data

    def get_book_id(self, book_name):
        self.cursor.execute(f"Select Id from books where book_name = '{book_name}'")

        raw_data = self.cursor.fetchall()
        data = ""
        for raw_item in raw_data:
            for temp_item in raw_item:
                # data.append(temp_item)
                data = temp_item

        return data

    def get_player(self, book_name):
        self.cursor.execute(f"Select * from player where book_id = "
                            f"(Select Id from books where book_name = '{book_name}')")

        raw_data = self.cursor.fetchall()
        data = []
        for raw_item in raw_data:
            for temp_item in raw_item:
                data.append(temp_item)
                #data = temp_item

        return data

    def get_player_equipment(self, target_table, player_name):
        self.cursor.execute(f"Select name, desc, quantity from {target_table} where player_id = "
                            f"(Select Id from player where player_name = '{player_name}')")

        raw_data = self.cursor.fetchall()
        data = []
        for raw_item in raw_data:
            for temp_item in raw_item:
                data.append(temp_item)
                # data = temp_item

        return data

    def get_player_id(self, player_name):
        self.cursor.execute(f"Select Id from player where player_name = '{player_name}'")

        raw_data = self.cursor.fetchall()
        data = []
        for raw_item in raw_data:
            for temp_item in raw_item:
                # data.append(temp_item)
                data = temp_item

        return data

    def get_monsters(self, book_id, book_chapter):

        self.cursor.execute(f"Select name, dexterity, hp from monsters "
                            f"where book_id = {book_id} AND book_page={book_chapter}")

        raw_data = self.cursor.fetchall()
        data = []
        for raw_item in raw_data:
            for temp_item in raw_item:
                data.append(temp_item)
                # data = temp_item

        return data





