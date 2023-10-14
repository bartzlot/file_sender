from lib import *

def creating_path_to_ui_file(filename: str):

    file_path = pathlib.PurePath(__file__)
    file_path = file_path.parent.parent
    file_path = file_path.joinpath('ui', filename)

    return str(file_path)