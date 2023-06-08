import json 
import csv
import os #to access the email files
import uuid #for the GUID number generation

#locate where the files are saved
directory = '../Desktop/test'                                            #need to specify where the email files are saved
                                                        
#a list that will store the standard data taken from the email
data_list = []

#a list that will store the item data taken from the email
items_list = []

#loop through all the files in the directory
for filename in os.listdir(directory):
    #set the GUID that the whole file will use
    GUID = str(uuid.uuid4())
    #check if the file is in the correct format
    if filename.endswith('.txt'):                                         #assuming the emails will be stored as a text file
        #set variable in order to read the file
        path_of_file = os.path.join(directory, filename)
        #open and read the current file
        with open(path_of_file, 'r') as file:
            #use counter to go line by line when a new item is found
            counter = 0
            #dictionary to be added to the items list, reset after each item
            items_dictionary = {}
            #loops through each line in the file, checks what it starts with, if the if statment 
            #matches you strip repeditive data and newline character, while adding to the variable.
            #there has to be a better way to do this, wayyyy too many if's, but should work with good runtime on the email files
            for line in file:
                    #if count is not equal to 0 then we are adding the items info to the items dictionary
                    if counter == 4:
                        items_dictionary['Item Total'] = line.replace('Item Total:','').strip()
                        #add current emails items to the list                
                        items_list.append(items_dictionary)
                        #reset the dictionary and counter so that we can have each item be an input
                        items_dictionary = {}
                        counter = 0

                    if counter == 3:
                        items_dictionary['Unit Price'] = line.replace('Unit Price:','').strip()
                        counter +=1
                    
                    if counter == 2:
                        items_dictionary['Quantity'] = line.replace('Quantity:','').strip()
                        counter +=1

                    if counter == 1:
                        items_dictionary['Description'] = line.replace('Description:','').strip()
                        counter +=1
                    

                    if line.startswith('Merchant'):
                        email_Merchant = line.replace('Merchant :','').strip()
                    if line.startswith('Date/Time'):
                        email_DateTime = line.replace('Date/Time :','').strip()
                    if line.startswith('Invoice'):
                        email_Invoice = line.replace('Invoice :','').strip()
                    if line.startswith('Description :'):
                        email_Description = line.replace('Description :','').strip()
                    if line.startswith('Response'):
                        email_Response = line.replace('Response :','').strip()
                    if line.startswith('Customer ID'):
                        email_Customer_ID = line.replace('Customer ID :','').strip()
                    if line.startswith('First Name'):
                        email_First_Name = line.replace('First Name :','').strip()
                    if line.startswith('Last Name'):
                        email_Last_Name = line.replace('Last Name :','').strip()
                    if line.startswith('Company'):
                        email_company = line.replace('Company :','').strip()
                    if line.startswith('Address'):
                        email_Address = line.replace('Address :','').strip()
                    if line.startswith('City'):
                        email_City = line.replace('City :','').strip()
                    if line.startswith('State/Province'):
                        email_StateProvince = line.replace('State/Province :','').strip()
                    if line.startswith('Zip/Postal Code'):
                        email_ZipPostal_Code = line.replace('Zip/Postal Code :','').strip()
                    if line.startswith('Country'):
                        email_Country = line.replace('Country :','').strip()
                    if line.startswith('Phone'):
                        email_Phone = line.replace('Phone :','').strip()
                    if line.startswith('Fax'):
                        email_Fax = line.replace('Fax :','').strip()

                    #we found a new item
                    if line.startswith('Item:'):
                        #update the counter in order to get its information on the following lines
                        counter += 1
                        #give the item a matching GUID
                        items_dictionary['GUID'] = GUID
                        items_dictionary['Item'] = line.replace('Item:','').strip()
                    
                    #break out of the loop when it hits info we do not need
                    if line.startswith('==== CUSTOMER SHIPPING INFORMATION ='):
                        break

            
            #this is a dictionary storing the feilds desired with the current emails data, along with a unique GUID 
            data_dictionary = {

                'GUID' : GUID,
                'Merchant' : email_Merchant,
                'Date/Time' : email_DateTime,
                'Invoice' : email_Invoice,
                'Description' : email_Description,
                'Response' : email_Response,
                'Customer ID': email_Customer_ID,
                'First Name' : email_First_Name,
                'Last Name' : email_Last_Name,
                'Company' : email_company,
                'Address' : email_Address,
                'City' : email_City,
                'State/Province' : email_StateProvince,
                'Zip/Postal Code' : email_ZipPostal_Code,
                'Country' : email_Country,
                'Phone' : email_Phone,
                'Fax' : email_Fax

            }           

    #add current emails data to the list                
    data_list.append(data_dictionary)






#write the standard data into the json file
with open("../Desktop/filtered_json/standard_data.json", "w") as file:      #need to specify where the json files are saved
        json.dump(data_list, file,indent=1)
        file.write('\n')

#write the item data into the json file
with open("../Desktop/filtered_json/item_data.json", "w") as file:          #need to specify where the json files are saved
        json.dump(items_list, file,indent=1)
        file.write('\n')
  





#converts the json file for standard data into a csv
with open('../Desktop/filtered_json/standard_data.json') as json_file:      #need to specify where the json files are taken from
    jsondata = json.load(json_file)
 
data_file = open('../Desktop/filtered_csv/standard_data.csv', 'w', newline='')  #need to specify where the csv files are saved
csv_writer = csv.writer(data_file)
 
count = 0
for data in jsondata:
    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(data.values())
 
data_file.close()


#converts the json file for item data into a csv
with open('../Desktop/filtered_json/item_data.json') as json_file:          #need to specify where the json files are taken from
    jsondata = json.load(json_file)
 
data_file = open('../Desktop/filtered_csv/item_data.csv', 'w', newline='')  #need to specify where the csv files are saved
csv_writer = csv.writer(data_file)
 
count = 0
for data in jsondata:
    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(data.values())
 
data_file.close()