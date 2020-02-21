from tempfile import TemporaryDirectory
from subprocess import run, check_output, CalledProcessError

class ChangedFile():

    def __init__(self, name: str, diff: str):
        self.name = name
        self.diff = diff

    def __str__(self):
        return self.name

class Step():

    def __init__(self, message: str, changes: list):
        self.message = message
        self.changes = changes

    def __str__(self):
        return self.message

class Blog():

    def __init__(self, repo: str):
        self.repo = repo
        with TemporaryDirectory() as tmpdir:
            try:
                clone_process = run(['git', 'clone', repo, tmpdir], capture_output=True, check=True)
            except CalledProcessError as e:
                raise e
            try:
                commits_process = run(['git', '-C', tmpdir, "rev-list", "master", "--reverse"], capture_output=True, check=True)
            except CalledProcessError as e: 
                raise e
            commits_raw = commits_process.stdout.decode('utf-8')
            commits = commits_raw.split('\n')[:-1]
            steps = []

            for i in range(1, len(commits)):

                current_commit = commits[i]
                previous_commit = commits[i-1]
                try:
                    commit_message_process = run(['git', '-C', tmpdir, 'show', '-s', '--format=%B', current_commit], capture_output=True, check=True)
                except CalledProcessError as e: 
                    raise e
                commit_message = commit_message_process.stdout.decode('utf-8').strip()
                try:
                    changed_files_process = run(['git', '-C', tmpdir, 'diff-tree', '-r', '--no-commit-id', '--name-only', current_commit], capture_output=True, check=True)
                except CalledProcessError as e: 
                    raise e
                changed_files_raw = changed_files_process.stdout.decode('utf-8')
                changed_files = changed_files_raw.split('\n')[:-1]
                changes = []
                for f in changed_files:
                    try:
                        file_diff_process = run(['git', '-C', tmpdir,'diff', '--color-words', previous_commit, current_commit, f], capture_output=True, check=True)
                    except CalledProcessError as e: 
                        raise e
                    file_diff = file_diff_process.stdout.decode('utf-8')
                    changes.append(ChangedFile(f, file_diff))
                steps.append(Step(commit_message, changes))
        self.steps = steps

    def __str__(self):
        blog_str = ''

        for step in self.steps:
            blog_str += 'MESSAGE: ' + step.message + '\n\n'
            for change in step.changes:
                blog_str += '\tCHANGE: ' + change.name + '\n\n'
                blog_str += '\n'.join(['\t\t' + line for line in change.diff.split('\n')]) + '\n'
            blog_str += '=========================================================\n\n'

        return blog_str

if __name__ == "__main__":
    b = Blog('git@github.com:nickmpaz/tiny-tetris.git')
    print(b)