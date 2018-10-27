import hashlib
import os
import sys
import time


def read_hash(filename):
    with open(filename, 'rb') as file:
        hash_md5 = hashlib.md5()
        image = file.read(65536)
        hash_md5.update(image)
        return hash_md5.hexdigest()


def fill_list_duplicates(path):
    dups = {}
    i = 0
    for dir, subdirs, files in os.walk(path):
        for file in files:
            filename = os.path.join(dir, file)
            dups[i] = {'md5': read_hash(filename), 'path': filename}
            i += 1
    return dups


def find_duplicates(dups):
    dupl = {}
    for i in range(len(dups)):
        for j in range(len(dups)):
            if dups[i]['md5'] == dups[j]['md5'] and dups[i]['path'] != dups[j]['path']:
                dupl[dups[i]['path']] = {'duplicates': dups[j]['path']}
    for filename in dupl.keys():
        with open(os.path.abspath("dublicdate.txt"), "a") as dublicates_txt:
            dublicates_txt.write(f"{filename}: {dupl[filename]['duplicates']}\n")


def main():
    path = sys.argv[1]
    start_time = time.time()
    find_duplicates(fill_list_duplicates(path))
    print(f"Сделано за {time.time()-start_time}")


if __name__ == '__main__':
    main()
