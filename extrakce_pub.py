import facebook
import requests
import csv


token = "access_token" #add your token no.

graph = facebook.GraphAPI(access_token=token, version="2.7")

def get_data():
    #stáhnu data a oprostím je od závěrečných blábolů o paginaci
    #fetches the data and deletes the pagination info from the end
    post4 = graph.get_object("yourfeed", fields="message,created_time,type,shares,reactions.summary(true).limit(0),comments.summary(true).limit(0)", limit=5) #replace "yourfeed" with the name of your feed, also set your limit to whatever, or delete it if you want all the posts


    post_list = []

    #for i in range(10):
    #i used this just to test if it loads the next page. when i want all the pages, i use:

    while True:
        #the following was deeply inspired by github.com/mobolic - thanks a lot!
        try:
            # Perform some action on each post in the collection we receive from
            # Facebook.

            for post in post4["data"]:
                post_list.append(post)
            # Attempt to make a request to the next page of data, if it exists.
            post4 = requests.get(post4['paging']['next']).json()
        except KeyError:
            # When there are no more pages (['paging']['next']), break from the
            # loop and end the script.
            break
    return post_list

def convert_dict_to_list(dict_list):
    #získaný seznam slovníků potřebuju převést na seznam seznamů. ze slovníků vytáhnu jenom hodnoty
    #a jednu po druhé jako jednotlivé seznamy uložím do velkého seznamu seznamů.
    #what i get from fb graphAPI is a list of dictionaries. i convert it to a list of lists.
    #first of all, i only take the values from the dicts and one at a time save them as lists into a list of lists.
    list_of_lists = []
    for dict in dict_list:
        single_post = []
        for post in dict.values():
            single_post.append(post)
        list_of_lists.append(single_post)

    return list_of_lists

all_posts_list = convert_dict_to_list(get_data())
#it just seems easier to have the output of that function as a global variable...

def convert_to_csv(data):
    #svůj seznam seznamů teď řádek po řádku naskládám do csv souboru.
    #last step is to take this list of lists and row after row write it into a csv file. replace yourfilename with the desired name, of course.
    with open("yourfilename.csv", mode = "w", newline='', encoding = "utf-8") as outfile:
        writer = csv.writer(outfile)
        for row in data:
            writer.writerow(row)

convert_to_csv(all_posts_list)


#toCSV = [{'name':'bob','age':25,'weight':200},
#         {'name':'jim','age':31,'weight':180}]
#keys = toCSV[0].keys()
#with open('people.csv', 'wb') as output_file:
#    dict_writer = csv.DictWriter(output_file, keys)
#    dict_writer.writeheader()
#    dict_writer.writerows(toCSV)

#print(vytahni_data())
