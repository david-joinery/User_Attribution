import csv
import json
from urllib.request import urlopen, urlretrieve
import random
from datetime import datetime
from os import listdir
from os.path import isfile, join
import Levenshtein
import pdb


def strip_names(name_1,name_2):
    name_1 = name_1.strip('[\']"\s')
    name_2 = name_2.strip('[\']"\s')
    name_1 = name_1.partition('@')[0]
    name_2 = name_2.partition('@')[0]
    name_1 = name_1.replace(" ", "")
    name_2 = name_2.replace(" ", "")
    name_1 = name_1.lower()
    name_2 = name_2.lower()
    return name_1, name_2


def calculate_lev_distance(name_1, name_2):
    return Levenshtein.jaro(name_1, name_2)

def update_dict(name_dict,name,new_name,dist):
    name_tuple = (new_name,dist)
    if name in name_dict.keys():
        #print('repeat')
        if dist > name_tuple[1]:
            name_dict.update(name = name_tuple)
    else:
        #print('new')
        name_dict[name] = name_tuple


#joint lists
fb_names = []
joinery_names = []
joinery_emails = []
joint_names = {}
joint_emails = {}
name_tuple = ()


#Retrieve List A
Joinery_Submitted_Listers_Data = 'https://app.periscopedata.com/api/joinery/chart/csv/6f01842a-d46c-a7d8-7863-9392a91441c9'

#Retrieve List C
All_Joinery_Users_Data = 'https://app.periscopedata.com/api/joinery/chart/csv/da87726f-452b-8210-919d-154d62087875'

#Ingest Data
Joinery_Submitted_Listers,Submitted_Headers =urlretrieve(Joinery_Submitted_Listers_Data)
All_Joinery_Users,Joinery_Headers = urlretrieve(All_Joinery_Users_Data)

Submitted_csv_file = open(Joinery_Submitted_Listers,'rt')
Joinery_Submitted_Listers_Csv = csv.reader(Submitted_csv_file,delimiter='\n')
next(Joinery_Submitted_Listers_Csv)

All_Joinery_Users_file = open(All_Joinery_Users,'rt')
All_Joinery_Users_Csv = csv.reader(All_Joinery_Users_file,delimiter = '\n')
next(All_Joinery_Users_Csv)



##loop through csv rows for Submitted_Listers
for row in Joinery_Submitted_Listers_Csv:
    row = str(row).split(',')
    #print(row)
    #assign data to individual variables
    fb_name, fb_fn, fb_ln, fb_date, fb_custom_aud_id, fb_aud_name, fb_custom_aud_id = row
    if fb_name != '""' and fb_name != '':
        fb_names.append(fb_name)
        


for row in All_Joinery_Users_Csv:
    row = str(row).split(',')
    if len(row) <= 5:
        j_name, j_fn, j_ln, j_email, j_lister = row
        if j_name != '""' and j_name != '':
            joinery_names.append(j_name)
        joinery_emails.append(j_email)
                
    

#sort lists
fb_names.sort()
joinery_names.sort()


csv_metrics = open('attr_metrics.csv', 'w', newline='')
fieldnames = ['name','matched name','distance']
attr_writer = csv.writer(csv_metrics, fieldnames)
attr_writer.writerow(fieldnames)


i = 0
for name in fb_names:
    j = 0
    for j_name in joinery_names:
        name_1, name_2 = strip_names(name, j_name)
        if name_1 != "" and name_2 != "":
            L_dist = calculate_lev_distance(name_1,name_2)
            
            if L_dist > .8:
                update_dict(joint_names, name_1, name_2, L_dist)
                #print(name_1 + "||" +  name_2 + "||" +  str(L_dist))
                #print('--------------------------')
                #if j > 1000:
                    #break
                j+=1
    k = 0            
    for j_email in joinery_emails:
        name_1, name_2 = strip_names(name, j_email)
        if name_1 != "" and name_2 != "":
            L_dist = calculate_lev_distance(name_1,name_2)

            if L_dist >.6:  
                update_dict(joint_emails, name_1, j_email, L_dist)
                #if k >1000:
                    #break
        #if i >1000:
            #break
        i+=1



print('NAMES:')
print('-----------------------------------------------------')
print('-----------------------------------------------------')
for name in joint_names:
    print(name,": ",joint_names[name])
    attr_writer.writerow([name,joint_names[name][0],joint_names[name][1]])
print('\n')
print('\n')

print('EMAILS:')
print('-----------------------------------------------------')
print('-----------------------------------------------------')
attr_writer.writerow(['name','matched email','distance'])
for x in joint_emails:
    attr_writer.writerow([name,joint_emails[x][0],joint_emails[x][1]])
    print(x,": ",joint_emails[x])
#pdb.set_trace()
