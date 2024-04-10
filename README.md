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

## Queries and indexes
### Without index:
~20 seconds
```
select sql_no_cache count(*) from users where birthday = '1992-01-04';
```
~22 seconds
```
select sql_no_cache count(*) from users_db.users where birthday BETWEEN '1990-01-01' AND '1999-12-31';
```
### BTREE index:
30-50 ms
```
select sql_no_cache count(*) from users where birthday = '1992-01-04';
```
~1 second
```
select sql_no_cache count(*) from users_db.users where birthday BETWEEN '1990-01-01' AND '1999-12-31';
```
### HASH index:

MySQL requires `ENGINE=MEMORY` table for creating a hash index. Failed to do so for a table with 40M users (not enough memory).

## Inserts and innodb_flush_log_at_trx_commit property

I tested write throughput using Apache Jmeter. Each test was running for 60 seconds. Incert counts for different concurrency and innodb_flush_log_at_trx_commit values are in the table.

| innodb_flush_log_at_trx_commit | 10 users | 25 users | 50 users |
|-------------------------------|-----------|----------|----------|
| 0                             | 250 176   | 376 972  | 722 114  |
| 1                             | 54 375    | 113 461  | 197 073  |
| 2                             | 185 282   | 208 914  | 279 719  |

As expected the fastest inserts are achieved when innodb_flush_log_at_trx_commit = 0. The difference is even bigger with higher concurrency.