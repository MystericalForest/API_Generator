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

class Config_file:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def get_create_config_file(self):
        filename="output\\api\\config\\dbclass.php"
        f = open(filename, "w")
        f.write("<?php\nclass DBClass {\n\n    private $host = \"" + self.host + "\";\n")
        f.write("    private $username = \"" + self.username + "\";\n")
        f.write("    private $password = \"" + self.password + "\";\n")
        f.write("    private $database = \"" + self.database + "\";\n\n")
        f.write("    public $connection;\n\n    // get the database connection\n")
        f.write("    public function getConnection(){\n\n        $this->connection = null;\n\n")
        f.write("        try{\n            $this->connection = ")
        f.write("new PDO(\"mysql:host=\" . $this->host . \";dbname=\" . $this->database, $this->username, ")
        f.write("$this->password);\n            $this->connection->exec(\"set names utf8\");\n")
        f.write("        }catch(PDOException $exception){\n            echo \"Error: \" . $exception->getMessage();\n")
        f.write("        }\n\n        return $this->connection;\n    }\n}\n?>")
        f.close()
