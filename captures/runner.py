from cli import genCLI
import os
from time import sleep


all_dir = sorted(os.listdir("./captures"))

cwd = os.getcwd()

print(cwd)

captures = []
for dir in all_dir:
    if dir[0:8] == "capture-":
        # print(dir)
        if os.path.exists(f"./captures/{dir}/capture.sh"):
            print(f"./captures/{dir}/capture.sh")
            captures.append(dir)

choice = genCLI(["all"] + captures)

if choice[0] == 0:
    for capture in captures:
        os.chdir(f"{cwd}/captures/{capture}/")
        os.system("./capture.sh")
        sleep(3)
else:
    os.chdir(f"{cwd}/captures/{choice[1]}/")
    os.system("./capture.sh")