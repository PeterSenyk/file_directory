"""
Program to find files in a file directory tree and return file paths
@author: Peter Senyk
@version: 2024_0.2
"""


def find_file_in_tree(tree_file_path, search_filename):
    file_path_dictionary = {}
    with open(tree_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    file_path_dictionary = check_lines(lines[::-1], search_filename)
    return file_path_dictionary
    
def check_lines(lines, search_filename):
    file_path_dictionary = {}
    count = 0
    for line in lines:
        if search_filename in line:
            count += 1
        elif "Directory" in line and count > 0:
            dir_line = clean_directory_line(line)
            file_path_dictionary[dir_line] = count
            count = 0
    return file_path_dictionary
        
def clean_directory_line(line):
    dir_line = line.lstrip(" ").strip("Directory: ")
    return dir_line
    
def clean_dictionary_results(file_path_dictionary):
    for key, value in file_path_dictionary.items():
        print(f"{key}\nContains {value} files containing the search\n")


if __name__ == '__main__':
    tree_file_path = r"C:\Users\SENYKP\Desktop\Projects\file_directory_script\F_PowerShell\directory_listing.txt"  # Path to the tree file
    output_file_path = r"C:\Users\SENYKP\Desktop\Projects\file_directory_script\Test_Output\TestOutput"  # Output file path
    search_filename = 'Campbell'  # Filename to search for

    file_path_set = find_file_in_tree(tree_file_path, search_filename)
    export_file_paths(file_path_set, output_file_path)
