import subprocess
import re
from cli import genCLI
from time import sleep


def remove(image):
    subprocess.run([
        # "sudo",
        "docker",
        "rmi",
        image
    ])
    print(f"Removed Image: {image}")


if __name__ == "__main__":

    while True:

        with open("installed.txt", "w") as output_file:
            subprocess.run([
                # "sudo",
                "docker",
                "images"
            ], stdout=output_file)

        with open("installed.txt", "r") as output_file:
            out_images = output_file.read().split("\n")

        images = []
        for image in out_images[1:-1:]:
            formatted_image = re.sub(r'\s+', ',', image).split(",")
            formatted_image = "".join([formatted_image[0], ":", formatted_image[1]])
            images.append(formatted_image)

        images = sorted(images)
        images.insert(0, "all")

        choice = genCLI(images)[0]

        if choice == -1:
            subprocess.run([
                # "sudo",
                "rm",
                "installed.txt"
            ])
            exit()
        elif choice == 0:
            for image in images[1::]:
                remove(image)
        else:
            remove(images[choice])

        subprocess.run([
            # "sudo",
            "rm",
            "installed.txt"
        ])

        sleep(2)