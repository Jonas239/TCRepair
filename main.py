"""Main script"""
from tree_hugger.core import PythonParser, JavaParser, CPPParser

PYTHON = "PYTHON"
JAVA = "JAVA"
CPP = "CPP"

def open_file(file):
    """opens a file and returns its content as string"""
    with open(file, "r", encoding="utf-8") as f:
        file_ = f.read()
    return file_

def create_hugger(language):
    """return a hugger to retrieve all information"""
    if language == PYTHON:
        return PythonParser(library_loc="build/my-languages.so")
    if language == JAVA:
        return JavaParser(library_loc="build/my-languages.so")
    if language == CPP:
        return CPPParser(library_loc="build/my-languages.so")

def get_function_heads(py, jv, cpp):
    if py:
        yield py.get_all_function_names_with_params()
    elif jv:
        yield jv.get_all_method_names_with_params()
    elif cpp:
        yield cpp.get_all_function_names_with_params()

def get_function_bodies(py, jv, cpp):
    if py:
        yield py.get_all_function_bodies()
    elif jv:
        yield jv.get_all_class_method_bodies()
    elif cpp:
        yield cpp.get_all_function_bodies()


def compare_function_heads():
    py,jv,cpp = get_function_heads()
    if py:
        for 


    """compares the heads of two functions and gives an estimate on equality"""
    pass

def compare_function_bodies():
    """compares the bodies of two functions and gives an estimate on equality"""
    pass

def compare_line():
    """compares lines and gives an estimate on equality"""
    pass

def extract_java_functions():
    pass



##generate language code from extracted information

if __name__ == "__main__":

    py = create_hugger(PYTHON)
    jv = create_hugger(JAVA)
    cpp = create_hugger(CPP)

    py.parse_file("self_made_dataset/python/one.py")
    jv.parse_file("self_made_dataset/java/one.java")
    cpp.parse_file("self_made_dataset/cpp/one.cpp")

    py_function_names = py.get_all_class_method_names()
    jv_function_names = jv.get_all_class_method_names()
    cpp_function_names = cpp.get_all_function_names()

    py_function_bodies = py.get_all_function_names_with_params()
    jv_function_bodies = jv.get_all_method_names_with_params() 
    cpp_function_bodies = cpp.get_all_function_names_with_params()

    print(py_function_bodies)
    print("--------------------------------------------------------")
    print(jv_function_bodies)
    print("--------------------------------------------------------")
    print(cpp_function_bodies)