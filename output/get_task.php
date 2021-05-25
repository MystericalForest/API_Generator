<?php

header("Content-Type: application/json; charset=UTF-8");
  if (isset($_GET['task']) && $_GET['task']!="") {
    include_once 'config/dbclass.php';
    include_once 'objects/tasks.php';
	
    $task_id = $_GET['task'];

    $dbclass = new DBClass();
    $connection = $dbclass->getConnection();

    $task = new Task($connection);

    $stmt = $task->read_one($task_id);
    $count = $stmt->rowCount();

    if($count > 0){


      $tasks = array();
      $tasks["body"] = array();
      $tasks["count"] = $count;

      while ($row = $stmt->fetch(PDO::FETCH_ASSOC)){

        extract($row);
        $p  = array(
          "task_id" => $task_id,
          "race_id" => $race_id,
          "task_name" => $task_name,
          "description" => $description
        );


        array_push($tasks["body"], $p);
      }

      echo json_encode($tasks);
    }

    else {

      echo json_encode(
          array("body" => array(), "count" => 0)
      );
    }
  }
  else {
    echo json_encode(
        array("body" => array(), "count" => 0)
    );
  }
?>