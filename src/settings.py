import os
import re
from typing import Optional, List


class Settings:
    """A class to hold settings for the program"""

    def __init__(
        self,
        in_directory: Optional[str] = None,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        out_path: Optional[str] = None,
        index_hidden_files: Optional[bool] = None,
    ):
        self.in_directory = in_directory or os.getcwd()
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or []
        self.index_hidden_files = index_hidden_files or False
        self.out_path = out_path or os.getcwd()

    def validate(self):
        """Validate that the settings are valid

        Raises:
            ValueError: A setting is invalid
        """
        if not isinstance(self.include_patterns, list) or not all(isinstance(p, str) and re.compile(p) for p in self.include_patterns):
            raise ValueError("include_patterns must be a list of valid regex.")

        if not isinstance(self.exclude_patterns, list) or not all(isinstance(p, str) and re.compile(p) for p in self.exclude_patterns):
            raise ValueError("exclude_patterns must be a list of valid regex.")

        if not os.path.isdir(self.in_directory):
            raise ValueError(f"The directory '{self.in_directory}' does not exist.")

        # Validate the output path (it should be a directory)
        if not os.path.isdir(self.out_path) and not os.path.exists(self.out_path):
            raise ValueError(f"The output path '{self.out_path}' is invalid.")


    def __repr__(self):
        return (
            f"Settings("
            f"in_directory={self.in_directory!r}, "
            f"include_patterns={self.include_patterns!r}, "
            f"exclude_patterns={self.exclude_patterns!r}, "
            f"index_hidden_files={self.index_hidden_files!r}, "
            f"out_path={self.out_path!r}"
            ")"
        )

