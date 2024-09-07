"""Module that can sync local music files with a ftp to a remote device."""
import argparse
import ftplib
import os
import pathlib


def upload_file(ftp: ftplib.FTP, local_file_path, remote_file_path) -> None:
  """Uploads a file."""
  with open(local_file_path, "rb") as file:
    ftp.storbinary(f'STOR {remote_file_path}', file)


def sync_directories(ftp, local_dir, remote_dir) -> None:
  remote_files = ftp.nlst(remote_dir)

  for root, dirs, files in os.walk(local_dir):
    relative_path = os.path.relpath(root, local_dir)
    remote_path = str(pathlib.PurePosixPath(remote_dir) / relative_path.replace("\\", "/"))

    try:
      ftp.mkd(remote_path)
    except ftplib.error_perm as e:
      print(f"Directory {remote_path} already exists.")

    # Sync files
    for file in files:
      local_file_path = os.path.join(root, file)
      remote_file_path = str(pathlib.PurePosixPath(remote_path) / file)
      if remote_file_path not in remote_files:
        print(f"Uploading '{local_file_path}' to '{remote_file_path}'")
        upload_file(ftp, local_file_path, remote_file_path)

    for remote_file in remote_files:
      if remote_file not in files:
        full_remote_path = str(pathlib.PurePosixPath(remote_path) / remote_file)
        if is_file(ftp, full_remote_path):
          print(f"Deleting {remote_file} from remote directory.")
          ftp.delete(full_remote_path)
        else:
          print(f"Deleting remote directory {remote_file}.")
          delete_remote_directory(ftp, full_remote_path)


def is_file(ftp, path):
  try:
    ftp.size(path)  # Returns the file size if it's a file
    return True
  except ftplib.error_perm:
    return False


def delete_remote_directory(ftp, remote_dir):
  # List the contents of the directory
  try:
    files = ftp.nlst(remote_dir)
  except ftplib.error_perm as e:
    print(f"Error listing directory {remote_dir}: {e}")
    return

  for file in files:
    # Skip "." and ".." (which might be returned by some FTP servers)
    if file in [".", ".."]:
      continue

    full_path = str(pathlib.PurePosixPath(remote_dir) / file)

    try:
      # Check if it's a directory by trying to change into it
      ftp.cwd(full_path)
      # It's a directory, so recurse into it
      delete_remote_directory(ftp, full_path)
    except ftplib.error_perm:
      # It's a file, so delete it
      print(f"Deleting file: {full_path}")
      ftp.delete(full_path)

  # Once the directory is empty, delete it
  print(f"Removing directory: {remote_dir}")
  try:
    ftp.rmd(remote_dir)
  except ftplib.error_perm as e:
    print(f"Error removing directory {remote_dir}: {e}")


if __name__ == "__main__":
  # Create an ArgumentParser object
  parser = argparse.ArgumentParser()
  # Add arguments
  parser.add_argument('--input', nargs='+', help='Input file')
  parser.add_argument('--ip', nargs='+', help='IP address of iPhone')
  parser.add_argument('--port', nargs='?', help='Port of iPhone (Foobar2000) ftp')
  parser.add_argument('--user', nargs='?', help='Username of iPhone (Foobar2000) ftp')
  parser.add_argument('--password', nargs='+', help='Password of iPhone (Foobar2000) ftp')
  # Parse arguments
  args = parser.parse_args()
  # <editor-fold desc="FTP data (User depended)">
  if args.ip is None:
    raise ValueError("Please specify an IP address!")
  FTP_HOST = args.ip[0]  # "192.168.40.98"
  if args.port is None:
    FTP_PORT = 21
  else:
    FTP_PORT = int(args.port)
  if args.user is None:
    FTP_USER = "generic"
  else:
    FTP_USER = args.user
  if args.password is None:
    raise ValueError("Please specify a password!")
  FTP_PASSWORD = str(args.password[0])
  if args.input is None:
    raise ValueError("Please specify an input path!")
  LOCAL_MUSIC_DIR = args.input[0]
  REMOTE_MUSIC_DIR = "/foobar2000 Music Folder"

  # </editor-fold>
  # <editor-fold desc="FTP connection setup">
  ftp = ftplib.FTP()
  ftp.connect(FTP_HOST, FTP_PORT)
  ftp.login(FTP_USER, FTP_PASSWORD)
  # </editor-fold>
  # <editor-fold desc="File syncing">
  ftp.cwd(REMOTE_MUSIC_DIR)
  sync_directories(ftp, LOCAL_MUSIC_DIR, REMOTE_MUSIC_DIR)
  ftp.quit()
  # </editor-fold>
