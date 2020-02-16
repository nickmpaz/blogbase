from subprocess import check_output


commits_raw = check_output(["git", "rev-list", "master", "--reverse"]).decode('utf-8')
commits = commits_raw.split('\n')[:-1]
for commit in commits:
    commit_message = check_output(["git", "show", "-s", "--format=%B", commit]).decode('utf-8')
    changed_files_raw = check_output(["git", "diff-tree", "-r", "--no-commit-id", "--name-only", commit]).decode('utf-8')
    changed_files = changed_files_raw.split('\n')[:-1]
    print(changed_files_raw)
# print(commits)