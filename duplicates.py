import hashlib
import os
import argparse
import time


def read_hash(filename):
    with open(filename, 'rb') as f:
        hash_md5 = hashlib.md5()
        image = f.read(65536)
        hash_md5.update(image)
        return hash_md5.hexdigest()


def fill_list_files_with_md5_hash(path):
    md5_files_dict = {}
    for dir, subdir, files in os.walk(path):
        for f in files:
            filename = os.path.join(dir, f)
            hash = read_hash(filename)
            md5_files_dict[filename] = {'md5': hash}
    return md5_files_dict


def find_duplicates(md5_files_dict):
    dups = {}
    for filename, hash in md5_files_dict.items():
        dups_filename = []
        for other_name, other_hash in md5_files_dict.items():
            if hash['md5'] == other_hash['md5'] and filename != other_name:
                dups_filename.append(other_name)
            if len(dups_filename) > 0:
                dups[hash['md5']] = {'original': filename, 'duplicates': dups_filename}
    return dups


def delete_duplicates(dups):
    for value in dups.values():
        for f in value['duplicates']:
            os.remove(f)
            print(f'Файл: {f} был удален')


def main():
    parser= argparse.ArgumentParser(description="USAGE: python duplicates.py path_to_directory_with_duplicates y/n")
    parser.add_argument('path', help="Переменная для установки пути для поиска дубликатов")
    parser.add_argument('delete', help="Флаг для разрешения/отказа на удаление дубликатов")
    args = parser.parse_args()
    md5_file_dict = fill_list_files_with_md5_hash(args.path)
    dict_dups = find_duplicates(md5_file_dict)
    if args.delete == 'y':
        delete_duplicates(dict_dups)
        print('Поиск дубликатов выполнен. Файлы были удалены, так как было дано ваше разрешение.')
    else:
        print('Поиск дубликатов выполнен. Файлы не были удалены, так как не было дано ваше разрешение.')


if __name__ == '__main__':
    main()