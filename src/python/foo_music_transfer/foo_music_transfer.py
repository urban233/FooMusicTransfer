"""Module that can sync local music files with a ftp to a remote device."""
import argparse
import ftplib
import os
import pathlib
import subprocess
import sys
import time
from dataclasses import dataclass

import toml


@dataclass
class Arguments:
  """Arguments that are needed for the transfer."""
  _input: str
  _ip: str
  _port: int
  user: str
  password: str

  def __init__(self) -> None:
    """Initialize an empty object."""
    self._input = ""
    self._ip = ""
    self._port = -1
    self.user = ""
    self.password = ""

  def get_input(self) -> str:
    """Gets the input path."""
    return self._input

  def get_ip(self) -> str:
    """Gets the ip address."""
    return self._ip

  def get_port(self) -> int:
    """Gets the port number."""
    return self._port

  def set_input(self, an_input: str) -> None:
    """Set the input."""
    if pathlib.Path(an_input).exists():
      self._input = an_input
    else:
      raise ValueError("Invalid filepath!")

  def set_ip(self, an_ip: str) -> None:
    """Set the ip."""
    if an_ip.count(".") == 3:
      self._ip = an_ip
    else:
      raise ValueError("Invalid IP format!")

  def set_port(self, an_port: str) -> None:
    """Set the port."""
    if int(an_port) > 0:
      self._port = int(an_port)
    else:
      raise ValueError("Invalid port number!")


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
  # parser = argparse.ArgumentParser()
  # # Add arguments
  # parser.add_argument('--input', nargs='+', help='Input file')
  # parser.add_argument('--ip', nargs='+', help='IP address of iPhone')
  # parser.add_argument('--port', nargs='?', help='Port of iPhone (Foobar2000) ftp')
  # parser.add_argument('--user', nargs='?', help='Username of iPhone (Foobar2000) ftp')
  # parser.add_argument('--password', nargs='+', help='Password of iPhone (Foobar2000) ftp')
  # # Parse arguments
  # args = parser.parse_args()
  args = Arguments()
  try:
    print("+++-----------------------------------------------+++")
    print("         --- Welcome to FooMusicTransfer ---")
    print("   The unofficial transfer software for Foobar2000")
    print("+++-----------------------------------------------+++")

    tmp_input = input("Do you want to (l)oad, (e)dit or (i)gnore the default config? \n")
    if tmp_input == "l":
      # Read the config.toml file
      tmp_appdata_roaming_path = pathlib.Path(os.getenv('APPDATA'))
      tmp_config_filepath = pathlib.Path(f"{tmp_appdata_roaming_path}/FooMusicTransfer/config.toml")
      with open(str(tmp_config_filepath), "r") as f:
        config = toml.load(f)
      args.set_input(config["input"]["input_path"])
      args.set_ip(config["ftp"]["host"])
      args.set_port(config["ftp"]["port"])
      args.user = config["ftp"]["user"]
      args.password = config["ftp"]["password"]
    elif tmp_input == "e":
      tmp_appdata_roaming_path = pathlib.Path(os.getenv('APPDATA'))
      tmp_config_filepath = pathlib.Path(f"{tmp_appdata_roaming_path}/FooMusicTransfer/config.toml")
      print("CAUTION! If you change the 'input_path' you have to use double backslashes!!")
      input("Press any key to edit the config.toml file. This will also exit the program.")
      subprocess.Popen(["notepad.exe", str(tmp_config_filepath)])
      sys.exit(0)
    elif tmp_input == "i":
      args.set_input(
        input("Please enter a path to the directory you want to sync to your iPhone: \n")
      )
      args.set_ip(
        input("Please enter the IP address of your iPhone: \n")
      )
      args.set_port(
        input("Please enter the port number of your iPhone: \n")
      )
      args.user = input("Please enter the username of your iPhone's ftp: \n")
      args.password = input("Please enter the password of your iPhone's ftp: \n")
    else:
      print("Wrong input, program will now exit ...")
      time.sleep(1)
      sys.exit(1)
  except Exception as e:
    print(f"An error occurred: {e}")
    input("Press any key to close.")
    sys.exit(1)
  # <editor-fold desc="FTP data (User depended)">
  FTP_HOST = args.get_ip()  # "192.168.40.98"
  FTP_PORT = args.get_port()
  FTP_USER = args.user
  FTP_PASSWORD = args.password
  LOCAL_MUSIC_DIR = args.get_input()
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
  input("Transfer completed. Press any key to close.")
