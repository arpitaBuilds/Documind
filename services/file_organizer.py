import os
import shutil
from pathlib import Path
from config.settings import settings

class FileOrganizer:
    """Handles physical file organization by copying/moving documents into suggested folder hierarchies."""

    ORGANIZED_BASE_DIR = os.path.join(settings.BASE_DIR, "organized_documents")

    @classmethod
    def organize_file(cls, source_path: str, suggested_folder: str) -> dict:
        """
        Physically moves/copies the source file to target organized folder structure.
        Example: organized_documents/Education/Web_Development/Experiment_8.pdf
        """
        if not source_path or not os.path.exists(source_path):
            return {
                "success": False,
                "message": f"Source file does not exist on disk: {source_path}",
                "target_path": None
            }

        file_name = os.path.basename(source_path)
        
        # Clean folder path
        clean_folder = suggested_folder.strip().strip("/").strip("\\")
        target_dir = os.path.join(cls.ORGANIZED_BASE_DIR, clean_folder)

        try:
            # Ensure target directory exists
            os.makedirs(target_dir, exist_ok=True)

            target_path = os.path.join(target_dir, file_name)

            # Copy file to organized folder
            shutil.copy2(source_path, target_path)

            rel_target_path = os.path.relpath(target_path, settings.BASE_DIR)

            return {
                "success": True,
                "message": f"Successfully organized '{file_name}' to target location.",
                "target_path": target_path,
                "relative_path": rel_target_path
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to organize file: {str(e)}",
                "target_path": None
            }
