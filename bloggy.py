from subprocess import check_output
out = check_output(["git", "rev-list", "master", "--reverse"]).decode('utf-8')
print(out)