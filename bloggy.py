from subprocess import check_output
out = check_output(["git", "rev-list", "master", "--reverse"])
print(out)