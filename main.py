import os
import json
import concurrent.futures
from instagrapi import Client

USER_FOLLOWINGS_DIR = os.path.join(os.getcwd(), "user_followings")
DETECTIONS_DIR = os.path.join(os.getcwd(), "detections")
SESSIONID = ""


# determines if the account is worth checking
def is_worth_checking_for_link(user_id):
    info = cl.user_info(user_id)
    return False if \
        info.following_count > 2000 \
        or info.is_verified \
        or info.is_business \
        or info.follower_count > 10000 \
        else True


# returns list of all people the account follows
def get_people_they_follow(user_id):
    return [fol for fol in cl.user_following(user_id)]


# writes list of people they follow to json file
def save_people_they_follow(list_of_people_followed, username_being_searched):
    id = 1
    followed_to_json = []
    for person_followed in list_of_people_followed:
        data = {
                'id': id,
                'uid': person_followed
            }
        followed_to_json.append(data)
        id += 1
    print("Writing to file")
    filename = os.path.join(USER_FOLLOWINGS_DIR, f"{username_being_searched}_followings.json")
    with open(filename, "w") as f_s:
        json.dump(followed_to_json, f_s, indent=4)
    print(f"Written to file {filename}")


# checks account for link
def check_for_link(user_id):
    print(f"Checking {user_id}")
    user_info = cl.user_info(user_id)
    if user_info.external_url and not user_info.is_verified:
        print(f"Link found for: {user_id}")
        print(f"{user_info.username} : {user_info.external_url}")
        return {
            'username': user_info.username,
            'name': user_info.full_name,
            'link': user_info.external_url
        }
    return None


# main function to check all the people user_id follows for a link
def check_followings_for_link(user_id, save_follows=True, save_detections=True):

    username = cl.username_from_user_id(user_id)
    print(f"Checking for link on: {username}")

    people_they_follow = get_people_they_follow(user_id)
    if save_follows:
        save_people_they_follow(people_they_follow, username)

    links_found = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(check_for_link, uid): uid for uid in people_they_follow}
        for future in futures:
            if future.result():
                links_found.append(future.result())
                print(f"Found: {future.result()}")

    if save_detections:
        detections_filename = os.path.join(DETECTIONS_DIR, f"{username}_detections.json")
        with open(detections_filename, 'w') as d_s:
            json.dump(links_found, d_s, indent=4)
        print(f"Detections saved to file {detections_filename}")


if __name__ == "__main__":

    cl = Client()
    print("Logging In")
    cl.login_by_sessionid(SESSIONID)
    print("Logged In")

    # load list of accounts to search followings of
    with open("people_i_follow.json", "r") as f:
        accounts = [p['uid'] for p in json.load(f)]
    print("Data Loaded")

    # or load a single account
    # accounts = [cl.user_id_from_username("")]
    # print("Single Account Loaded")

    for account_to_search in accounts:
        print(f"Checking account {account_to_search}")
        if not is_worth_checking_for_link(account_to_search):
            print(f"Skipping: {account_to_search}")
            continue
        check_followings_for_link(account_to_search, save_follows=True, save_detections=True)
