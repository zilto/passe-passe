import argparse

import auth
import models
import config


def parse_arguments():
    parser = argparse.ArgumentParser(description="Store and manage credentials")
    parser.add_argument("-g", "-get", "--get", help="Enter '-get website' to get credentials")
    parser.add_argument("-s", "-set", "--set", help="Enter '-set website' to set credentials")
    parser.add_argument("-f", "-flag", "--flag", action="store_true", help="Add '-f' or 'flag' to set command to make entry hidden to '-list' command")
    parser.add_argument("-u", "-update", "--update", help="Enter '-u website' to update credentials")
    parser.add_argument("-del", "-delete", "--delete", help="Enter '-del website' to delete stored credentials")
    parser.add_argument("-dir", "-directory", "--directory", help="Enter '-dir directoryname' to set directory of databse")
    parser.add_argument("-l", "-list", "--list", action="store_true", help="Display all websites stored in the database")
    # returns an argparse objects with the args passed by user on command line
    args, remaining_args = parser.parse_known_args()
    return args


def create_credentials(website, session_key):
    credentials = {website: {"email" : input("Enter email: "),
                             "username" : input("Enter username: "),
                             "password" : input("Enter password: ")}
                   }
    crypt_cred = auth.encrypt_AES(session_key, credentials)
    cred_obj = models.Credentials(cipher = crypt_cred["cipher"],
                                  kdfsalt = crypt_cred["kdfsalt"],
                                  ciphertext = crypt_cred["ciphertext"],
                                  nonce = crypt_cred["nonce"],
                                  mac = crypt_cred["mac"])
    return cred_obj


def main():
    args = vars(parse_arguments())
    session = models.initialize(config.DBDIR + config.DBNAME)
    print("\nSQL session initialized.\n")

    if args["get"] or args["set"]:
        session_key = auth._getpass("Enter session key: ")
        print("Session key registered.\n")

    if args["list"]:
        models.list_all(session)

    if args["set"]:
        entry = models.Registry(website=args["set"], flag=args["flag"])
        entry.credentials = [create_credentials(args["set"], session_key)]
        models.add_entry(session, entry)

    if args["update"]:
        #
        #entry = read_entry(session, args["update"])
        #models.update_entry(session, entry)
        pass

    if args["get"]:
        query = models.read_entry(session, args["get"])
        crypto_cred = query.credentials[0]
        json_cred = auth.decrypt_AES(session_key,
                                     kdfsalt=crypto_cred.kdfsalt,
                                     ciphertext=crypto_cred.ciphertext,
                                     nonce=crypto_cred.nonce,
                                     mac=crypto_cred.mac)
        print(json_cred)

    if args["delete"]:
        if input(f"Are you sure you want to delete this entry? (y/n)").lower() == "y":
            models.remove_entry(session, args["delete"])
            print("Entry deleted")
        else:
            print("Entry not deleted")

    session.commit()

if __name__ == "__main__":
    main()
