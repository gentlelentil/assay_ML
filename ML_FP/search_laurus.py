import mariadb
import sys

username = 'rouser'
database = 'laurus.fmp-berlin.de'
las_port = 3306
CID = 2244

query = f'SELECT * FROM aggregator.pubchem_compound WHERE pubchem_id = {CID};'
columns = f'SELECT * FROM INFORMATION_SCHEME.COLUMNS WHERE TABLE_NAME = N\'aggregator.pubchem_compound\''

try:
    conn = mariadb.connect(
        user = username,
        host = database,
        password = None,
        port = las_port,
    )
except mariadb.Error as e:
    print(f'Error connecting to laurus: {e}')
    sys.exit(1)

cur = conn.cursor()

cur.execute(query)

info = cur.fetchall()

for i in info:
    print(i[5])

#SMILES canonical is index 5
def query_db(query):
    try:
        conn = mariadb.connect(
            user = username,
            host = database,
            password = None,
            port = las_port,
    )

    except mariadb.Error as e:
        print(f'Error connecting to laurus: {e}')
        sys.exit(1)

    cur = conn.cursor()

    try:
        cur.execute(query)
    
    except mariadb.Error as e:
        print(f'Error in query: {e}')
        sys.exit(1)
    
    info = cur.fetchall()
    
    conn.close()

    return info
