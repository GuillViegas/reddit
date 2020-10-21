import os


SQL_PATH = os.path.dirname(os.path.abspath(__file__))


def load_sql_file(filename):
    fh = open(os.path.join(SQL_PATH, filename), 'r')
    return fh.read()


def discover_and_load(path):
    print("\nLooking for SQL scripts...\n")
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(".sql"):
                vname = filename.split(".sql")[0].upper()
                globals()[vname] = load_sql_file(filename)
                print(f"\tLoaded SQL scripts: {filename} as {vname}")
    print("\n---\n")


discover_and_load(SQL_PATH)
