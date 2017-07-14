import csv
import flask
import json
from urllib.request import urlopen, urlretrieve
import random
from datetime import datetime
from os import listdir
from os.path import isfile, join
import Levenshtein
import pdb

app = flask.Flask(__user-attribution-metrics__)
@app.route("/")

def strip_names(name_1,name_2, reverse):
    name_1 = name_1.strip('[\']\"\s')
    name_2 = name_2.strip('[\']\"\s')
    #name_1 = name_1.partition('@')[0]
    #name_2 = name_2.partition('@')[0]
    #print(name_1,name_2)
    #print(name_1,name_2)
    fn = name_1.partition(' ')[0]
    ln = name_1.partition(' ')[2]
    l = 0
    if reverse:
        name_1, l = reverse_names(fn, ln)
    else: 
        name_1 = fn + ln
    fn = name_2.partition(' ')[0]
    ln = name_2.partition(' ')[2]
    if reverse:
        name_2, l = reverse_names(fn, ln)
    else:
        name_2 = fn + ln
        l = len(fn)
    name_1 = name_1.lower()
    name_2 = name_2.lower()
    return name_1, name_2, l

def reverse_names(fn, ln):
    name = ln + fn
    l = len(ln)
    return name, l 

def get_length(name):
    return len(name)


def calculate_lev_distance(name_1, name_2, ln_length, jw):
    
    if jw:
        #print(name_2)
        #print(ln_length)
        if ln_length <= 5 and ln_length > 0: 
            return Levenshtein.jaro_winkler(name_1,name_2, .1)
        else:
            return Levenshtein.jaro_winkler(name_1,name_2, .13)

    else:  
        return Levenshtein.jaro(name_1, name_2)


def update_dict(name_dict,name,new_name,dist):
    name_tuple = (new_name,dist)
    if name in name_dict.keys():
        #print(name, name_tuple, name_dict[name])
        #print('repeat')
        if dist > name_dict[name][1]:
            name_dict[name] = name_tuple
            #print('updated')
            #print(name, name_dict[name])
    else:
        #print('new')
        name_dict[name] = name_tuple
        #2print('new')
    return name_dict

def index():
    #joint lists
    no_names = 0
    #no_emails = 0
    fb_names = []
    joinery_names = []
    #joinery_emails = []
    joint_names_1 = {}
    joint_names_2 = {}
    joint_names_3 = {}
    joint_names_4 = {}
    #joint_emails = {}
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
        if fb_name != '""' and fb_name != '' and fb_name != '[\'' and fb_name != '["':
            #print(fb_name)
            fb_names.append(fb_name)
            


    for row in All_Joinery_Users_Csv:
        row = str(row).split(',')
        if len(row) <= 5:
            j_name, j_fn, j_ln, j_email, j_lister = row
            if j_name != '""' and j_name != '' and j_name != '[\'' and j_name != '["':
                #print(j_name)
                joinery_names.append(j_name)
            else:
                no_names += 1
            #if j_email != '' and j_email != '""' and j_email != '[\'' and j_email != '["':    
                #joinery_emails.append(j_email)
            #else:
                #no_emails +=1

               

              

            
                    
        

    #sort lists
    fb_names.sort()
    joinery_names.sort()


    csv_metrics = open('attr_metrics.csv', 'w', newline='')
    fieldnames = ['name','matched name','fn first jaro distance', 'fn first jaro-winkler distance', 'ln first jaro distance', 'ln first jaro-winkler distance']
    attr_writer = csv.writer(csv_metrics, fieldnames)
    attr_writer.writerow(fieldnames)


    i = 0
    for name in fb_names:
        j = 0
        for j_name in joinery_names:
            name_1, name_2, l = strip_names(name, j_name, False)
            rname_1, rname_2, rl = strip_names(name, j_name, True)
            if name_1 != "" and name_2 != "":
                fn_first_j_dist = calculate_lev_distance(name_1, name_2, l, False)
                fn_first_jw_dist = calculate_lev_distance(name_1, name_2, l, True)
                ln_first_j_dist = calculate_lev_distance(rname_1, rname_2, rl , False)
                ln_first_jw_dist = calculate_lev_distance(rname_1, rname_2, rl , True)
                
                
                joint_names_1 = update_dict(joint_names_1, name_1, name_2, fn_first_j_dist)
                joint_names_2 = update_dict(joint_names_2, name_1, name_2, fn_first_jw_dist)
                joint_names_3 = update_dict(joint_names_3, name_1, name_2, ln_first_j_dist)
                joint_names_4 = update_dict(joint_names_4, name_1, name_2, ln_first_jw_dist)
                    



    print('NAMES:')
    print('-----------------------------------------------------')
    print('-----------------------------------------------------')
    for name in joint_names_1:
        #print(name,": ",joint_names_[name])
        attr_writer.writerow([name,joint_names_1[name][0],joint_names_1[name][1],joint_names_2[name][1], joint_names_3[name][1], joint_names_4[name][1]])
    print('\n')
    print('\n')

    print('no names:',no_names)
    #print('no emails',no_emails)
