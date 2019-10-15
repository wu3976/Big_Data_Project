import logging

log=logging.getLogger()
log.setLevel('INFO')
handler=logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s[%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)


# creating a new keyspace named keyspace

# session: the session of cassandra cluster in which keyspace would be created
# keyspace: the string name of keyspace

# requires: session is an active cluster session
# ensures: a keyspace named keyspace is created in the session.
def createKeySpace(session, keyspace):

    log.info("Creating keyspace...")
    try:
        # session.execute: just like type in the code in cqlsh
        # firstly drop the existing keyspace.
        # In the future, function of checking if keyspace exists would be added
        session.execute("""DROP KEYSPACE %s""" % keyspace)
        # create the keyspace, using incoming keyspace aurgument
        session.execute("""CREATE KEYSPACE %s
        WITH replication = {'class':'SimpleStrategy', 'replication_factor':'2'}""" % keyspace)

        log.info("setting keyspace...")
        session.set_keyspace(keyspace)

        log.info("creating table...")
        # create a table named table_1
        session.execute("""
        CREATE TABLE table_1(
        Filename text, 
        Time_of_Upload text, 
        Prediction_Result text, 
        PRIMARY KEY (Filename, Time_of_Upload)
        )
        """ )

    except Exception as e:
        log.error("Some errors happened!")
        log.error(e)


# insert a row of data into a table in the session.

# session: the session of keyspace in which data would be added.
# file_name: one of the data, representing the string file name of uploaded file.
# Time_of_upload: the other one.
# Prediction_Result: the third one.

# requires: [session exists and activated, a table with appropriate format is used]
# and [file_name, upload_time, result are string objects]
# ensures: the corresponding data are added to the table.
def insert_data(session, file_name, upload_time, result):
    session.execute("""INSERT INTO table_1 (Filename, Time_of_Upload, Prediction_Result)
                                VALUES ('%s', '%s', '%s')
                                """ % (file_name, upload_time, result)
                    )

