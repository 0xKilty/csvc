import csv    

def read_sv_file(filename, delimiter=","):
    with open(filename) as fp:
        reader = csv.reader(filename, delimiter=delimiter)
    return list(reader)

def read_file(filename):
    with open(filename, "rb") as fp:
        data = fp.read()
    return data

def main():
    filename = "test_data\\2025q1_form345\\NONDERIV_TRANS.tsv"
    file_data = read_file(filename)
    print(file_data)

if __name__ == "__main__":
    main()