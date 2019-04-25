import requests
from subprocess import run, PIPE, Popen
import base64
import store
import psycopg2
from json import dumps

request = requests.get(f"https://hackattic.com/challenges/backup_restore/problem?access_token={store.key}").json()

dump = request["dump"]
binDump = base64.b64decode(dump)

with open('db.dump', 'wb') as fp:
	fp.write(binDump)

"""
Commands to convert b64dump to psql:
-----------------------------------
createdb testdb

gunzip -c db.dump | psql testdb

"""

run(['createdb', 'testdb'])
gunzip = Popen(['gunzip', '-c', 'db.dump'], stdout=PIPE)
run(['psql', 'testdb'], stdin=gunzip.stdout)

try:
	connect_str = f"dbname='testdb' user={store.dbuser} host='localhost' password={store.dbpass}"

	conn = psycopg2.connect(connect_str)

	cursor = conn.cursor()

	cursor.execute(f"{store.command}")

	ssn = cursor.fetchall()
	ssnList = []
	for num in ssn:
		ssnList.append(*num)

	conn.commit()

	conn.close()

except Exception as e:
	print(e)

finally:
	#Remove tempdb at the end of program
	run(['dropdb', 'testdb'])

	data = dumps({'alive_ssns': ssnList})

	post_request = requests.post(f"https://hackattic.com/challenges/backup_restore/solve?access_token={store.key}", data = data)

	print(post_request.text)


