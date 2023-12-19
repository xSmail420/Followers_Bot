# import json

# def save_followed(users):
#     existing_users = load_followed()
#     with open("instagram/followed.json", "w") as file:
#         json.dump(existing_users + users, file)

# def load_followed():
#     try:
#         with open("instagram/followed.json", "r") as file:
#             users = json.load(file)
#             # Assurez-vous que 'users' est une liste
#             if not isinstance(users, list):
#                 users = []
#         return users
#     except FileNotFoundError:
#         return []

# Exemple d'utilisation
# followed = [{"username": "ali", "date": "12/12/2023"}, {"username": "boouba", "date": "12/10/2023"}]
# users = ["ali", "omar", "adem"]

# users_to_keep = [user for user in users if user not in [item['username'] for item in followed]]

# print(users_to_keep)

# import datetime

# # Assuming you have a stored date in the "date" key of a dictionary
# current_date = datetime.datetime.now().strftime("%m/%d/%Y")
# print(current_date)
# stored_date_str = "12/11/2022"
# stored_date = datetime.datetime.strptime(stored_date_str, "%m/%d/%Y").date()

# # Calculate the number of days since the stored date
# current_date = datetime.datetime.now().date()
# days_since_stored_date = (current_date - stored_date).days

# print(f"Days since stored date: {days_since_stored_date}")

url = "https://www.instagram.com/jdija>3r3grgb___bcjsdbcksdjvblsdj/"

# Split the URL by "/" and take the last part
username = url.split("/")[-2]

# Output the extracted username
print(username)