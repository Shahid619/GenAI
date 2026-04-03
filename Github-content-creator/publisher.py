"""
GitHub Content Publisher
Clones or updates a GitHub repository and pushes new content.
Uses GitHub Personal Access Token for authentication.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

try:
    import git
    from git import Repo
except ImportError:
    print("❌ GitPython not installed. Run: pip install gitpython")
    raise


class GitHubPublisher:
    """Publishes content to a GitHub repository."""

    def __init__(self, token: str, username: str, repo_name: str,
                 local_dir: str = "_repo_work"):
        """
        Initialize the publisher.

        Args:
            token: GitHub Personal Access Token (with 'repo' scope)
            username: GitHub username
            repo_name: Repository name
            local_dir: Local working directory for the repo
        """
        self.token = token
        self.username = username
        self.repo_name = repo_name
        self.local_dir = Path(local_dir)
        self.repo_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
        self.clean_url = f"https://github.com/{username}/{repo_name}.git"
        self.repo = None

    def setup_repo(self):
        """Clone the repo if it doesn't exist, or pull latest."""
        if self.local_dir.exists():
            print(f"📂 Found existing local repo. Pulling latest...")
            self.repo = Repo(self.local_dir)
            self.repo.remotes.origin.pull()
            print("✅ Repo updated.")
        else:
            print(f"📂 Cloning repository: {self.clean_url}")
            self.repo = Repo.clone_from(self.repo_url, self.local_dir)
            print("✅ Repo cloned.")

    def publish_file(self, file_path: str, commit_message: str) -> bool:
        """
        Add a file, commit, and push to the remote repository.

        Args:
            file_path: Path to the file to publish
            commit_message: Git commit message

        Returns:
            True if push was successful
        """
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                print(f"❌ File not found: {file_path}")
                return False

            # Copy file into the repo
            dest = self.local_dir / file_path.name
            shutil.copy2(file_path, dest)

            # Configure git identity (if not already set)
            with self.repo.config_writer() as cw:
                if not self.repo.config_reader().has_section("user"):
                    cw.set_value("user", "name", "AI Content Publisher")
                    cw.set_value("user", "email", "publisher@ai-content.local")

            # Stage, commit, push
            self.repo.index.add([file_path.name])
            self.repo.index.commit(commit_message)
            self.repo.remotes.origin.push()

            print(f"\n✅ Published: {file_path.name}")
            print(f"📝 Commit: {commit_message}")
            print(f"🔗 URL: {self.clean_url}/blob/main/{file_path.name}")

            return True

        except Exception as e:
            print(f"❌ Publish failed: {e}")
            return False

    def cleanup(self):
        """Remove local repo directory."""
        if self.local_dir.exists():
            shutil.rmtree(self.local_dir)
            print(f"🧹 Cleaned up local repo.")
