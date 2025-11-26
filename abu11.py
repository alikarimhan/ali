

import subprocess
from datetime import datetime

def get_git_commit_hash():
    try:
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD']
        ).decode('utf-8').strip()
        return commit_hash
    except subprocess.CalledProcessError:
        return "Git commit табылмады"

def get_git_commit_date():
    try:
        commit_date = subprocess.check_output(
            ['git', 'log', '-1', '--format=%cd']
        ).decode('utf-8').strip()
        return commit_date
    except subprocess.CalledProcessError:
        return "Commit уақыты табылмады"

def save_build_info():
    commit_hash = get_git_commit_hash()
    commit_date = get_git_commit_date()
    build_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("build_info.txt", "w", encoding="utf-8") as file:
        file.write(f"Commit hash: {commit_hash}\n")
        file.write(f"Commit date: {commit_date}\n")
        file.write(f"Build time: {build_time}\n")

    print("✅ build_info.txt файлы жаңартылды.")

if __name__ == "__main__":
    save_build_info()
