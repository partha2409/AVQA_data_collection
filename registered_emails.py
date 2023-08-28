import pickle

users_dict = {
    'xyz@tuni.fi': 1,
    'abc@tuni.fi': 2,

}

with open('registered_emails.pkl', "wb") as f:
    pickle.dump(users_dict, f)