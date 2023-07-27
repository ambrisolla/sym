```sql
CREATE DATABASE sym;

CREATE TABLE amounts (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(45) DEFAULT NULL,
  category varchar(45) DEFAULT NULL,
  method varchar(45) DEFAULT NULL,
  amount_type varchar(45) DEFAULT NULL,
  necessary tinyint DEFAULT NULL,
  date datetime DEFAULT NULL,
  value float(10,2) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY id_UNIQUE (id)
) ENGINE=InnoDB AUTO_INCREMENT=463 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

```