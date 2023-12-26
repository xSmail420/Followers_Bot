import argparse
import json
import time
import datetime
from instagram.InstaBot import InstagramBot

def load_accounts():
        try:
            with open("instagram/accounts.json", "r") as file:
                accounts = json.load(file)
        except:
            accounts = []
        return accounts

def load_users():
        try:
            with open("instagram/users.json", "r") as file:
                users = json.load(file)
            return users
        except FileNotFoundError:
            return None
     
def save_accounts(accounts):
    with open("instagram/accounts.json", "w") as file:
        json.dump(load_accounts() + accounts, file)

def save_followed(users):
    with open("instagram/followed.json", "w") as file:
        json.dump(users, file)

def load_followed():
    try:
        with open("instagram/followed.json", "r") as file:
            users = json.load(file)
            # Assurez-vous que 'users' est une liste
            if not isinstance(users, list):
                users = []
        return users
    except FileNotFoundError:
        return []

def create_bot(account):
    bot = InstagramBot()
    bot.login(email=account["username"], password=account["password"])
    return bot

def main():
    parser = argparse.ArgumentParser(description="Instagram Bot")

    parser.add_argument("-a", "--accounts", action="store_true", help="Use multiple accounts")
    parser.add_argument("-d", "--days", type=int, default=7, help="Days before unfollow users")
    parser.add_argument("-del", "--delay", type=int, default=5, help="Delay in seconds between actions")

    args = parser.parse_args()

    if args.accounts:
        accounts = load_accounts()

        if len(accounts) == 0:
            print("No accounts found. Please add accounts first.")
            return

        for i, account in enumerate(accounts):
            print(f"Account {i+1}: {account['username']}")

        account_choice = input("Select an account number: ")

        try:
            account_choice = int(account_choice)
            if account_choice < 1 or account_choice > len(accounts):
                print("Invalid account number.")
                return
        except ValueError:
            print("Invalid input.")
            return

        account = accounts[account_choice - 1]
        bot = create_bot(account)
    else:
        username = input("Enter your Instagram username: ")
        password = input("Enter your Instagram password: ")

        account = {
            "username": username,
            "password": password
        }
        save_accounts([account])
        bot = create_bot(account)

    
    usernames = load_users()
    followed = load_followed()
    follow_actions = 0
    unfollow_actions = 0
    queue = []
    
    while True:

        if follow_actions > 90 or unfollow_actions >90 :
            # 190 actions per day
            print("sleep until daily limit resets")
            unfollow_actions = 0
            follow_actions = 0
            time.sleep(24 * 60 * 60)
            continue

        # Get the current date
        current_date = datetime.datetime.now().date()
        users_to_follow = []

        # Iterate over the followed list and unfollow users with dates more than provided days ago
        for entry in followed:

            if unfollow_actions > 90 :
                print("daily unfollow actions limit reached...")
                break

            entry_date = datetime.datetime.strptime(entry["date"], "%m/%d/%Y").date()
            days_difference = (current_date - entry_date).days


            if days_difference >= args.days:
                # Unfollow the user
                print(f'unfollow action : {entry["username"]}')
                bot.unfollow(user = entry["username"], delay = args.delay)
                
                unfollow_actions += 1
            else :
                queue.append(entry)
                

        for username in usernames:
            usernames.remove(username)
            followers = bot.getfollowers(username=username, delay=args.delay)
            users_to_follow.extend([user for user in followers if user not in [item['username'] for item in followed]])

        for user in users_to_follow:
            if follow_actions > 90 :
                print("daily follow actions limit reached...")
                break
            # bot.follow(user = user,delay = args.delay)
            print(f'follow action : {user}')
            follow_actions += 1
            queue.append({"username": user, "date": datetime.datetime.now().strftime("%m/%d/%Y")})
            
        print(queue)
        save_followed(queue)

    bot.quit()

if __name__ == "__main__":
    main()
