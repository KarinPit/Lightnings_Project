import os


def get_dirs(wanted_date, file_type):
    main_dir_path = 'D:/ENTLN/ENTLN DATA/'
    dirs = []
    for item in os.listdir(main_dir_path):
        full_path = os.path.join(main_dir_path, item)
        if os.path.isdir(full_path) and full_path[-7:] == wanted_date:
            full_path = full_path.replace('\\', '/')
            for item in os.listdir(full_path):
                if os.path.isdir(full_path) and item == file_type:
                    full_path = os.path.join(full_path, item)
                    full_path = full_path.replace('\\', '/')
                    dirs.append(full_path)
    dirs.sort()
    return dirs


def get_all_files(dir):
    all_files = os.listdir(dir)
    txt_files = []
    for file in all_files:
        full_path = os.path.join(dir, file)
        full_path = full_path.replace('\\', '/')
        if file.find('.txt') != -1:
            txt_files.append(full_path)
        else:
            pass
    return txt_files


def get_united_file(all_files):
    with open('D:/ENTLN/ENTLN DATA/Dec_2021.txt', 'w') as outfile:
        for fname in all_files:
            with open(fname) as infile:
                outfile.write(infile.read())


def main():
    wanted_date = '12-2021'
    file_type = 'flash'
    dirs = get_dirs(wanted_date, file_type)
    all_files = []
    for dir in dirs:
        files = get_all_files(dir)
        all_files += files
    get_united_file(all_files)


if __name__ == '__main__':
    main()