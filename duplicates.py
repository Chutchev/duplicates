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
                dupl[dups[i]['path']] = {'duplicates': dups[j]['path'], 'md5': dups[j]['md5']}
    for filename in dupl.keys():
        with open(os.path.abspath("duplicates.txt"), "a") as dublicates_txt:
            dublicates_txt.write(f"{filename}: \n\t{dupl[filename]['duplicates']}  {dupl[filename]['md5']}\n")
    return dupl


def fill_delete_list(dupl):
    delete_list = dupl.copy()
    keys_list = []
    for i in dupl.keys():
        keys_list.append(i)
    for duplicate_name in dupl.keys():
        keys_list.pop(keys_list.index(duplicate_name))
        for filename in keys_list:
            if duplicate_name != filename:
                if dupl[duplicate_name]['duplicates'] == filename:
                    delete_list[filename] = {'duplicates': 'File was Deleted'}
    for filename in delete_list.keys():
        with open(os.path.abspath("for_duplicates_delete.txt"), "a") as dublicates_txt:
            dublicates_txt.write(f"{filename}:\n\t{delete_list[filename]['duplicates']}\n")
    return delete_list


def delete_duplicates(duplicates):
    for filenames in duplicates.keys():
        if duplicates[filenames]['duplicates'] != "File must be deleted!!!":
            with open(os.path.abspath("delete_duplicates.txt"), "a") as dublicates_txt:
                dublicates_txt.write(f"{filenames}\n")
            os.remove(filenames)


def main():
    path = sys.argv[1]
    start_time = time.time()
    dubl = find_duplicates(fill_list_duplicates(path))
    delete_file = fill_delete_list(dubl)
    delete = sys.argv[2]
    if delete.lower() == 'y':
        delete_duplicates(delete_file)
    elif delete.lower() == 'n':
        pass
    print(f"Сделано за {time.time()-start_time}")


if __name__ == '__main__':
    main()