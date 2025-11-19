class ReadFile:

    def read_rules(self):
        data = ""
        with open("szabályok.csv", "r", encoding="utf-8") as f:
            raw_data = f.readlines()

            for item in raw_data:
                temp_item = item.split(";")
                data += "\n"
                data += temp_item[0]
                data += "\n"
                data += "\n"
                data += temp_item[1]

        return data
