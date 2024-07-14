import time

class FileSystemNode:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content
        self.children = {}

class Commit:
    def __init__(self, message, snapshot):
        self.message = message
        self.timestamp = time.time()
        self.snapshot = snapshot

class Branch:
    def __init__(self, name, root):
        self.name = name
        self.commits = [Commit("Initial commit", root)]

    def get_current_snapshot(self):
        return self.commits[-1].snapshot

class Repository:
    def __init__(self, name):
        self.name = name
        self.root = FileSystemNode("/")
        self.branches = {"main": Branch("main", self.copy_file_system_node(self.root))}
        self.current_branch = "main"

    def get_current_branch(self):
        return self.branches[self.current_branch]

    def copy_file_system_node(self, node):
        new_node = FileSystemNode(node.name, node.content)
        for name, child in node.children.items():
            new_node.children[name] = self.copy_file_system_node(child)
        return new_node

    def commit(self, message, changes):
        new_snapshot = self.copy_file_system_node(self.get_current_branch().get_current_snapshot())

        for path, content in changes.items():
            parts = path.split('/')
            current_node = new_snapshot
            for part in parts[:-1]:
                if part not in current_node.children:
                    current_node.children[part] = FileSystemNode(part)
                current_node = current_node.children[part]
            current_node.children[parts[-1]] = FileSystemNode(parts[-1], content)

        self.get_current_branch().commits.append(Commit(message, new_snapshot))

    def create_branch(self, branch_name):
        self.branches[branch_name] = Branch(branch_name, self.copy_file_system_node(self.get_current_branch().get_current_snapshot()))

    def switch_branch(self, branch_name):
        if branch_name in self.branches:
            self.current_branch = branch_name
        else:
            print("Branch not found.")

    def merge_branch(self, source_branch, target_branch):
        if source_branch not in self.branches or target_branch not in self.branches:
            print("One of the branches not found.")
            return

        source_snapshot = self.branches[source_branch].get_current_snapshot()
        target_snapshot = self.branches[target_branch].get_current_snapshot()

        changes = {}
        conflicts = set()

        def traverse(source, target, path):
            if source.content != target.content:
                if target.content == "":
                    changes[path] = source.content
                else:
                    conflicts.add(path)

            for name, child in source.children.items():
                traverse(child, target.children.get(name, FileSystemNode(name)), path + "/" + name)

        traverse(source_snapshot, target_snapshot, "")

        if not conflicts:
            for path, content in changes.items():
                self.commit(f"Merge from {source_branch} to {target_branch}", {path: content})
            print("Merged successfully without conflicts.")
        else:
            print("Merge conflicts found:")
            for conflict in conflicts:
                print(conflict)

    def resolve_conflict(self, conflict_id, resolution):
        self.commit(f"Conflict resolution for {conflict_id}", {conflict_id: resolution})

    def view_commit_history(self, branch_name):
        if branch_name not in self.branches:
            print("Branch not found.")
            return

        for commit in self.branches[branch_name].commits:
            print(f"Commit message: {commit.message}")
            print(f"Timestamp: {time.ctime(commit.timestamp)}")

    def view_file_history(self, file_path):
        for branch_name, branch in self.branches.items():
            print(f"Branch: {branch_name}")
            for commit in branch.commits:
                parts = file_path.split('/')
                current_node = commit.snapshot
                for part in parts:
                    if part in current_node.children:
                        current_node = current_node.children[part]
                    else:
                        current_node = None
                        break

                if current_node is not None:
                    print(f"Commit message: {commit.message}")
                    print(f"Timestamp: {time.ctime(commit.timestamp)}")
                    print(f"Content: {current_node.content}")

# Driver Function
if __name__ == "__main__":
    repo = Repository("MyRepo")

    repo.commit("Initial Commit", {})

    repo.commit("Add file1.txt", {"dir/file1.txt": "Hello there!!!"})
    repo.commit("Add file2.txt", {"dir/file2.txt": "We had fun today :)"})

    repo.create_branch("feature")

    repo.switch_branch("feature")

    repo.commit("Modify file1.txt in feature branch", {"dir/file1.txt": "Modified content of file1 in feature branch"})

    repo.switch_branch("main")

    repo.merge_branch("feature", "main")

    repo.view_commit_history("main")

    repo.view_file_history("dir/file1.txt")
