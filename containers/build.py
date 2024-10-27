import os
import subprocess
from time import time, sleep
from threading import Thread
from datetime import datetime
from cli import genCLI


running: bool = False


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


def printProgress(progress):
    start = time()
    while running:
        os.system("clear")
        print(f"{progress} : {round(time() - start, 2)}")
        sleep(1)


def build(image) -> dict:
    path = f"./containers/{image}"
    tag = f"detlearsom/{image[7::]}"
    start = time()
    with open(f"{path}/build_log.log", "w") as log_file:
        result = subprocess.run(
            [
                # "sudo",
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
                # "sudo",
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

if __name__ == "__main__":

    while True:

        all_dir = sorted(os.listdir("./containers"))
        STD_IMAGES = set([
            "httpd:2.4.34",
            "nginx:1.13.8-alpine",
            "ubuntu:18.04",
            "corentinaltepe/heirloom-mailx:latest",
            "mysql:8.0.12",
            "linuxserver/syncthing:131",
            "fauria/vsftpd:latest"
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

        choice = genCLI(["all"] + list(images.values()))[0]

        if choice == -1:
            exit()

        # Build images

        os.system("clear")

        to_build = [choice] if choice != 0 else images.keys()

        os.system("sudo echo ''")
        input("Start:")

        progress = ""
        total_success = 0
        for key in to_build:
            image = images[key]
            # print(f"{progress}{bcolors.OKBLUE}In Progress : {key} {image}{bcolors.ENDC}")
            running = True
            Thread(target=lambda: printProgress(f"{progress}{bcolors.OKBLUE}In Progress : {key} {image}{bcolors.ENDC}"), daemon=True).start()
            if image in STD_IMAGES:
                res = pull(image)
            else:
                res = build(image)
            running = False
            sleep(1.5)
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

        date_time = datetime.now().strftime("%d_%m_%Y_H%H_M%M")

        with open(f"./containers/build_result_{date_time}.log", "w") as build_result:
            build_result.write(progress)

        sleep(3)
