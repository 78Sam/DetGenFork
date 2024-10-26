import os
import difflib

cwd = os.path.dirname(os.path.abspath(__file__))

print(cwd)

cwd = f"{cwd}/captures/capture-022-nginxSSL/data/"

files = sorted(os.listdir(cwd))

html_files = [file for file in files if ".html" in file]

if not html_files:
    print("No HTML files found.")
    exit()

print(f"FIRST FILE: {html_files[0]}")

with open(os.path.join(cwd, html_files[0]), "r") as first_file:
    last_file_data = first_file.read()

for file in html_files[1:]:
    with open(os.path.join(cwd, file), "r") as current_file:
        current_file_data = current_file.read()
        if last_file_data != current_file_data:
            diff = difflib.unified_diff(
                last_file_data.splitlines(),
                current_file_data.splitlines(),
                fromfile=html_files[0],
                tofile=file,
                lineterm=''
            )
            print(f"Differences found in {file}:")
            for line in diff:
                print(line)
        last_file_data = current_file_data