import hashlib
import os
import sys
import time

def read_hash(filename):
    with open(filename, 'rb') as f:
        hash_md5 = hashlib.md5()
        image = f.read(65536)
        hash_md5.update(image)
        return hash_md5.hexdigest()


def fill_list_duplicates(path):
    dups = {}
    index = 0
    for dir, subdirs, files in os.walk(path):
        for f in files:
            filename = os.path.join(dir, f)
            dups[index] = {'md5': read_hash(filename), 'path': filename}
            index += 1
    return dups


def find_duplicates(dups):
    dupl = {}
    for index in range(len(dups)):
        for jindex in range(len(dups)):
            if dups[index]['md5'] == dups[jindex]['md5'] and dups[index]['path'] != dups[jindex]['path']:
                dupl[dups[index]['path']] = {'duplicates': dups[jindex]['path'], 'md5': dups[jindex]['md5']}
    for filename in dupl.keys():
        with open(os.path.abspath("duplicates.txt"), "a") as dublicates_txt:
            dublicates_txt.write(f"{filename}: \n\t{dupl[filename]['duplicates']}  {dupl[filename]['md5']}\n")
    return dupl


def fill_delete_list(dupl):
    delete_list = dupl.copy()
    keys_list = []
    for index in dupl.keys():
        keys_list.append(index)
    for duplicate_name in dupl.keys():
        keys_list.pop(keys_list.index(duplicate_name))
        for filename in keys_list:
            if duplicate_name != filename:
                if dupl[duplicate_name]['duplicates'] == filename:
                    delete_list[filename] = {'duplicates': 'File must be deleted!!!'}
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