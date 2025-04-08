# Setup logging
import logging
from tkinter import messagebox


LOG_FILE = "directory_index.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def exception_catcher(func):
    """Decorator to catch and log exceptions, then show an error message."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Exception in {func.__name__}: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"An error occurred:\n{e}")
    return wrapper