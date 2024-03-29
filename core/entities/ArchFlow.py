from abc import ABC, abstractmethod
from core.entities.DirectoryCreator import DirectoryCreator
from core.entities.DirectoryExplorer import DirectoryExplorer
from core.entities.StringManipulator import StringManipulator
from core.entities.utils.Filter import Filter
from core.entities.output.OutputHandler import OutputHandler
import sys
import os


filter = Filter()


class ArchFlow(ABC):
    def __init__(self):
        self.DirectoryCreator = DirectoryCreator()
        self.DirectoryExplorer = DirectoryExplorer()
        self.StringManipulator = StringManipulator()
        self.OutputHandler = OutputHandler()
        self.root_path = os.getcwd()

    @abstractmethod
    def create_project(self, *args):
        pass

    @abstractmethod
    def functions_flow(self):
        pass

    def create_file_based_in_template(self, file_destination, file_name, template_file_name, args=None):
        file_destination = file_destination
        content = self.DirectoryExplorer.read_file_template(template_file_name)
        if args:
            content = self.StringManipulator.replace_args(content, args)
        content = self.StringManipulator.replace_tags(content)
        self.DirectoryCreator.create_file(file_destination, file_name, content)

    @staticmethod
    def handle_args():
        args_input = sys.argv
        return args_input[1:]

    def handler_input(self, args, json_content):
        if len(args) == 0:
            self.OutputHandler.success_message("Whoopsie-daisy! It seems like you forgot to provide a function. "
                                               "How about trying --help for some magic commands?")
            return None
        name_function = args[0]

        func = filter.find_key_in_dictionaries(json_content, name_function)
        if func is not None:
            steps_funcao = filter.find_key_in_dictionaries(func, 'steps')
            dictonary_functions = self.dictionary_of_standard_functions()
            self.execute_step(steps_funcao, args, dictonary_functions, json_content)
        else:
            self.OutputHandler.alert_message(f"function '{name_function}' is not valid, try another one or try --help ")

    def execute_step(self, steps_function, args, dictonary_functions, functions_json):
        for dic in steps_function:
            for step in dic:
                args_function = filter.find_key_in_dictionaries(dic, step)
                function = filter.find_key_in_dictionaries(dictonary_functions, step)
                if function is None:
                    function = filter.find_key_in_dictionaries(functions_json, step)
                    steps_functions = filter.find_key_in_dictionaries(function, 'steps')
                    args_function_ = filter.find_key_in_dictionaries(dic, step)
                    args_mapped = filter.map_args(args_function_, args[0:], "tem[")
                    self.execute_step(steps_functions, args_mapped, dictonary_functions, functions_json)
                    break
                try:
                    if args_function == "None":
                        function()
                    elif isinstance(args_function, list):
                        args_mapped = filter.map_args(args_function, args[0:])
                        function(*args_mapped)
                    else:
                        function(*args[1:])
                except TypeError as e:
                    self.OutputHandler.alert_message(f"Error calling the function: {e}")

    def dictionary_of_standard_functions(self):
        dictionary_directory_creator = self.DirectoryCreator.dictionary_of_standard_functions()
        dictionary_directory_explorer = self.DirectoryExplorer.dictionary_of_standard_functions()
        dictionary_string_manipulator = self.StringManipulator.dictionary_of_standard_functions()
        dictionary_output_handler = self.OutputHandler.dictionary_of_standard_functions()
        functions_flow = self.functions_flow()
        return {'create_project': self.create_project,
                'functions_flow': functions_flow,
                'directory_creator': dictionary_directory_creator,
                'directory_explorer': dictionary_directory_explorer,
                'string_manipulator': dictionary_string_manipulator,
                'output_handler': dictionary_output_handler,
                'create_file_based_in_template': self.create_file_based_in_template
                }

