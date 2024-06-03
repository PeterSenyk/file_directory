"""
Program to search a file directory and return file paths
@author: Peter Senyk
@version: 2024_0.2
"""

import csv
from datetime import datetime


def find_file_in_tree(file_path, filename):
    with open(file_path, 'r', encoding='utf-16') as file:
        lines = file.readlines()
    file_path_dictionary = check_lines(lines, filename)
    return file_path_dictionary


def check_lines(lines, filename):
    file_path_dictionary = {}
    current_dir = ''
    count = 0

    for i, line in enumerate(lines):
        if "Directory:" in line:
            if current_dir and count > 0:
                file_path_dictionary[current_dir] = count
            current_dir = clean_directory_line(line.strip())
            current_dir = check_multiline_directory(lines, i + 1, current_dir)
            count = 0
        elif line.strip() == '' and count > 0:
            if current_dir:
                file_path_dictionary[current_dir] = count
                current_dir = ''
                count = 0
        elif filename.lower() in line.lower():
            count += 1

    if current_dir and count > 0:
        file_path_dictionary[current_dir] = count

    print(file_path_dictionary)
    return file_path_dictionary


def check_multiline_directory(lines, index, current_dir):
    while index < len(lines) and lines[index].strip() != '' and "Directory:" not in lines[index]:
        current_dir += lines[index].strip()
        index += 1
    return current_dir


def clean_directory_line(line):
    dir_line = line.removeprefix("    Directory: ")
    return dir_line


def clean_dictionary_results(file_path_dictionary):
    for key, value in file_path_dictionary.items():
        print(f"{key}\nContains {value} files containing the search\n")


def export_file_paths(path_dictionary, output_path):
    current_date = datetime.now().strftime("%y-%m-%d")
    file_name = f"Filepath_Output_{current_date}.csv"
    file_output = output_path + "\\" + file_name

    with open(file_output, "w", newline="") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["File Path", "Number of Files"])

        for path, number in path_dictionary.items():
            writer.writerow([path, number])


if __name__ == '__main__':
    tree_file_path = r"D:\testScripts\batch\directory_listing.txt"  # Path to the tree file
    output_file_path = r"D:\testScripts\testOutput"  # Output file path
    search_filename = "syntychristmas"  # Filename to search for

    file_paths = find_file_in_tree(tree_file_path, search_filename)
    export_file_paths(file_paths, output_file_path)
