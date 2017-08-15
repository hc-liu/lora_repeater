import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='lora',
                             password='lora',
                             db='lora',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Read a single record
        #sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        sql = "SELECT netid_group, appskey, nwkskey  FROM table_netid"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()