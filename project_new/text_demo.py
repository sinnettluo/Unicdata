import pymongo
from pandas import DataFrame

connection = pymongo.MongoClient('192.168.1.94', 27017)
db = connection["chexiu"]
collection = db["chexiu_car"]
model_data = collection.find({}, {"vehicle_id": 1, "vehicle": 1, '_id': 0})

car_msg_list = list(model_data)
car_msg_df = DataFrame(car_msg_list)
car_msg_df_new = car_msg_df.drop_duplicates('vehicle_id')

print(car_msg_df_new)