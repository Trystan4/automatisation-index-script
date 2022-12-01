#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import sys
import json
import os

environnement = {
}

def main():
    URL_JSON = os.path.abspath("json")
    URL_INDEX = os.path.abspath("index_script")
    first_line = "SET ANSI_PADDING ON\n"
    go_line = "GO\n"
    last_line = "WITH (STATISTICS_NORECOMPUTE = OFF, DROP_EXISTING = OFF, ONLINE = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]\n"
    create_lines = []
    column_lines = []
    number = 0
    # 1 by 1 json 
    for e in environnement :
        
        complete_name = os.path.join(URL_JSON, environnement[e] + '.json')
        # read json file
        read_file = open(complete_name, 'r')
        data_content = read_file.read()
        data = json.loads(data_content)
        
        # json content
        table_name = data["TABLE"]
        table_columns = data["COLONNE"]
        columns_length = len(table_columns)
        
        # sql script content
        sql_file = open('script.sql', "r")
        sql_lines = sql_file.readlines()
        for column in table_columns:
            for line in sql_lines:
                if("CREATE" in line):
                    # create line table and column
                    line = line.replace("TABLE", table_name)
                    line = line.replace("COLONNE", column)
                    create_lines.append(line)
                    # column line
                if("ASC" in line):
                    line = line.replace("COLONNE", column)
                    column_lines.append(line)
        
        complete_index = os.path.join(URL_INDEX, table_name + ".sql")
        with open(complete_index, 'w') as f:
            while(number < columns_length):
                f.write(first_line)
                f.write(go_line)
                f.write(create_lines[number] + "\n")
                f.write(column_lines[number] + "\n")
                f.write(last_line)
                f.write(go_line)
                f.write("\n")
                number += 1
            f.close()
        
        sql_file.close()
        read_file.close()
        # réinitialisation à chaque fichier
        create_lines = []
        column_lines = []
        number = 0
    return 0

if __name__ == "__main__":
    sys.exit(main())