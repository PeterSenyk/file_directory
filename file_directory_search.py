"""
Program to search a PowerShell recursive file directory and return file paths
@author: Peter Senyk
@version: 2024_0.3
"""

import csv


def find_file_in_tree(file_path, filename):
    """
    Reads the file directory textfile and searches for given filename.
    :param file_path: Path to the file directory text file.
    :param filename:  Filename to search for.
    :return: A dictionary where the key represents a filepath, and the value represents the number of matches at
    that location.
    """
    try:
        with open(file_path, 'r', encoding='utf-16') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File {file_path} was not found.")
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

    return process_lines(lines, filename)


def process_lines(lines, filename):
    """
    Processes the lines from the directory text file and searches for the filename.
    :param lines: List of lines from the directory file.
    :param filename: String representing the filename being searched for.
    :return: A dictionary where the key represents a filepath, and the value represents the number of matches at
    that location.
    """
    file_path_dictionary = {}
    current_dir = ''
    count = 0
    print("Searching...", end="")

    for i, line in enumerate(lines):
        if "Directory:" in line:
            # if current_dir and count > 0:
            #     file_path_dictionary[current_dir] = count
            current_dir = clean_directory_line(line.strip())
            current_dir = check_multiline_directory(lines, i + 1, current_dir)
            count = 0
        elif line.strip() == '' and count > 0:
            if current_dir:
                # current_dir = clean_directory_line(current_dir)
                file_path_dictionary[current_dir] = count
                current_dir = ''
                count = 0
        elif filename.lower() in line.lower():
            count += 1

    print("Complete")
    return file_path_dictionary


def check_multiline_directory(lines, index, current_dir):
    """
    Checks for paths that may consist of multiple lines in the directory file.
    :param lines: List of lines from the directory file.
    :param index: An int representing the initial line the "Directory" keyword was found on.
    :param current_dir: A string representing the current file path being searched.
    :return: A string representing the current directory path being searched.
    """
    while index < len(lines) and lines[index].strip() != '' and "Directory:" not in lines[index]:
        current_dir += lines[index].strip()
        index += 1
    return current_dir


def clean_directory_line(line):
    """
    Removes unnecessary parts of the directory path.
    :param line: A string representing the current line being read.
    :return: A string representing the total directory path.
    """
    return line.removeprefix(" ").removeprefix("Directory:").removeprefix(" ")


def total_results(path_dictionary):
    path_count = len(path_dictionary)
    file_count = 0
    for files in path_dictionary.values():
        file_count += files
    print(f"{path_count} file paths were found\nContaining a total of {file_count} files/folders")


def export_file_paths(path_dictionary, search, output_path):
    """
    Exports the filepaths to a CSV file.
    :param path_dictionary: A dictionary holding the filepaths and the amount of files found at each path.
    :param search: A string representing the filename searched for
    :param output_path: A string representing the output path for the CSV file.
    """
    file_name = f"Filepath_Output_For_Search_{search}.csv"
    file_output = f"{output_path}\\{file_name}"
    try:
        with open(file_output, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["File Path", "Number of Files"])

            for path, number in path_dictionary.items():
                writer.writerow([path, number])
        print(f"CSV exported to {file_output}")
    except Exception as e:
        print(f"Error writing to file: {e}")


if __name__ == '__main__':
    tree_file_path = r"D:\testScripts\batch\directory_listing.txt"  # Path to the tree file
    output_file_path = r"D:\testScripts\testOutput"  # Output file path
    search_filename = input("Enter your search here: ")  # Filename to search for

    file_paths = find_file_in_tree(tree_file_path, search_filename)
    total_results(file_paths)
    export_file_paths(file_paths, search_filename, output_file_path)
    stay_open = input("Press Enter to exit...")
