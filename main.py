"""Main script"""
from tree_hugger.core import PythonParser, JavaParser, CPPParser
from fuzzywuzzy import fuzz
import statistics

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


# def get_function_heads(py, jv, cpp):
#     if py:
#         return py.get_all_function_names_with_params()
#     if jv:
#         return jv.get_all_method_names_with_params()
#     if cpp:
#         return cpp.get_all_function_names_with_params()


# def get_function_bodies(language):
#     if language == PYTHON:
#         return py.get_all_function_bodies()
#     if language == JAVA:
#         return jv.get_all_class_method_bodies()
#     if language
#         return cpp.get_all_function_bodies()

def erase_none_values(aTuple):
    """erase none values from parameter list"""
    res = list(aTuple)
    check = []
    for item in res:
        if item != None:
            check.append(item)
    return check


def compare_function_heads(language_one, language_two, py_=None, jv_=None, cpp_=None):
    """compares the heads of two functions and gives an estimate on equality"""
    py, jv, cpp = py_, jv_, cpp_
    findings = {}
    sums = []

    if language_one == PYTHON and language_two == JAVA or language_one == JAVA and language_two == PYTHON:
        if py and jv:
            for py_key, jv_key in zip(py.keys(), jv.keys()):
                if py_key == jv_key:
                    py_params = py[py_key]
                    jv_params = jv[jv_key]
                    for py_s_params, jv_s_params in zip(py_params, jv_params):
                        final_compare_py = erase_none_values(py_s_params)
                        final_compare_jv = erase_none_values(jv_s_params)
                        for item, jitem in zip(final_compare_py, final_compare_jv):
                            sums.append(fuzz.ratio(item, jitem))
                        findings[py_key] = statistics.median(sums)
                    

    if language_one == PYTHON and language_two == CPP or language_one == CPP and language_two == PYTHON:
        if py and cpp:
            for py_key,cpp_key in zip(py.keys(),cpp.keys()):
                if py_key == cpp_key:
                    py_params = py[py_key]
                    cpp_params = cpp[cpp_key]
                    for py_s_params, cpp_s_params in zip(py_params,cpp_params):
                        final_compare_py = erase_none_values(py_s_params)
                        final_compare_cpp = erase_none_values(cpp_s_params)
                        for item, jitem in zip(final_compare_py, final_compare_cpp):
                            sums.append(fuzz.ratio(item,jitem))
                        findings[py_key] = statistics.median(sums)
       
    if language_one == JAVA and language_two == CPP or language_one == CPP and language_two == JAVA:
        if jv and cpp:
            for cpp_key, jv_key in zip(cpp.keys(), jv.keys()):
                if cpp_key == jv_key:
                    cpp_params = cpp[cpp_key]
                    jv_params = jv[jv_key]
                    for cpp_s_params, jv_s_params in zip(cpp_params, jv_params):
                        final_compare_cpp = erase_none_values(cpp_s_params)
                        final_compare_jv = erase_none_values(jv_s_params)
                        for item, jitem in zip(final_compare_cpp, final_compare_jv):
                            sums.append(fuzz.ratio(item, jitem))
                        findings[cpp_key] = statistics.median(sums)
    return findings


       

    
def compare_function_bodies():
    """compares the bodies of two functions and gives an estimate on equality"""
    pass


def compare_line():
    """compares lines and gives an estimate on equality"""
    pass


def extract_java_functions(jv_dict):
    """sanitize java functions from class names"""
    sanitized = {}
    for value in jv_dict.values():
        sanitized.update(value)
    return sanitized


# generate language code from extracted information
if __name__ == "__main__":

    py = create_hugger(PYTHON)
    jv = create_hugger(JAVA)
    cpp = create_hugger(CPP)

    py.parse_file("self_made_dataset/python/one.py")
    jv.parse_file("self_made_dataset/java/one.java")
    cpp.parse_file("self_made_dataset/cpp/one.cpp")

    # py_function_names = py.get_all_class_method_names()
    # jv_function_names = jv.get_all_class_method_names()
    # cpp_function_names = cpp.get_all_function_names()

    # py_function_heads = py.get_all_function_names_with_params()
    # jv_function_heads = extract_java_functions(jv.get_all_method_names_with_params())
    # cpp_function_heads = cpp.get_all_function_names_with_params()


    # print(compare_function_heads(PYTHON,JAVA,py_function_heads,jv_function_heads,cpp_function_heads))

    py_function_bodies = py.get_all_function_bodies()
    jv_function_bodies = jv.get_all_method_bodies()
    cpp_function_bodies = cpp.get_all_function_bodies()

    print("------------_PYTHON_-----------------")
    print(py_function_bodies["test"])
    print("------------_JAVA_-----------------")
    print(extract_java_functions(jv_function_bodies)["test"])
    print("------------_CPP_-----------------")
    print(cpp_function_bodies)