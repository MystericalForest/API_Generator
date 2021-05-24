<?php
class Task{

    // Connection instance
    private $connection;

    // table name
    private $table_name = "ra_tasks";

    // table columns
    public $task_id;
    public $race_id;
    public $task_name;
    public $description;

    public function __construct($connection){
        $this->connection = $connection;
    }
    
    //C
    public function create($task_id, $race_id, $task_name, $description){
        $query = "INSERT INTO `ra_tasks`('task_id', 'race_id', 'task_name', 'description') VALUES (". $task_id. ", ". $race_id. ", '". $task_name. "', '". $description. "')";

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
    //R
    public function read(){
        $query = "SELECT task_id, race_id, task_name, description FROM `ra_tasks`";

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
    //R
    public function read_one($task_id){
        $query = "SELECT task_id, race_id, task_name, description FROM `ra_tasks` WHERE task_id=". $task_id;

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
    //U
    public function update($task_id, $race_id, $task_name, $description){
        $query = "UPDATE `ra_tasks` SET `race_id`='". $race_id. "',`task_name`=". $task_name. ",`description`='". $description. "' WHERE `task_id`=". $task_id;

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
    //D
    public function delete($task_id){
        $query = "DELETE FROM ra_tasks WHERE task_id=". $task_id;

        $stmt = $this->connection->prepare($query);

        $stmt->execute();

        return $stmt;
    }
}