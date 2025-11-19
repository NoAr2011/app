from kivy.uix.button import Button


class ExtractingNext:

    def get_next_chapters(self, splited_text):
        page_split = []

        i = 1

        while i < len(splited_text):
            temp_split = splited_text[i].split(".")

            for item in temp_split:

                empty_space = item.strip(" ").split(" ")

                if len(empty_space) > 1:
                    just_number = empty_space[1].split("-")[0]
                    try:
                        int_number = int(just_number)
                        page_split.append(just_number)
                    except Exception as ex:
                        pass

            i += 1

        return page_split

    def add_new_buttons(self, chapter_grid, page_split, target_screen):
        chapter_grid.cols = len(page_split)
        for item in page_split:
            page_button = Button()
            page_button.text = item
            page_button.background_normal = "button09.png"
            page_button.border = (0, 0, 0, 0)
            page_button.bind(on_release=target_screen.next_chapter)

            chapter_grid.add_widget(page_button)