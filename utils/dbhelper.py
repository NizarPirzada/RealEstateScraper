import sqlite3
from sqlite3 import Error
import datetime
import pytz
from utils import helper

database = r"real_estate.sqlite3"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(create_table_sql):
    """ create a table from the create_table_sql statement
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    conn = create_connection(database)
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
    conn.close()


def alter_table(alter_table_sql):
    conn = create_connection(database)
    try:
        c = conn.cursor()
        c.execute(alter_table_sql)
    except Error as e:
        print(e)
    conn.close()


def update_table(update_table_sql):
    conn = create_connection(database)
    try:
        if conn is not None:
            conn.execute(update_table_sql)
            conn.commit()

    except Error as e:
        print("Error in update_table():", e)
    conn.close()


def insert_setting(data):
    conn = create_connection(database)
    lastrowid = 0
    try:
        sql = ''' INSERT INTO setting(setting_id, captcha_string)
                  VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        print("Data inserted!!!. Row Id:", cur.lastrowid)
        lastrowid = cur.lastrowid
    except Error as e:
        print("Error:", e)
    conn.close()
    return lastrowid


def insert_supported_website(data):
    conn = create_connection(database)
    lastrowid = 0
    try:
        sql = ''' INSERT INTO supported_website(supported_website_id, name,url)
              VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        print("Data inserted!!!. Row Id:", cur.lastrowid)
        lastrowid = cur.lastrowid
    except Error as e:
        print("Error:", e)
    conn.close()
    return lastrowid


def insert_configuration(data):
    conn = create_connection(database)
    lastrowid = 0
    try:
        if conn is not None:
            sql = ''' INSERT INTO configuration(configuration_id, emails, start_time, end_time, is_proxy)
                  VALUES(?,?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, data)
            conn.commit()
            print("Data inserted!!!. Row Id:", cur.lastrowid)
            lastrowid = cur.lastrowid
    except Error as e:
        print("Error:", e)
    conn.close()
    return lastrowid


def insert_website(data):
    conn = create_connection(database)
    lastrowid = 0
    try:
        if conn is not None:
            sql = ''' INSERT INTO website(website_id, url, desired_price, supported_website_id, configuration_id)
                  VALUES(?,?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, data)
            conn.commit()
            print("Data inserted!!!. Row Id:", cur.lastrowid)
            lastrowid = cur.lastrowid
    except Error as e:
        print("Error:", e)
    conn.close()
    return lastrowid


def insert_real_estate(data):
    conn = create_connection(database)
    lastrowid = 0
    try:
        if conn is not None:
            sql = ''' INSERT INTO real_estate(real_estate_id, url, file_path, price, area, good, email_sent, website_id)
                  VALUES(?,?,?,?,?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, data)
            conn.commit()
            print("Data inserted!!!. Row Id:", cur.lastrowid)
            lastrowid = cur.lastrowid
    except Error as e:
        print("Error in insert_real_estate():", e)
    conn.close()
    return lastrowid


def update_status(table_name, row_id):
    conn = create_connection(database)
    current_timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    try:
        if conn is not None:
            sql_update_by_id = f"UPDATE {table_name} SET status_id=1, updated_date='{current_timestamp}' where \
                                    {table_name}_id={row_id} "
            print(sql_update_by_id)
            conn.execute(sql_update_by_id)
            conn.commit()

    except Error as e:
        print("Error in update_status():", e)
    conn.close()


def update_record(table_name, data):
    conn = create_connection(database)
    tz = pytz.timezone('Europe/Berlin')
    current_timestamp = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    row_id = data[table_name+"_id"]
    del data[table_name+"_id"]
    keys = []
    values = []
    for key, value in data.items():
        keys.append(key)
        values.append(value)

    try:
        if conn is not None:
            sql_update_by_id = f"UPDATE {table_name} SET"
            for key, value in data.items():
                sql_update_by_id = sql_update_by_id + f" {key}='{value}',"

            sql_update_by_id = sql_update_by_id + f" updated_date='{current_timestamp}' where {table_name}_id={row_id}"

            # sql_update_by_id = f"UPDATE {table_name} SET status_id=1, updated_date='{current_timestamp}' where {
            # table_name}_id={row_id}"
            print(sql_update_by_id)
            conn.execute(sql_update_by_id)
            conn.commit()

    except Error as e:
        print("Error in update_status():", e)
    conn.close()


def get_list_id(table_name):
    conn = create_connection(database)
    list_id = []
    try:
        if conn is not None:
            row_id = table_name + '_id'
            sql_last_id = f"SELECT {row_id} FROM {table_name}"
            cur = conn.execute(sql_last_id)
            rows = cur.fetchall()
            for row in rows:
                list_id.append(row[0])
    except Error as e:
        print("Error:", e)
    conn.close()
    return list_id


def get_last_id(table_name):
    conn = create_connection(database)
    lastrowid = 0
    try:
        if conn is not None:
            row_id = table_name + '_id'
            sql_last_id = f"SELECT max({row_id}) FROM {table_name}"
            cur = conn.execute(sql_last_id)
            lastrowid = cur.fetchone()[0]
            if lastrowid is None:
                lastrowid = 0
    except Error as e:
        print("Error:", e)
    conn.close()
    return lastrowid


def get_all_data(table_name):
    conn = create_connection(database)
    data = []
    try:
        if conn is not None:
            sql_last_id = f"SELECT * FROM {table_name} WHERE is_deleted=0"
            cur = conn.execute(sql_last_id)

            rows = cur.fetchall()

            columns = list(map(lambda x: x[0], cur.description))
            for row in rows:
                row_data = {}
                for c, r in zip(columns, row):
                    row_data[c] = r
                data.append(row_data)

    except Error as e:
        print("Error:", e)
    conn.close()
    return data


def get_unprocessed_data(table_name):
    conn = create_connection(database)
    data = []
    try:
        if conn is not None:
            sql_last_id = f"SELECT * FROM {table_name} where status_id=0"
            cur = conn.execute(sql_last_id)

            rows = cur.fetchall()

            columns = list(map(lambda x: x[0], cur.description))
            for row in rows:
                row_data = {}
                for c, r in zip(columns, row):
                    row_data[c] = r
                data.append(row_data)

    except Error as e:
        print("Error:", e)
    conn.close()
    return data


def get_data_by_id(table_name, row_id):
    conn = create_connection(database)
    data = {}
    try:
        if conn is not None:
            sql_last_id = f"SELECT * FROM {table_name} where {table_name}_id={row_id}"
            cur = conn.execute(sql_last_id)

            row = cur.fetchone()

            columns = list(map(lambda x: x[0], cur.description))
            # for row in rows:
            data = {}
            for c, r in zip(columns, row):
                data[c] = r
            # data.append(row_data)

    except Error as e:
        print("Error in get_configuration_details():", e)
    conn.close()
    return data


def get_data_by_parent_id(table_name, parent_name, parent_id):
    conn = create_connection(database)
    data = []
    try:
        if conn is not None:
            sql_last_id = f"SELECT * FROM {table_name} where {parent_name}_id={parent_id}"
            cur = conn.execute(sql_last_id)

            rows = cur.fetchall()

            columns = list(map(lambda x: x[0], cur.description))
            for row in rows:
                row_data = {}
                for c, r in zip(columns, row):
                    row_data[c] = r
                data.append(row_data)

    except Error as e:
        print("Error in get_configuration_details():", e)
    conn.close()
    return data


def get_duplicate_real_estate(url):
    data = []
    conn = create_connection(database)
    sql_query = """
            SELECT real_estate_id, url, price, area, email_sent, website_id
            FROM real_estate
            WHERE url='{}';
        """.format(url)
    # print(sql_query)

    try:
        if conn is not None:
            cur = conn.execute(sql_query)
            rows = cur.fetchall()
            columns = ["real_estate_id", "url", "price", "area", "email_sent", "website_id"]
            for row in rows:
                dic = {}
                for c, r in zip(columns, row):
                    dic[c] = r
                data.append(dic)
            # print(data)
    except Error as e:
        print("Error:", e)
    return data


def get_scheduled_websites():
    data = []
    conn = create_connection(database)

    sql_query = """
        SELECT website.website_id, website.url, website.desired_price, website.iter_no, website.supported_website_id, 
        website.configuration_id, configuration.emails, configuration.is_proxy, 
        configuration.start_time, configuration.end_time, website.updated_date, website.last_error_datetime, 
        website.error_creation_datetime
        FROM website
        INNER JOIN configuration ON configuration.configuration_id=website.configuration_id
        WHERE configuration.is_deleted is 0 
        AND website.is_deleted is 0
        AND configuration.active_state=1
        ORDER BY  website.iter_no;
    """.format()
    # print(sql_query)
    try:
        if conn is not None:
            cur = conn.execute(sql_query)
            columns = list(map(lambda x: x[0], cur.description))
            rows = cur.fetchall()

            for row in rows:
                dic = {}
                for c, r in zip(columns, row):
                    dic[c] = r

                start_time = dic['start_time']
                end_time = dic['end_time']
                updated_date = dic['updated_date']
                is_scheduled = helper.is_datetime_between(start_time, end_time, "time")
                run_scheduled = helper.run_config_again(updated_date)
                if is_scheduled and run_scheduled:
                    data.append(dic)

            # print(data)
    except Error as e:
        print("Error:", e)
    return data


def main():


    sql_create_supported_website_table = """ CREATE TABLE `supported_website` (
                                            `supported_website_id` int(11) NOT NULL,
                                            `name` varchar(150) NOT NULL,
                                            `url` varchar(200) NOT NULL,
                                            `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                            `updated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                            `is_deleted` int(11) NOT NULL DEFAULT 0,
                                            PRIMARY KEY (`supported_website_id`)
                                            ); 
                                        """

    sql_create_configuration_table = """ CREATE TABLE `configuration` (
                                        `configuration_id` int(11) NOT NULL,
                                        `emails` varchar(500) NOT NULL,
                                        `start_time` time NOT NULL DEFAULT CURRENT_TIME,
                                        `end_time` time NOT NULL DEFAULT CURRENT_TIME,
                                        `active_state` int(11) NOT NULL DEFAULT 1,
                                        `is_proxy` tinyint(4) NOT NULL DEFAULT '0',
                                        `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                        `updated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                        `status_id` int(11) NOT NULL DEFAULT 0,
                                        `is_deleted` int(11) NOT NULL DEFAULT 0,
                                        PRIMARY KEY (`configuration_id`)
                                        );
                                    """

    sql_create_website_table = """ CREATE TABLE `website` (
                                    `website_id` int(11) NOT NULL,
                                    `url` varchar(200) NOT NULL,
                                    `desired_price` double NOT NULL,
                                    `supported_website_id` int(11) NOT NULL,
                                    `configuration_id` int(11) NOT NULL,
                                    `iter_no` int(11) NOT NULL DEFAULT 0, 
                                    `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                    `updated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                    `status_id` int(11) NOT NULL DEFAULT 0,
                                    `is_deleted` int(11) NOT NULL DEFAULT 0,
                                    `last_error_datetime` datetime,
                                    `error_creation_datetime` datetime
                                    PRIMARY KEY (`website_id`)
                                    );
                                """

    sql_create_real_estate_table = """ CREATE TABLE `real_estate` (
                                        `real_estate_id` int(11) NOT NULL,
                                        `url` varchar(200) NOT NULL,
                                        `file_path` varchar(100) NOT NULL,
                                        `price` double NOT NULL,
                                        `area` double NOT NULL,
                                        `good` tinyint(4) NOT NULL DEFAULT '0',
                                        `email_sent` tinyint(4) NOT NULL DEFAULT '0',
                                        `website_id` int(11) NOT NULL,
                                        `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                        `updated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                        `is_deleted` int(11) NOT NULL DEFAULT 0,
                                        PRIMARY KEY (`real_estate_id`)
                                        );
                                    """

    sql_create_setting_table = """ CREATE TABLE `setting` (
                                            `setting_id` int(11) NOT NULL,
                                            `captcha_string` varchar(500) NOT NULL,
                                            `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                            `updated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                            `is_deleted` int(11) NOT NULL DEFAULT 0,
                                            PRIMARY KEY (`setting_id`)
                                            );
                                        """

    # create tables
    # create_table(sql_create_supported_website_table)
    # create_table(sql_create_configuration_table)
    # create_table(sql_create_website_table)
    # create_table(sql_create_real_estate_table)
    # create_table(sql_create_setting_table)

    alter_table_sql = """
        ALTER TABLE website
        ADD last_error_datetime datetime, error_creation_datetime datetime;
    """
    alter_table(alter_table_sql)

    # insert supported websites
    # data = (1, 'Ebay Kleinanzeigen', 'https://www.ebay-kleinanzeigen.de/')
    # insert_supported_website(data)
    # data = (2, 'Immo Welt', 'https://www.immowelt.de/')
    # insert_supported_website(data)
    # data = (3, 'Immo Scout 24', 'https://www.immobilienscout24.de/')
    # insert_supported_website(data)
    #
    # # insert captcha key
    # data = (1, 'db6c05aed5b31c17500f03efe8cc8628')
    # insert_setting(data)
    # data = {
    #         "configuration_id" : 23,
    #         "active_state" : 1
    #     }
    # update_record("c", data)
    # # data = get_scheduled_websites()
    # # for d in data:
    # #     print(d)
    # # current_real_estate = {
    # #     'url' : 'https://www.immowelt.de/expose/2z2bf4w',
    # #     'price': 479000.0,
    # #     'area': 201.0
    # # }
    # # data = get_duplicate_real_estate('https://www.immowelt.de/expose/2z2bf4w')
    # # for d in data:
    # #     print(d)
    # # print(helper.check_duplicate_real_estate(current_real_estate, data))
    # print(get_scheduled_websites())

    # data = {
    #     "website_id": 44,
    #     "is_deleted": 1
    # }
    # update_record('website', data)
if __name__ == '__main__':
    database = r"real_estate.sqlite3"
    # import helper
    main()
