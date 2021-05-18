<?php
class DBClass {

    private $host = "mysql55.unoeuro.com";
    private $username = "vildmarkskaffe_dk";
    private $password = "Kasper3230";
    private $database = "vildmarkskaffe_dk_db";

    public $connection;

    // get the database connection
    public function getConnection(){

        $this->connection = null;

        try{
            $this->connection = new PDO("mysql:host=" . $this->host . ";dbname=" . $this->database, $this->username, $this->password);
            $this->connection->exec("set names utf8");
        }catch(PDOException $exception){
            echo "Error: " . $exception->getMessage();
        }

        return $this->connection;
    }
}
?>