class SQL:
    def __init__(self, table):
        self._table=table

    def get_create_table_file(self):
        filename="output\\sql\\create_" + self._table.table_name + ".sql"
        f = open(filename, "w")
        f.write("\n-- Creating table " + self._table.table_name + "\n")
        f.write("CREATE TABLE " + self._table.table_name + " (\n")
        for idx, field in enumerate(self._table.fields):
            f.write("  " + field.field_name + " " + field.field_type)
            if idx==len(self._table.fields)-1:
                f.write("\n")
            else:
                f.write(",\n")
        f.write(");")
        f.close()
