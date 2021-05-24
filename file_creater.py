class SQL:
    def __init__(self, tables):
        self._tables=tables

    def create_sql_tables_file(self):
        filename="output\\sql\\create_tables.sql"
        f = open(filename, "w")
        for table in self._tables:
            f.write("\n-- Creating table " + table.table_name + "\n")
            f.write("CREATE TABLE " + table.table_name + " (\n")
            for idx, field in enumerate(table.fields):
                f.write("  " + field.field_name + " " + field.field_type)
                if (field.primary):
                    f.write(" NOT NULL")
                if idx==len(table.fields)-1:
                    primary=table.get_primary_fields()
                    if len(primary)==0:
                        f.write("\n")
                    else:
                       f.write(",\n  PRIMARY KEY (")
                       for idx, primary_key in enumerate(primary):
                           f.write(primary_key.field_name)
                           if idx==len(primary)-1:
                               f.write(")\n")
                           else:
                              f.write(", ") 
                else:
                    f.write(",\n")
            f.write(");\n\n")
        f.close()

class Config_file:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def create_config_file(self):
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

class CRUD_API_file:
    def __init__(self):
        pass

    def _get_function_text(self, sql):
        rtn="        $query = \"" + sql + "\n\n"
        rtn+="        $stmt = $this->connection->prepare($query);\n\n"
        rtn+="        $stmt->execute();\n\n        return $stmt;\n"

        return rtn

    def _get_insert_text(self):
        sql="INSERT INTO `ra_tasks`('task_id', 'race_id', 'task_name', 'description') VALUES (\". $task_id. \", \". $race_id. \", '\". $task_name. \"', '\". $description. \"')\""
        return sql

    def _get_select_text(self, table):
        sql="SELECT "
        for idx, field in enumerate(table.fields):
            sql+= field.field_name
            if idx<len(table.fields)-1:
                sql+=", "
            else:
                sql+=" "
        sql+="FROM " + table.table_name + "\";"
        return sql

    def _get_select_one_text(self, table):
        sql="SELECT "
        for idx, field in enumerate(table.fields):
            sql+= field.field_name
            if idx<len(table.fields)-1:
                sql+=", "
            else:
                sql+=" "
        sql+="FROM " + table.table_name + " WHERE "
        primary=table.get_primary_fields()
        for idx, field in enumerate(primary):
            sql+= field.field_name + " = \". $" + field.field_name
            if idx<len(primary)-1:
                sql+=" . \" AND "
            else:
                sql+=";"
        return sql
    
    def _get_update_text(self):
        sql="UPDATE `ra_tasks` SET `race_id`='\". $race_id. \"',`task_name`=\". $task_name. \",`description`='\". $description. \"' WHERE `task_id`=\". $task_id;"
        return sql

    def _get_delete_text(self, table):
        sql="DELETE FROM " + table.table_name + " WHERE "
        primary=table.get_primary_fields()
        for idx, field in enumerate(primary):
            sql+= field.field_name + " = \". $" + field.field_name
            if idx<len(primary)-1:
                sql+=" . \" AND "
            else:
                sql+=";"
        return sql

    def _get_primary_fields(self, table):
        primary=table.get_primary_fields()
        rtn=""
        for idx, field in enumerate(primary):
            rtn+= "$" + field.field_name
            if idx<len(primary)-1:
                rtn+=", "
            else:
                rtn+=""
        return rtn

    def _get_all_fields(self, table):
        fields=table.fields
        rtn=""
        for idx, field in enumerate(fields):
            rtn+= "$" + field.field_name
            if idx<len(fields)-1:
                rtn+=", "
            else:
                rtn+=""
        return rtn

    def create_CRUD_file(self, table):
        filename="output\\api\\objects\\" + table.table_name + ".php"
        f = open(filename, "w")
        f.write("<?php\nclass " + table.table_name.capitalize() + "{\n\n    // Connection instance\n    private $connection;\n\n")
        f.write("    // table name\n    private $table_name = \"" + table.table_name + "\";\n\n")
        f.write("    // table columns\n")
        for idx, field in enumerate(table.fields):
            f.write("    public $" + field.field_name + ";\n")
        f.write("\n    public function __construct($connection){\n")
        f.write("        $this->connection = $connection;\n    }\n\n    //C\n")
        f.write("    public function create(")
        f.write(self._get_all_fields(table))
        f.write("){\n" + self._get_function_text(self._get_insert_text()))       
        f.write("    }\n    //R\n    public function read(){\n")
        f.write(self._get_function_text(self._get_select_text(table)))
        f.write("    }\n    //R\n    public function read_one(")
        f.write(self._get_primary_fields(table))
        f.write("){\n")
        f.write(self._get_function_text(self._get_select_one_text(table)))
        f.write("    }\n    //U\n    public function update(")
        f.write(self._get_all_fields(table))
        f.write("){\n" + self._get_function_text(self._get_update_text()) + "    }\n")
        f.write("    //D\n    public function delete(")
        f.write(self._get_primary_fields(table))
        f.write("){\n")
        f.write(self._get_function_text(self._get_delete_text(table)))
        f.write("    }\n}\n")
        f.close()
        
