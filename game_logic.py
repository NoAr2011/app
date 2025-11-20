import random
from kivy.app import App
from kivy.clock import Clock
from insert_Into_db import *


class ImplementGameLogic:

    inserting_to_db = AddingData()

    @staticmethod
    def generate_dice(main_grid):
        player_dice_01 = random.randrange(1, 7)  # D6
        player_dice_02 = random.randrange(1, 7)  # D6

        player_attack = player_dice_01 + player_dice_02

        main_grid.children[len(main_grid.children) - 4].text = str(player_attack)

        enemy_dice_01 = random.randrange(1, 7)  # D6
        enemy_dice_02 = random.randrange(1, 7)  # D6

        enemy_attack = enemy_dice_01 + enemy_dice_02

        i = len(main_grid.children) - 8

        while i > -1:

            if main_grid.children[i + 1].text != "0":  # Enemy HP

                main_grid.children[i].text = str(enemy_attack)
                break
            i -= 4

    def fight_enemy(self, popup_screen, screen, main_grid):
        j = len(main_grid.children)

        if main_grid.children[j - 4].text != "":

            player_attack = int(main_grid.children[j - 2].text) + int(main_grid.children[j - 4].text)

            i = len(main_grid.children) - 5

            while i > -1:

                if main_grid.children[i - 2].text != "0" and main_grid.children[i-1].text != "" \
                        and main_grid.children[i-3].text != "":  # Enemy HP

                    enemy_attack = int(main_grid.children[i - 3].text) + int(main_grid.children[i-1].text)

                    if player_attack > enemy_attack:
                        if int(main_grid.children[i - 2].text) - 2 < 0:
                                main_grid.children[i - 2].text = "0"
                        else:
                            main_grid.children[i - 2].text = str(int(main_grid.children[i - 2].text) - 2)

                        if main_grid.children[i - 2].text == "0":
                            popup_screen.warning_popup(screen, "Győztél!")

                        main_grid.children[i - 3].text = ""
                        main_grid.children[j - 4].text = ""
                        break

                    if player_attack < enemy_attack:
                        if int(main_grid.children[j - 3].text) - 2 < 0:
                            main_grid.children[j - 3].text = "0"

                        else:
                            main_grid.children[j - 3].text = str(int(main_grid.children[j - 3].text) - 2)

                        main_grid.children[i - 3].text = ""
                        main_grid.children[j - 4].text = ""
                        break

                    if player_attack == enemy_attack:
                        popup_screen.warning_popup(screen, "Dontetlen, dobj újra!")

                i -= 4
            self.update_player_hp(main_grid.children[j - 3].text, main_grid.children[j - 1].text)
            current_app = App.get_running_app()
            root_screen = current_app.root
            target_screen = root_screen.get_screen("book")
            target_screen.ids["actual_health"].text = main_grid.children[j - 3].text
            if main_grid.children[j - 3].text == "0":
                popup_screen.warning_popup(screen, "Elvesztettted a harcot!")

        else:
            popup_screen.warning_popup(screen, "Dobj a kockákkal!")

    def update_player_hp(self, player_hp, player_name):
            self.inserting_to_db.update_player_hp(player_hp, player_name)

    def generate_luck(self, popup_screen, screen, player_dice_text, player_luck_text, player_name):
        player_dice_01 = random.randrange(1, 7)  # D6
        player_dice_02 = random.randrange(1, 7)  # D6

        player_dice_text.text = str(int(player_dice_01)+int(player_dice_02))

        if int(player_dice_text.text) > int(player_luck_text.text):

            Clock.schedule_once(lambda dt: popup_screen.warning_popup(screen, "Nincs szerencséd!"), 0.5)

        else:

            Clock.schedule_once(lambda dt: popup_screen.warning_popup(screen, "Szerencséd van!"), 0.5)

        if int(player_luck_text.text) > 0:
            Clock.schedule_once(lambda dt: self.update_luck(dt, player_luck_text, player_name), 0.8)

    def update_luck(self, dt, player_luck_text, player_name):
        new_luck = int(player_luck_text.text) - 1
        player_luck_text.text = str(new_luck)

        current_app = App.get_running_app()
        root_screen = current_app.root
        target_screen = root_screen.get_screen("book")
        target_screen.ids["actual_luck"].text = player_luck_text.text

        self.inserting_to_db.update_player_luck(player_luck_text.text, player_name)

    def new_backpack_item(self, popup_window, button_text, screen, player_id, item_name, item_desc, item_quant):

            if item_name != "" and item_desc != "" and item_quant != "":

                if button_text == "Felszerelés":
                    target_table = "equipment"
                else:
                    target_table = "spells"

                try:
                    check_quantity = int(item_quant)

                    self.inserting_to_db.add_new_player_stuff(target_table, player_id, item_name, item_desc, check_quantity)
                    popup_window.warning_popup(screen, f"{button_text} sikeresen elmentve!")
                except Exception as ex:
                    popup_window.warning_popup(screen, "Mennyiséghez csak szám írható!")


            else:
                popup_window.warning_popup(screen, "Minden mezőt ki kell töltened!")

    def update_backpack(self, popup_window, button_text, screen, player_id, stuff_grid):
        new_data = []
        for item in stuff_grid.children:
            for child_item in item.children:
                new_data.append(child_item.text)

        if button_text == "Felszerelés":
            target_table = "equipment"
        else:
            target_table = "spells"
        new_data.reverse()
        self.inserting_to_db.update_player_stuff(target_table, player_id, new_data)

        popup_window.warning_popup(screen, "Felszerelés frissítve!")

    def change_player(self, popup_window, screen, dex_start, hp_start, luck_start, chapter, player_name, book_id):

        self.inserting_to_db.update_player(dex_start, hp_start, luck_start, chapter, player_name, book_id)
        self.inserting_to_db.delete_player_items("equipment", player_name, book_id)
        self.inserting_to_db.delete_player_items("spells", player_name, book_id)

        popup_window.warning_popup(screen, "Karakter módosítva!")
