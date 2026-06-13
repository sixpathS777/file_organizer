import shutil
from pathlib import Path
import zipfile


def extract_archive(zip_path, extract_to):
    try:
        # 'r' opens the file for reading only.
        # 'with' handles safe memory release automatically.
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        print(f"Extracted {zip_path.name}")
        return True
    except Exception as e:
        print(f"Error in extracting {zip_path.name}: {e}")
        return False


def organize_folder(folder_path):
    # Converts string to Path object and expands user shortcuts like '~'
    target_path = Path(folder_path).expanduser()

    if not target_path.exists():
        print(f"The directory {target_path} does not exist.")
        return

    extensions_map = {
        # Images
        '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', '.gif': 'Images', '.svg': 'Images',
        # Documents
        '.pdf': 'Doc', '.docx': 'Doc', '.txt': 'Doc', '.xlsx': 'Doc', '.pptx': 'Doc',
        # Audio/Video
        '.mp3': 'Media', '.mp4': 'Media', '.mov': 'Media', '.wav': 'Media',
        # Archives
        '.zip': 'Archives', '.tar': 'Archives', '.gz': 'Archives', '.rar': 'Archives',
        # Code/Executables
        '.py': 'Code', '.js': 'Code', '.html': 'Code', '.exe': 'Executables', '.dmg': 'Executables'
    }

    print(f"Checking for zip files in {target_path}...")
    # FIXED: Added () to is_file() and added the '.' to '.zip'
    for item in target_path.iterdir():
        if item.is_file() and item.suffix.lower() == '.zip':
            extract_archive(item, target_path)

    print(f"\nStarting cleaning in {target_path}")
    moved_count = 0

    for item in target_path.iterdir():
        if item.is_file():
            file_extension = item.suffix.lower()

            # Skip files with no extensions or hidden configurations (e.g., .DS_Store, .gitignore)
            if not file_extension or item.name.startswith('.'):
                continue

            category = extensions_map.get(file_extension, "Others")
            destination_dir = target_path / category

            # exist_ok=True prevents an error if the directory already exists
            destination_dir.mkdir(exist_ok=True)

            destination_file = destination_dir / item.name
            counter = 1

            # Resolves duplicate naming issues by appending a counter
            while destination_file.exists():
                new_name = f"{item.stem}_{counter}{file_extension}"
                destination_file = destination_dir / new_name
                counter += 1

            try:
                # shutil.move works seamlessly with Path objects natively
                shutil.move(item, destination_file)
                print(f"Moving {item.name} -> {destination_dir.name}/{destination_file.name}")
                moved_count += 1
            except Exception as e:
                print(f"Error in moving {item.name} to {destination_file}: {e}")

    print(f"\nSuccessfully cleaned and organized {moved_count} files.")


# Execution Block
if __name__ == "__main__":
    target_folder = "~/Downloads"
    organize_folder(target_folder)