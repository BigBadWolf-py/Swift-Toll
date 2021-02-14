import MySQLdb
from datetime import datetime
from common import utils


class BaseDAO:
    def __init__(self):
        pass

    @staticmethod
    def __get_connection():
        # Open database connection
        try:
            db = MySQLdb.connect("st-db.cl03quqjypwx.us-west-2.rds.amazonaws.com", "swiftoll", "Swiftoll#1", "db_st")
            #db = MySQLdb.connect("localhost", "root", "", "db_st")
            return db
        except MySQLdb.MySQLError:
            print("Can't connect to mysql server")

    @staticmethod
    def __close_connection(db):
        # Disconnect from mysql server
        if db:
            db.close()

    @classmethod
    def _get_item(cls, sql):
        db = cls.__get_connection()
        di = {}
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            if results:
                for row in results:
                    for idx, field in enumerate([i[0] for i in cursor.description]):
                        di.update({field: row[idx]})
                return di
        except MySQLdb.MySQLError:
            print "Error: unable to fetch data"
        finally:
            cls.__close_connection(db)

    @classmethod
    def _get_items(cls, sql):
        db = cls.__get_connection()
        di = []
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            if results:
                for row in results:
                    d = {}
                    for idx, field in enumerate([i[0] for i in cursor.description]):
                        d.update({field: row[idx]})
                    di.append(d)
                return di
        except MySQLdb.Error as e:
            print "Error: unable to fetch data"
        finally:
            cls.__close_connection(db)

    @classmethod
    def insert(cls, object, table, uuid=""):
        db = cls.__get_connection()
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        try:
            if object.get('created_on'):
                object['created_on'] = utils.get_str_from_date(datetime.now())
            if object.get('updated_on'):
                object['updated_on'] = utils.get_str_from_date(datetime.now())

            sql = 'INSERT INTO {0}('.format(table)
            if uuid:
                sql += 'id,'
            for key in object:
                if key == 'id' or key == 'unique_id' or object[key] is None:
                    continue
                sql += key + ","
            sql = sql[:-1]
            sql += ") VALUES ("
            if uuid:
                sql += "'" + uuid + "',"
            for key in object:
                if key == 'id' or key == 'unique_id' or object[key] is None:
                    continue
                if type(object[key]) in [str, unicode]:
                    sql += "'" + object[key] + "',"
                elif type(object[key]) == list:
                    sql += "'" + ','.join(object[key]) + "',"
                else:
                    sql += str(object[key]) + ","

            sql = sql[:-1]
            sql += ")"
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
            return cursor.lastrowid
        except MySQLdb.Error as e:
            print e[1]
            # Rollback in case there is any error
            db.rollback()
            return None
        finally:
            cls.__close_connection(db)

    @classmethod
    def update(cls, object, table, keys):
        db = cls.__get_connection()
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        try:
            if object.get('updated_on'):
                object['updated_on'] = utils.get_str_from_date(datetime.now())

            sql = 'UPDATE {0} SET '.format(table)
            for key in keys:
                if object[key]:
                    if type(object[key]) in [str, unicode]:
                        sql += "{0}='{1}',".format(key, object[key])
                    elif type(object[key]) == list:
                        sql += "'" + ','.join(object[key]) + "',"
                        sql += "{0}='{1}',".format(key, ','.join(object[key]))
                    else:
                        sql += "{0}={1},".format(key, object[key])
                else:
                    sql += "{0}=null,".format(key)
            sql = sql[:-1]
            try:
                int(object['id'])
                sql += " WHERE id={0}".format(object['id'])
            except:
                sql += " WHERE id='{0}'".format(object['id'])
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
            return cursor.lastrowid
        except MySQLdb.Error as e:
            print e[1]
            # Rollback in case there is any error
            db.rollback()
            return None
        finally:
            cls.__close_connection(db)
