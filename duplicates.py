import hashlib
import os
import sys

def read_hash(filename):
    with open(filename, 'rb') as file:
        hash_md5 = hashlib.md5()
        image = file.read(65536)
        hash_md5.update(image)
        return hash_md5.hexdigest()


def fill_list_duplicates(path):
    dups = {}
    for dir, subdirs, files in os.walk(path):
        for file in files:
            filename = os.path.join(path, file)
            dups[filename] = {'md5': read_hash(filename), 'path': filename}
    return dups


def find_duplicates(dups):
    dupl = []
    i = 0
    for filename in dups.keys():
        md5_hash = dups[filename]["md5"]
        

def main():
    #path = sys.argv[1]
    find_duplicates(fill_list_duplicates("C:\\Users\\Ivan\\Desktop\\ИВТ-16"))

if __name__ == '__main__':
    main()