<?php
class Task{

    // Connection instance
    private $connection;

    // table name
    private $table_name = "task";

    // table columns
    public $task_id;
    public $title;
    public $description;

    public function __construct($connection){
        $this->connection = $connection;
    }

    //C
    public function create($task_id, $title, $description){
        $query = "INSERT INTO `task` ('task_id', 'title', 'description') VALUES (". $task_id. ", '". $title. "', '". $description. "')"

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
    //R
    public function read(){
        $query = "SELECT task_id, title, description FROM task";

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
    //R
    public function read_one($task_id){
        $query = "SELECT task_id, title, description FROM task WHERE task_id = ". $task_id;

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
//U
    public function update($task_id, $title, $description){
        $query = "UPDATE `task` SET `title`='". $title. "', `description`='". $description. "' WHERE `task_id`=". $task_id;

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
    //D
    public function delete($task_id){
        $query = "DELETE FROM task WHERE task_id = ". $task_id;

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
}
