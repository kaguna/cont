import pandas as pd
import sqlite3
import numpy as np
from IPython.display import HTML

"""
Create a database named contractors and a table one inside the database with parameters
Create Table_one of unique contractors
"""
conn = sqlite3.connect("contractor.sql")
create_table_one = "create TABLE unique_contractor (id integer primary key, Global_Vendor_Name varchar)"
conn.execute(create_table_one)

# Insert data to table_one
insert_contractor = "insert into unique_contractor (Global_Vendor_Name) " \
                    "select distinct Global_Vendor_Name from unique_contractor;"
conn.execute(insert_contractor)

"""
Creating Table Two with the following parameters 
The second table should include an id (primary key),
department, actions (number of actions), dollars 
(dollars obligated) and contractor_id as a foreign key
to the contractors table
"""

create_table_two = "create TABLE contractor_data (dataid integer primary key,department text, " \
                   "actions int, dollars real,  name text, contractor_id int )"
conn.execute(create_table_two)
nom_query = '''
select contractor_data.department as department, 
contractor_data.actions as actions, contractor_data.dollars as dollars, 
contractor_data.name as name, unique_contractor.id as contractor_id from
contractor_data INNER JOIN unique_contractor
ON contractor_data.name=unique_contractor.Global_Vendor_Name ;'''

nom_query_execute = conn.execute(nom_query).fetchall()
insert_table_two = '''insert into contractor_data (department,actions,dollars,name,contractor_id ) 
values (?,?, ?,?, ?);'''
conn.executemany(insert_table_two, nom_query_execute)

"""
question one 
1. What are the total actions and dollars obligated by department?
"""

query = ''' SELECT sum(actions),sum(dollars) 
FROM contractor_data
GROUP BY department;'''

first_output = conn.execute("SELECT department, sum(actions),sum(dollars) FROM "
                            "contractor_data GROUP BY department ;").fetchall()

dept = []
actions = []
dollars = []

for output in first_output:
    dept.append(output[0])
    actions.append(output[1])
    dollars.append(output[2])


data = pd.DataFrame({'Department': dept, 'Total_actions': actions, 'Dollars': dollars})
HTML(data.to_html())

"""
Question Two 
2. What is Johns Hopkins University's number of actions and dollars by department?
"""

second_output = conn.execute("SELECT department, sum(actions),sum(dollars) FROM "
                             "contractor_data where name = 'JOHNS HOPKINS UNIVERSITY' "
                             "GROUP BY department ;").fetchall()

dept = []
actions = []
dollars = []

for output in second_output:
    dept.append(output[0])
    actions.append(output[1])
    dollars.append(output[2])


data = pd.DataFrame({'Department': dept, 'Total_actions': actions, 'Dollars': dollars})
HTML(data.to_html())

"""
Question Three 
3. What is the count of vendors by deparments
(how many vendors received contracts from 1 department,
2 departments, etc.). 
"""
third_output = conn.execute("SELECT name, count (*) department FROM contractor_data GROUP BY name ;").fetchall()
# Declaring empty array to store query data
y = []
for output in third_output:
    y.append(output[1])

"""
Using bincount to find number of contractors with 1 department, 2 department & so on ...
"""
bincount = np.bincount(y)
data = pd.DataFrame({'Department': list(range(len(bincount))), 'Num_of_vendors': bincount})
HTML(data[1:].to_html())

