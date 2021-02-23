import sqlite3

class DatabaseOperations:
    '''
    Performs Database operation on the given database
    '''
    def __init__(self,database_name):
        '''Initializing the database and its cursors'''
        self.database_name = database_name
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS urls(short_url char(5) PRIMARY KEY NOT NULL,actual_url varchar(500) NOT NULL)")
        self.connection.commit()
    
    def close_connection(self):
        '''Closes the connection to Database'''
        self.connection.close()
    
    def check_if_exists(self,short_url):
        '''Returns True if a shortened url exists in DB else returns False'''
        sql_query='''SELECT * FROM urls where short_url=?'''
        check_tuple = (short_url,)
        self.cursor.execute(sql_query,check_tuple)
        output = self.cursor.fetchone()
        if not output:
            return False
        else:
            return True
        
    def insert_into_database(self,short_url,actual_url):
        '''Inserts a new row into the table.
        Return True if the insert is successfull else returns False.'''
        try:
            sql_query = '''INSERT INTO urls VALUES(?,?)'''
            input_tuple = (short_url,actual_url)
            self.cursor.execute(sql_query,input_tuple)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"[INSERTION FAILED]: e")
            return False
    
    def get_actual_url(self,short_url):
        '''Get the actual_url from the short_url from DB.
        Returns False if no URL is found '''
        sql_query = '''SELECT actual_url FROM urls where short_url=?'''
        check_tuple = (short_url,)
        self.cursor.execute(sql_query,check_tuple)
        output = self.cursor.fetchone()
        if not output:
            return False
        else:
            return output
        
