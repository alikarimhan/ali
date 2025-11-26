import subprocess
import csv
import datetime
import os


CSV_FILE = "changes.csv"


def run_git(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Git қатесі:", result.stderr.strip())
        return None
    return result.stdout.strip()


def check_git_repo():
    result = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                            capture_output=True, text=True)
    return result.returncode == 0


def get_changes():
    output = run_git(["git", "status", "--short"])
    if not output:
        return []

    changes = []
    for line in output.split("\n"):
        if line.strip():
            status = line[:2].strip()
            filename = line[3:].strip()
            changes.append((status, filename))

    return changes


def write_csv(changes):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Status", "Filename", "Timestamp"])
        now = datetime.datetime.now().isoformat()

        for status, filename in changes:
            writer.writerow([status, filename, now])


def git_commit_and_push():
    print("CSV файл Git-ке қосылуда...")
    run_git(["git", "add", CSV_FILE])

    print("Commit жасалуда...")
    run_git(["git", "commit", "-m", "Автоматты CSV жаңарту"])

    print("GitHub-қа push жасалуда...")
    push_result = run_git(["git", "push"])

    if push_result is not None:
        print("✔ GitHub-қа push сәтті жасалды!")
    else:
        print("❌ Push кезінде қате пайда болды.")


def main():
    print("GitHub автоматты тексеру іске қосылды...\n")

    if not check_git_repo():
        print("❌ Қате: Бұл қалта Git репозиторий емес!")
        print("Алдымен орындаңыз: git init")
        return

    changes = get_changes()

    if not changes:
        print("Өзгерістер жоқ — CSV жасалмайды.")
        return

    print("Табылған өзгерістер CSV-ге сақталуда...")
    write_csv(changes)

    print("CSV дайын. GitHub-қа жүктеу басталды...")
    git_commit_and_push()


if __name__ == "__main__":
    main()
