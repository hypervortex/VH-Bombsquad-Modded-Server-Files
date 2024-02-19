from tools import mongo
#by SARA

#check the complaint of player and add in mongoDB xD
def update_complaint_count(useracid, myself, mongo):
    # Assuming count is initialized somewhere before this block of code
    count = 0
    index = None  # Initialize index to None

    # Retrieve the latest document from MongoDB
    complainter = mongo.complaint_count.find_one() or {'complainter': {'pb_id': [], 'name': [], 'count': []}}

    #print("Before checking:")
    #print("Pbid:", complainter['complainter']['pb_id'])
    #print("Name:", complainter['complainter']['name'])
    #print("Count:", complainter['complainter']['count'])

    if useracid in complainter['complainter']['pb_id']:
        # Player is already present; increase the count
        index = complainter['complainter']['pb_id'].index(useracid)

        # Ensure 'count' has the correct length
        while len(complainter['complainter']['count']) <= index:
            complainter['complainter']['count'].append(0)

        #print("After checking:")
        #print("Pbid:", complainter['complainter']['pb_id'])
        #print("Name:", complainter['complainter']['name'])
        #print("Count:", complainter['complainter']['count'])
        #print("Index:", index)

        # Now, safely update the count
        existing_count = complainter['complainter']['count'][index]
        complainter['complainter']['count'][index] = existing_count + 1
        mongo.complaint_count.delete_many({})
        mongo.complaint_count.insert_one(complainter)
        #print("After adding:")
        #print("Count:", complainter['complainter']['count'])
        #print(f"Incrementing the count in mongo db with id {useracid} ")
    else:
        # Player is new; add player details and initialize count
        complainter['complainter']['pb_id'].append(useracid)
        complainter['complainter']['name'].append(myself)
        complainter['complainter']['count'].append(1)  # Initialize count as a list for the new player
        mongo.complaint_count.delete_many({})
        mongo.complaint_count.insert_one(complainter)
        #print("After adding:")
        #print("Pbid:", complainter['complainter']['pb_id'])
        #print("Name:", complainter['complainter']['name'])
        #print("Count:", complainter['complainter']['count'])
        #print(f"Successfully added id in mongo db")


#check complaints of player and add in mongo db :))
def update_complaints_count(acid, offender, mongo):
    # Assuming count is initialized somewhere before this block of code
    count = 0
    index = None  # Initialize index to None

    # Retrieve the latest document from MongoDB
    complaints = mongo.complaints_count.find_one() or {'complaints': {'pb_id': [], 'name': [], 'count': []}}

    #print("Before checking:")
    #print("Pbid:", complaints['complaints']['pb_id'])
    #print("Name:", complaints['complaints']['name'])
    #print("Count:", complaints['complaints']['count'])

    if acid in complaints['complaints']['pb_id']:
        # Player is already present; increase the count
        index = complaints['complaints']['pb_id'].index(acid)

        # Ensure 'count' has the correct length
        while len(complaints['complaints']['count']) <= index:
            complaints['complaints']['count'].append(0)

        #print("After checking:")
        #print("Pbid:", complaints['complaints']['pb_id'])
        #print("Name:", complaints['complaints']['name'])
        #print("Count:", complaints['complaints']['count'])
        #print("Index:", index)

        # Now, safely update the count
        existing_count = complaints['complaints']['count'][index]
        complaints['complaints']['count'][index] = existing_count + 1
        mongo.complaints_count.delete_many({})
        mongo.complaints_count.insert_one(complaints)
        #print("After adding:")
        #print("Count:", complaints['complaints']['count'])
        #print(f"Incrementing the count in mongo db with id {acid} ")
    else:
        # Player is new; add player details and initialize count
        complaints['complaints']['pb_id'].append(acid)
        complaints['complaints']['name'].append(offender)
        complaints['complaints']['count'].append(1)  # Initialize count as a list for the new player
        mongo.complaints_count.delete_many({})
        mongo.complaints_count.insert_one(complaints)
        #print("After adding:")
        #print("Pbid:", complaints['complaints']['pb_id'])
        #print("Name:", complaints['complaints']['name'])
        #print("Count:", complaints['complaints']['count'])
        #print(f"Successfully added complaints id in mongo db")

