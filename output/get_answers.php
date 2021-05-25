<?php

header("Content-Type: application/json; charset=UTF-8");
  if (isset($_GET['task']) && $_GET['task']!="") {
    include_once 'config/dbclass.php';
    include_once 'objects/answers.php';
	
    $task_id = $_GET['task'];

    $dbclass = new DBClass();
    $connection = $dbclass->getConnection();

    $answer = new Answer($connection);

    $stmt = $answer->read_task($task_id);
    $count = $stmt->rowCount();

    if($count > 0){

      $answers = array();
      $answers["body"] = array();
      $answers["count"] = $count;

      while ($row = $stmt->fetch(PDO::FETCH_ASSOC)){

        extract($row);
        $p  = array(
		  "answer_id" => $answer_id,
		  "task_id" => $task_id,
		  "answer_name" => $answer_name,
		  "description" => $description
        );


        array_push($answers["body"], $p);
      }

      echo json_encode($answers);
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