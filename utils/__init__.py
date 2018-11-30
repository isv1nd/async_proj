import importlib


def import_from_str(path_to_obj: str):
    path_ = path_to_obj.split(".")
    module = importlib.import_module(".".join(path_[:-1]))
    return getattr(module, path_[-1])

