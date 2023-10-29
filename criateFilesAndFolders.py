import os
import re

from db import get_function_by_name
from searchAndRead import find_folder
from utils import to_snake_case, split_words, join_words, to_pascal_case, to_package_format_case, \
    remove_after_use_case
from variables import write_permission, structure_root_folder, \
    regex_to_replace_template, barra_system

string_manipulation = {"case_name_pascal_case": to_pascal_case,
                       "case_name_snake_case": to_snake_case,
                       "package": to_package_format_case,
                       "package_no_use_case": remove_after_use_case}


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print(f"create use-case in: {path}")
        return path
    else:
        print(f'don´t possible create use-case in: {path}')


def create_file(path, conteudo):
    if os.path.exists(path):
        print(f"file already exists in directory: {path}")
    else:
        with open(path, write_permission) as file:
            file.write(conteudo)


def create_folder_structure(name_folder, folder_structure):
    name_folder = split_words(name_folder)
    path_use_case = create_dir(find_folder(structure_root_folder) + "\\" + to_snake_case(name_folder))
    for case in folder_structure:
        create_dir(path_use_case + "\\" + case)


def replace_text_in_string(input_string, substitution_dictionary, name_case):
    matches = re.findall(regex_to_replace_template, input_string)
    for match in matches:
        if match in substitution_dictionary:
            replacement_func = substitution_dictionary[match]
            input_string = re.sub(regex_to_replace_template, lambda x: replacement_func(name_case), input_string, count=1)

    return input_string


def create_file_structure(name_case, function):
    name_case = split_words(name_case)
    function_obj = get_function_by_name(function)
    files_to_be_created = function_obj.GetFiles()
    path_of_case = find_folder(structure_root_folder)

    for file in files_to_be_created:
        content = (replace_text_in_string(file.GetContent(), string_manipulation, name_case))
        path_of_file = (replace_text_in_string(file.GetPath(), string_manipulation, name_case))
        name_of_file = (replace_text_in_string(file.GetName(), string_manipulation, name_case))
        create_file(path_of_case+barra_system+path_of_file+barra_system+name_of_file, join_words(content))
        print(f"file created '{name_of_file}' in {path_of_file}")