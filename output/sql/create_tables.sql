
-- Creating table task
CREATE TABLE task (
  task_id int NOT NULL,
  title varchar,
  description varchar,
  PRIMARY KEY (task_id)
);


-- Creating table tents
CREATE TABLE tents (
  tent_id int NOT NULL,
  tent_type int NOT NULL,
  name varchar,
  description varchar,
  PRIMARY KEY (tent_id, tent_type)
);

