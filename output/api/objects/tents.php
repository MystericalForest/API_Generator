<?php
class Tents{

    // Connection instance
    private $connection;

    // table name
    private $table_name = "tents";

    // table columns
    public $tent_id;
    public $tent_type;
    public $name;
    public $description;

    public function __construct($connection){
        $this->connection = $connection;
    }

    //C
    public function create($tent_id, $tent_type, $name, $description){
        $query = "INSERT INTO `tents` ('tent_id', 'tent_type', 'name', 'description') VALUES (". $tent_id. ", ". $tent_type. ", '". $name. "', '". $description. "')"

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
    //R
    public function read(){
        $query = "SELECT tent_id, tent_type, name, description FROM tents";

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
    //R
    public function read_one($tent_id, $tent_type){
        $query = "SELECT tent_id, tent_type, name, description FROM tents WHERE tent_id = ". $tent_id . " AND tent_type = ". $tent_type;

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
//U
    public function update($tent_id, $tent_type, $name, $description){
        $query = "UPDATE `tents` SET `name`='". $name. "', `description`='". $description. "' WHERE `tent_id`=". $tent_id. ", `tent_type`=". $tent_type;

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
    //D
    public function delete($tent_id, $tent_type){
        $query = "DELETE FROM tents WHERE tent_id = ". $tent_id . " AND tent_type = ". $tent_type;

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
}
