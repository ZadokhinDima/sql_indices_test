import sys
from faker import Faker
import pymysql
import time
import threading
from tqdm import tqdm

def generate_users(num_users, batch_size, worker_name):
    # Create a Faker instance
    fake = Faker()

    conn = pymysql.connect(
        host='localhost',
        user='admin',
        password='admin',
        database='users_db',
        cursorclass=pymysql.cursors.DictCursor
    )
    c = conn.cursor()

    # Create a progress bar
    pbar = tqdm(total=num_users, desc=worker_name)

    # Generate and insert users
    users = []
    for count in range(num_users):
        user = (fake.name(), fake.email(), fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True), fake.date_of_birth(minimum_age=18, maximum_age=90))
        users.append(user)

        if (count % batch_size == 0 and count != 0) or count == num_users - 1:
            # Build the INSERT statement
            sql = "INSERT INTO users (username, email, password, birthday) VALUES " + ", ".join("(%s, %s, %s, %s)" for _ in users)

            # Execute the INSERT statement
            c.execute(sql, [item for sublist in users for item in sublist])

            # Update the progress bar
            pbar.update(len(users))

            conn.commit()

            # Clear the users list
            users.clear()

    # Close the connection
    conn.close()

# Define a worker function
def worker(num_users, batch_size, worker_name):
    generate_users(num_users, batch_size, worker_name)

if __name__ == '__main__':
    num_users = int(sys.argv[1])
    batch_size = int(sys.argv[2])
    workers_count = int(sys.argv[3])

    start_time = time.time()

    # Create worker threads
    threads = []
    for i in range(workers_count):
        t = threading.Thread(target=worker, args=(int (num_users / workers_count), batch_size, "Worker" + str(i)))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
