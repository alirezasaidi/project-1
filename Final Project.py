import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
from sklearn import linear_model
import numpy as np

model_list = []
year_list = []
milage_list = []
gheymat_list = []

pages = input('How many pages of the truecar site should we check?: ')
for q in range(1, int(pages)+1):
    r = requests.get('https://www.truecar.com/used-cars-for-sale/listings/?page='+str(q))

    soup = BeautifulSoup(r.text, 'html.parser')
    modelha = soup.find_all(class_="vehicle-header-make-model text-truncate")
    yearha = soup.find_all(class_="vehicle-card-year font-size-1")
    milageha = soup.find_all(class_="d-flex w-100 justify-content-between")
    gheymatha = soup.find_all(class_="heading-3 margin-y-1 font-weight-bold")
     
    for model in modelha:
        model_list.append(model.text)
    
    for year in yearha:
        year_list.append(year.text)
    
    for milage in milageha:
        milage_list.append(milage.text)
        for j in range(0, len(milage_list)):
            b = milage_list[j].split()
            milage_list[j] = b[0]
            milage_list[j] = milage_list[j].replace(',', '')
    
    for gheymat in gheymatha:
        gheymat_list.append(gheymat.text)
        for k in range(0, len(gheymat_list)):
            gheymat_list[k] = gheymat_list[k].replace('$', '')
            gheymat_list[k] = gheymat_list[k].replace(',', '')

DB_NAME = 'Project_Jadi'

TABLES = {}
TABLES['Final_Project'] = (
    "CREATE TABLE `Final_Project` ("
    "  `Model` varchar(100),"
    "  `Year` varchar(100),"
    "  `Mileage` varchar(100),"
    "  `Price` varchar(100)"
    ") ENGINE=InnoDB")

username = input('Please insert your database user: ')
passwordd = input('Please insert your database password: ')
cnx = mysql.connector.connect(user=username, password=passwordd,host='127.0.0.1')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for Final_Project in TABLES:
    table_description = TABLES[Final_Project]
    try:
        print("Creating table {}: ".format(Final_Project), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cnx = mysql.connector.connect(user=username, password=passwordd,host='127.0.0.1', database=DB_NAME)
cursor = cnx.cursor()

add_car = ("INSERT IGNORE INTO Final_Project (Model, Year, Mileage, Price) VALUES (%s, %s, %s, %s)")

data_car = (model_list, year_list, milage_list, gheymat_list)

for i in range(0, len(model_list)):
    data_car = (model_list[i], year_list[i], milage_list[i], gheymat_list[i])
    cursor.execute(add_car, data_car)

cnx.commit()
cursor.close()
cnx.close()

barazesh = []
barazesh_nahaie = []
for z in range(0, len(model_list)):
    barazesh.append([model_list[z], year_list[z], milage_list[z], gheymat_list[z]])
    if 'Toyota' in barazesh[z][0]:
        barazesh_nahaie.append(barazesh[z])

for v in range(0, len(barazesh_nahaie)):
    if '4Runner' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota 4Runner', '16')
    if 'Avalon' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Avalon', '14')
    if 'C-HR' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota C-HR', '3')
    if 'Camry' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Camry', '6')
    if 'Corolla' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Corolla', '1') 
    if 'Corolla Cross' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Corolla Cross', '4') 
    if 'Corolla Hatchback' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Corolla Hatchback', '2')
    if 'GR Supra' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota GR Supra', '18') 
    if 'GR86' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota GR86', '9') 
    if 'Highlander' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Highlander', '13') 
    if 'Land Cruiser' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Land Cruiser', '20') 
    if 'Prius' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Prius', '5') 
    if 'Prius Prime' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Prius Prime', '10') 
    if 'RAV4' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota RAV4', '7') 
    if 'RAV4 Prime' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota RAV4 Prime', '17') 
    if 'Sequoia' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Sequoia', '19') 
    if 'Sienna' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Sienna', '12') 
    if 'Tacoma' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Tacoma', '8') 
    if 'Tundra' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Tundra', '15') 
    if 'Venza' in barazesh_nahaie[v][0]:
       barazesh_nahaie[v][0] = barazesh_nahaie[v][0].replace('Toyota Venza', '11') 

x = []
y = []
for u in range(0, len(barazesh_nahaie)):
    x.append((barazesh_nahaie[u][:3]))
    y.append(barazesh_nahaie[u][3])

for ozv in x:
   for adad in range(0, 3):
      ozv[adad] = float(ozv[adad])

y = [float(ozv2) for ozv2 in y]

che_modeli = (input('What model of Toyota to check?: ')).title()
if che_modeli == '4Runner':
   che_modeli = 16
if che_modeli == 'Avalon':
   che_modeli = 14
if che_modeli == 'C-HR':
   che_modeli = 3
if che_modeli == 'Camry':
   che_modeli = 6
if che_modeli == 'Corolla':
   che_modeli = 1
if che_modeli == 'Corolla Cross':
   che_modeli = 4
if che_modeli == 'Corolla Hatchback':
   che_modeli = 2
if che_modeli == 'GR Supra':
   che_modeli = 18
if che_modeli == 'GR86':
   che_modeli = 9 
if che_modeli == 'Highlander':
   che_modeli = 13 
if che_modeli == 'Land Cruiser':
   che_modeli = 20
if che_modeli == 'Prius':
   che_modeli = 5
if che_modeli == 'Prius Prime':
   che_modeli = 10
if che_modeli == 'RAV4':
   che_modeli = 7 
if che_modeli == 'RAV4 Prime':
   che_modeli = 17
if che_modeli == 'Sequoia':
   che_modeli = 19 
if che_modeli == 'Sienna':
   che_modeli = 12
if che_modeli == 'Tacoma':
   che_modeli = 8 
if che_modeli == 'Tundra':
   che_modeli = 15
if che_modeli == 'Venza':
   che_modeli = 11

che_sali = int(input('Year of car production: '))
che_mileagi = int(input('Mileage of car: '))

regr = linear_model.LinearRegression()
regr.fit (x, y)
answer = regr.predict([[che_modeli, che_sali, che_mileagi]])

print ('The approximate price of your car:', int(answer[0]), '$')

