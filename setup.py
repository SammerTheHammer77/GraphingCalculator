import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\Samuel\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Samuel\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

executables = [cx_Freeze.Executable("Final.py")]

cx_Freeze.setup(
    name="Graphing Calculator",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["C:/Users/Samuel/Documents/Final/Buttons",
                                            "C:/Users/Samuel/Documents/Final/Pics"]}},
    executables = executables

    )
