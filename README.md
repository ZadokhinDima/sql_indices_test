# Performance test for InnoDB

## Create users table
```
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    birthday DATE
);
```

## Create data
### Create 40M users using user-generator.py

10 workers, batches of 1000 - took 4625s 
```
python .\user-generator.py 40000000 1000 10
```

## Queries
### Without index:
~20 seconds
```
select count(*) from users where birthday = '1990-01-01';
```
~22 seconds
```
select count(*) from users where birthday = '1990-01-01';
```
### BTREE index:
30-50 ms
```
select count(*) from users where birthday = '1990-01-01';
```
~1 second
```
select count(*) from users where birthday = '1990-01-01';
```
### HASH index:

MySQL requires `ENGINE=MEMORY` table for creating a hash index. Failed to do so for a table with 40M users (not enough memory).

## Play with innodb_flush_log_at_trx_commit

```
innodb_flush_log_at_trx_commit = 0
```

```
innodb_flush_log_at_trx_commit = 1
```

```
innodb_flush_log_at_trx_commit = 2
```
