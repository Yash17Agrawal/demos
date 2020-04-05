import os
import re
from random import randint
from random import seed
import shutil
import glob


class Clean_Music_Files:
    def __init__(self):
        super().__init__()
        self.parent_dir = '/media/yash/91EE-A58B/music'
        self.group_size = 10
        self.number_of_folders = 0

    def clean_name(self, dirty_file_name):
        dirty_file_name = dirty_file_name.replace('-', ' ')
        file_name_parts = dirty_file_name.split(' ')
        if (file_name_parts[0].isdigit()):
            file_name_parts[0] = ''
        dirty_file_name = ' '.join(file_name_parts)
        return dirty_file_name.strip()

    def make_directory(self, folder_name):
        try:
            os.mkdir(folder_name)
        except Exception as e:
            print("Ignore this error")
            print(e)
        return

    def set_number_of_folders(self, total_files):
        self.number_of_folders = int(total_files / self.group_size)

    def make_groups(self, total_files):
        for folder_index in range(self.number_of_folders):
            folder_index = folder_index + 1
            path = os.path.join(self.parent_dir, str(folder_index))
            self.make_directory(path)
        if (total_files % self.group_size != 0):
            path = os.path.join(self.parent_dir, str(
                self.number_of_folders + 1))
            self.make_directory(path)
        return

    def check_if_folder_already_exists(self):
        return

    def delete_files(self):
        """
        to delete repetetive files
        """
        return

    def combine_sub_folders_files(self, dest_dir):
        dest_dir = dest_dir + '/'
        """
        if there are sub directories of music files we can combine them and do unified processing
        """
        # Check if both the are directories
        if os.path.isdir(dest_dir):
            # Iterate over all the files in source directory
            for path in glob.glob(dest_dir + '/*'):
                for filePath in glob.glob(path + '/*'):
                    # Move each file to destination Directory
                    shutil.move(filePath, dest_dir)
        else:
            print("dstDir should be Directories")

    def process_music_files(self):
        print("****beginning cleaning****")
        folder_path = self.parent_dir
        self.combine_sub_folders_files(folder_path)
        path, dirs, files = next(os.walk(folder_path))

        num_of_files = len(files)
        self.set_number_of_folders(num_of_files)
        self.make_groups(num_of_files)
        with os.scandir(folder_path) as entries:
            for entry in entries:
                if (entry.is_file()):
                    updated_name = self.clean_name(entry.name)
                    folder_to_put = randint(1, self.number_of_folders)
                    os.rename('{}/{}'.format(folder_path, entry.name),
                              '{}/{}/{}'.format(folder_path, folder_to_put, updated_name))
        print("****cleaning completed****")
        return


Clean_Music_Files().process_music_files()
