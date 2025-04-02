import os
from typing import Optional


class Settings:
    """A class to hold settings for the program"""

    def __init__(self, in_directory: Optional[str] = None, extensions: Optional[str] = None, out_path: Optional[str] = None):
        self.in_directory = in_directory or os.getcwd()
        self.extensions = extensions or ".*"
        self.out_path = out_path or os.getcwd()

    def validate(self):
        """Validate that the selected directories exists

        Raises:
            ValueError: A directory doesn't exist or is invalid
        """
        if not os.path.isdir(self.in_directory):
            raise ValueError(f"The directory '{self.in_directory}' does not exist.")

        # Validate the output path (it should be a directory)
        if not os.path.isdir(self.out_path) and not os.path.exists(self.out_path):
            raise ValueError(f"The output path '{self.out_path}' is invalid.")

    def __repr__(self):
        return f"Settings(directory={self.in_directory}, extensions={self.extensions}, out_path"
