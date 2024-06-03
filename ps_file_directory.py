"""
Program to find files in a file directory tree and return file paths
@author: Peter Senyk
@version: 2024_0.2
"""


def find_file_in_tree(tree_file_path, search_filename):
    file_path_dictionary = {}
    count = 0
    with open(tree_file_path, 'r', encoding='cp437') as file:
        lines = file.readlines()
        for line in lines:
            if search_filename.lower() in line.lower():
                print(line)


def export_file_paths(file_path_set, output_file_path):
    with open(output_file_path, 'w') as file:
        for path in file_path_set:
            file.write(path + '\n')


if __name__ == '__main__':
    tree_file_path = r"C:\Users\SENYKP\Desktop\Projects\file_directory_script\F_PowerShell\directory_listing.txt"  # Path to the tree file
    output_file_path = r"C:\Users\SENYKP\Desktop\Projects\file_directory_script\Test_Output\TestOutput"  # Output file path
    search_filename = 'Campbell'  # Filename to search for

    file_path_set = find_file_in_tree(tree_file_path, search_filename)
    export_file_paths(file_path_set, output_file_path)
