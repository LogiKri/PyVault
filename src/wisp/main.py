from wisp import config
from wisp.storage import LocalStore, ServerStore
# Backend selection is fixed (config.BACKEND was previously read via
# os.getenv() directly in this file, using a .env that never actually
# loaded - see wisp/config.py for the fix).
store = LocalStore() if config.BACKEND == "LOC" else ServerStore()


def main():
    print("""Wisp
    1. add user
    2. add key
    3. list keys
    4. delete key
    5. quit
    """)

    while True:
        choice = input("> ").strip()
        if choice == "1":
            username = input("username: ")
            password = input("password: ")
            success = store.create_user(username, password)
            if not success:
                print("That username is already taken, try again.")
            else:
                print("User created.")
        elif choice == "2":
            name = input("name: ")
            key = input("key: ")
            store.add_item({"name": name, "key": key})
        elif choice == "3":
            get_list = store.get_list()
            print("#####################")
            for i in get_list:
                print(i)
            print("#####################")
        elif choice == "4":
            name = input("Enter name of item: ")
            store.delete_smt(name)
            print("Item deleted")
        elif choice == "5":
            break


if __name__ == "__main__":
    main()
