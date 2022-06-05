from cx_Freeze import setup,Executable

build_exe_options={"packages":["os"],"includes":["tkinter","shutil","subprocess","copy","multiprocessing","sys","PIL"],"include_files":['projectBase',"data"]}

base="Win32GUI"

setup(name="KEngine",version="0.0.1a",description="criado por kaklik",options={"build_exe":build_exe_options},executables=[Executable(script="KEngine.py")])
#python3 setup.py build