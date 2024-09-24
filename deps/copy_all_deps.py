import os
import shutil

# CONSTANTS
DEPS_EXE_FILE = "deps_exe"
DEPS_ONE_LEVEL_ABOVE_EXE_FILE = "deps_above_exe"
RELEASE_DIR_NAME = "release"
DEBUG_DIR_NAME = "debug"
LEVELS_UP_TO_BUILD_DIRS = "../../"

# FUNCTIONS
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                continue
            shutil.copytree(s, d, symlinks, ignore)
        else:
            if os.path.exists(d):
                continue
            shutil.copy2(s, d)

def make_release_or_debug_path(out):
        r_d = '/'
        if RELEASE_DIR_NAME in out.lower():
            r_d = r_d + RELEASE_DIR_NAME
        if DEBUG_DIR_NAME in out.lower():
            r_d = r_d + DEBUG_DIR_NAME
        return r_d



# SCRIPT FOR RESOLVING ALL DEPENDENCIES
print('STEP 1 - Create deps directories list and files list')
files_in_exe_list = os.listdir(DEPS_EXE_FILE)
for file in files_in_exe_list:
    print(file)
files_in_above_exe_list = os.listdir(DEPS_ONE_LEVEL_ABOVE_EXE_FILE)
for file in files_in_above_exe_list:
    print(file)


print('\nSTEP 2 - Create build directories list')
out_dir_list = []
build_dirs_list = os.listdir(LEVELS_UP_TO_BUILD_DIRS)
for dir in build_dirs_list:
    if not RELEASE_DIR_NAME  in dir.lower() and not DEBUG_DIR_NAME in dir.lower():
        print('IGNORE THIS DIR (no release and debug word in its name) -->', dir)
        continue
    if os.path.isfile(dir):
        continue
    print("BUILD folder: " + dir)
    full_release_path = LEVELS_UP_TO_BUILD_DIRS + dir + "/" + RELEASE_DIR_NAME
    full_debug_path = LEVELS_UP_TO_BUILD_DIRS + dir + "/" + DEBUG_DIR_NAME
    print ("FULL_PATH: " + full_release_path)
    if not os.path.exists(full_release_path):
       os.mkdir(full_release_path)
    if not os.path.exists(full_debug_path):
       os.mkdir(full_debug_path)
    out_dir_list.append(dir)


print('STEP 3 - Copy files to build dirs with .EXE')
print(out_dir_list)
for file in files_in_exe_list:
    file = DEPS_EXE_FILE + "/" + file
    print(file)
    for out in out_dir_list:
        r_d = make_release_or_debug_path(out)
        if r_d == '/':
            print('RELEASE DEBUG UNEXPECTED ERROR',out)
            continue     
        if os.path.isfile(file):
           print("file exists: " + file)
           print(f"copy exe file deps {file} to: -->", LEVELS_UP_TO_BUILD_DIRS + out + r_d)
           shutil.copy(file, LEVELS_UP_TO_BUILD_DIRS + out + r_d)
        if os.path.isdir(file):
           file_name = LEVELS_UP_TO_BUILD_DIRS + out + r_d
           print(f"copy dir deps {file} to: --> {file_name}")
           base_name_ = os.path.basename(file)
           print("BASE NAME: -- >" + base_name_)
           full_path = file_name + "/" + base_name_
           if not os.path.exists(full_path):
               os.mkdir(full_path)
           copytree(file, full_path)


print('STEP 4 - Copy files to build one level above exe dir')
for file in files_in_above_exe_list:
    file = DEPS_ONE_LEVEL_ABOVE_EXE_FILE + "/" + file
    for out in out_dir_list:
        if os.path.isfile(file):
            file_name = LEVELS_UP_TO_BUILD_DIRS + out
            print(f"copy file deps {file} to: --> {file_name}")
            shutil.copy(file, file_name)
        if os.path.isdir(file):
            file_name = LEVELS_UP_TO_BUILD_DIRS + out
            print(f"copy dir deps {file} to: --> {file_name}")
            base_name_ = os.path.basename(file)
            print("BASE NAME: -- >" + base_name_)
            full_path = file_name + "/" + base_name_
            if not os.path.exists(full_path):
               os.mkdir(full_path)
            copytree(file, full_path)

