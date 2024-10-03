import os
import subprocess
from time import time


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def build(image) -> dict:
    path = f"./containers/{image}"
    tag = f"detlearsom/{image[7::]}"
    start = time()
    with open(f"{path}/build_log.log", "w") as log_file:
        result = subprocess.run(
            [
                "sudo",
                "docker",
                "build",
                "--platform",
                "linux/amd64",
                "-t",
                f"{tag}",
                f"{path}"
            ],
            stdout=log_file,
            stderr=subprocess.STDOUT
        )

    return {
        "code": not result.returncode,
        "state": f"{bcolors.FAIL}Failed" if result.returncode != 0 else f"{bcolors.OKGREEN}Succeeded",
        "time": round(time()-start, 2),

    }


def pull(image: str) -> dict:
    start = time()
    tag = image[:image.index(":"):] if ":" in image else image
    log_name = tag.replace("/", "")
    # print(tag)
    with open(f"./containers/standard-logs/{log_name}.log", "w") as log_file:
        result = subprocess.run(
            [
                "sudo",
                "docker",
                "pull",
                "--platform",
                "linux/amd64",
                f"{image}"
            ],
            stdout=log_file,
            stderr=subprocess.STDOUT
        )

    if result.returncode == 0:
        subprocess.run(
            [
                "sudo",
                "docker",
                "tag",
                f"{image}",
                f"{tag}"
            ]
        )

    return {
        "code": not result.returncode,
        "state": f"{bcolors.FAIL}Failed" if result.returncode == 1 else f"{bcolors.OKGREEN}Succeeded",
        "time": round(time()-start, 2),

    }


all_dir = sorted(os.listdir("./containers"))
STD_IMAGES = set([
    "httpd:2.4.34",
    "nginx:1.13.8-alpine",
    "ubuntu:18.04",
    "corentinaltepe/heirloom-mailx:latest",
    "mysql:8.0.12",
    "linuxserver/syncthing:131",
])

images = {}
count = 1
for image in STD_IMAGES:
    images.update({count: image})
    count += 1

# Get all images

for item in all_dir:
    if item[0:7] == "docker-":
        images.update({count: item})
        count += 1

# Get user input

choice = ""
while choice not in images and choice != 0:
    os.system("clear")
    print("Choose an image")
    print(f"\t0: all images")
    for key, value in images.items():
        print(f"\t{key}: {value}")
    choice = input("")
    try:
        choice = int(choice)
    except ValueError:
        pass

# Build images

os.system("clear")

to_build = [choice] if choice != 0 else images.keys()

progress = ""
total_success = 0
for key in to_build:
    image = images[key]
    print(f"{progress}{bcolors.OKBLUE}In Progress : {key} {image}{bcolors.ENDC}")
    if image in STD_IMAGES:
        res = pull(image)
    else:
        res = build(image)
    progress += f"{res['state']} : {key} {image} : {res['time']}{bcolors.ENDC}\n"
    os.system("clear")
    if res["code"]:
        total_success += 1

print(progress)

progress += f"Total: {total_success}/{len(images)}"
progress = progress.replace(f"{bcolors.FAIL}", "")
progress = progress.replace(f"{bcolors.OKGREEN}", "")
progress = progress.replace(f"{bcolors.OKBLUE}", "")
progress = progress.replace(f"{bcolors.ENDC}", "")

with open("./containers/build_result.log", "w") as build_result:
    build_result.write(progress)
