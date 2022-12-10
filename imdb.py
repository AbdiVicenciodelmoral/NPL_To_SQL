#!/usr/bin/python
import psycopg2
from config import config


class IMDB_Connect():
    def __init__(self,query):
        self.query = query
        self.rows = []

    def connect(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            
            conn = psycopg2.connect(**params)
    		
            # create a cursor
            cur = conn.cursor()
            
    	# execute a statement
            
            sql = "SELECT COUNT(title) FROM imdb.imdb WHERE imdb.director LIKE '%Mel Gibson%'"
            cur.execute(self.query)
                   
            #cur.execute("SELECT rank, title, actors from imdb.imdb where actors LIKE '%Bradley Cooper%'")
            
            #cur.execute("SELECT title, actors, REPLACE(ACTORS, ',', ' ') from imdb.imdb where REPLACE(actors), ',', ' ') LIKE '%Bradley Cooper%'")
                    
            #cur.execute("SELECT title, revenue from imdb.imdb WHERE directors LIKE 'S%' ")

            # display the PostgreSQL database server version
           
        
            for row in cur:
                self.rows.append(','.join(str(i) for i in row))

            
           
    	# close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')



def main():
   sql = IMDB_Connect('TEST')
   sql.connect()
   print(sql.rows)

if __name__ == '__main__':
    main()