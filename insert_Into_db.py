import db_connection


class AddingData:
    conn = db_connection.MainConnection.return_main_connection()

    cursor = conn.cursor()

    def register_new_player(self, p_name, dexterity, health, luck, book_id, chapter):

        query_text = f"""Insert Into player (book_id, player_name, dext_start, hp_start, luck_start, dext_act, hp_act, 
        luck_act, chapter) Values ('{book_id}', '{p_name}', '{dexterity}', '{health}', '{luck}', '{dexterity}', 
        '{health}', '{luck}', '{chapter}')"""

        self.cursor.execute(query_text)

        self.conn.commit()

    def save_progress(self, dext_act, hp_act, luck_act, chapter, player_name):

        query_text = f"""Update player set dext_act = {dext_act}, hp_act={hp_act}, luck_act={luck_act}, 
        chapter={chapter} where player_name = '{player_name}'"""

        self.cursor.execute(query_text)

        self.conn.commit()

    def update_player(self, dex_start, hp_start, luck_start, chapter, player_name, book_id):

        query_text = f"""Update player set dext_act = {dex_start}, hp_act={hp_start}, luck_act={luck_start}, 
        dext_start = {dex_start}, hp_start={hp_start}, luck_start={luck_start}, chapter={chapter}, 
        player_name = '{player_name}' where book_id = '{book_id}'"""

        self.cursor.execute(query_text)

        self.conn.commit()

    def update_player_stuff(self, target_table, player_id, player_data):
        i = 0

        while i < len(player_data):

            query_text = f"""Update {target_table} set desc = '{player_data[i+1]}', quantity = {player_data[i+2]} 
            where player_id = {player_id} and name = '{player_data[i]}' """

            self.cursor.execute(query_text)

            self.conn.commit()

            i += 3

    def add_new_player_stuff(self, target_table, player_id, item_name, item_desc, item_quant):

        query_text = f"""insert into {target_table} (player_id, name, desc, quantity) 
        values ({player_id}, '{item_name}', '{item_desc}', {item_quant})"""

        self.cursor.execute(query_text)

        self.conn.commit()

    def update_player_luck(self, act_luck, player_name):

        query_text = f"""Update player set luck_act={act_luck} where player_name = '{player_name}'"""

        self.cursor.execute(query_text)

        self.conn.commit()

    def update_player_hp(self, player_hp, player_name):

        query_text = f"""Update player set hp_act={player_hp} where player_name = '{player_name}'"""

        self.cursor.execute(query_text)

        self.conn.commit()

    def delete_player_items(self, table_name, player_name, book_id):
        query_text = f"""Delete from {table_name} where player_id = 
        (Select Id from player where player_name = '{player_name}' and book_id = 
        (Select id from books where id={book_id}))"""

        self.cursor.execute(query_text)

        self.conn.commit()

