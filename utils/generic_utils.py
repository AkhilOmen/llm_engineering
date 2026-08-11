



def run_python_code_str(python_code_str):
    """
        This exec function will let us run the Python code which is in string format
        for Example:
            run: exec("print(2+2)")
            output: 4
    """

    globals = {"__builtins__": __builtins__}
    exec(python_code_str, globals)
