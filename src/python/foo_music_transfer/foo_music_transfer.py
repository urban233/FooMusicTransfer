#
# Foo Music Transfer - Software for transferring music to a foobar2000 mobile device.
#
# Copyright (C) 2024
# Martin Urban (martin.urban@studmail.w-hs.de)
#
# Source code is available at <https://github.com/urban233/FooMusicTransfer>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""Module that can sync local music files with a ftp to a remote device."""
import ftplib
import os
import pathlib
import subprocess
import sys
import time
import toml
from dataclasses import dataclass

__docformat__ = "google"


@dataclass
class Arguments:
  """Arguments that are needed for the transfer."""

  # <editor-fold desc="Class attributes">
  _input: str
  """The path to the input directory."""
  _ip: str
  """The ip address of the device."""
  _port: int
  """The port number the ftp uses."""
  user: str
  """The username the ftp uses."""
  password: str
  """The password the ftp uses."""
  # </editor-fold>

  def __init__(self) -> None:
    """Constructor."""
    self._input = ""
    self._ip = ""
    self._port = -1
    self.user = ""
    self.password = ""

  def get_input(self) -> str:
    """Gets the input path.

    Returns:
      The path to the input directory.
    """
    return self._input

  def get_ip(self) -> str:
    """Gets the ip address.

    Returns:
      The ip address.
    """
    return self._ip

  def get_port(self) -> int:
    """Gets the port number.

    Returns:
      The port number.
    """
    return self._port

  def set_input(self, an_input: str) -> None:
    """Sets the input.

    Args:
      an_input: The path to the input directory.

    Raises:
      ValueError: If an_input is None, an empty string or an invalid path.
    """
    # <editor-fold desc="Checks">
    if an_input is None:
      raise ValueError("an_input is None.")
    if an_input == "":
      raise ValueError("an_input is an empty string.")
    if not pathlib.Path(an_input).exists():
      raise ValueError("Invalid path!")
    # </editor-fold>
    self._input = an_input

  def set_ip(self, an_ip: str) -> None:
    """Sets the ip.

    Args:
      an_ip: The ip address of the ftp server.

    Raises:
      ValueError: If an_ip is None, an empty string or an invalid ip address.
    """
    # <editor-fold desc="Checks">
    if an_ip is None:
      raise ValueError("an_ip is None.")
    if an_ip == "":
      raise ValueError("an_ip is an empty string.")
    if not an_ip.count(".") == 3:
      raise ValueError("Invalid IP format!")
    # </editor-fold>
    self._ip = an_ip

  def set_port(self, a_port: str) -> None:
    """Set the port.

    Args:
      a_port: The port number of the ftp server.

    Raises:
      ValueError: If a_port is None, an empty string or an invalid port number.
    """
    # <editor-fold desc="Checks">
    if a_port is None:
      raise ValueError("a_port is None.")
    if a_port == "":
      raise ValueError("a_port is an empty string.")
    if not int(a_port) > 0:
      raise ValueError("Invalid port number!")
    # </editor-fold>
    self._port = int(a_port)


def upload_file(a_ftp: ftplib.FTP, a_local_file_path, a_remote_file_path) -> None:
  """Uploads a file.

  Args:
    a_ftp: The ftp server connection.
    a_local_file_path: The local filepath of the music file to be uploaded to.
    a_remote_file_path: The remote filepath, where the music file should be stored.

  Raises:
    ValueError: If a_ftp is None or a_local_file_path is None, an empty string or an invalid path, or if a_remote_file_path is None or an empty string.
  """
  # <editor-fold desc="Checks">
  if a_ftp is None:
    raise ValueError("a_ftp is None.")
  if a_local_file_path is None:
    raise ValueError("a_local_file_path is None.")
  if a_local_file_path == "":
    raise ValueError("a_local_file_path is an empty string.")
  if not pathlib.Path(a_local_file_path).exists():
    raise ValueError("a_local_file_path could not be found!")
  if a_remote_file_path is None:
    raise ValueError("a_remote_file_path is None.")
  if a_remote_file_path == "":
    raise ValueError("a_remote_file_path is an empty string.")
  # </editor-fold>
  with open(a_local_file_path, "rb") as file:
    a_ftp.storbinary(f'STOR {a_remote_file_path}', file)


def sync_directories(a_ftp, a_local_dir, a_remote_dir) -> None:
  """Syncs the local directory with the remote one.

  Args:
    a_ftp: The ftp server connection.
    a_local_dir: The path to the local directory.
    a_remote_dir: The path to the remote directory.

  Raises:
    ValueError: If a_ftp is None or a_local_dir is None, an empty string or an invalid path, or if a_remote_dir is None or an empty string.
  """
  # <editor-fold desc="Checks">
  if a_ftp is None:
    raise ValueError("a_ftp is None.")
  if a_local_dir is None:
    raise ValueError("a_local_dir is None.")
  if a_local_dir == "":
    raise ValueError("a_local_dir is an empty string.")
  if not pathlib.Path(a_local_dir).exists():
    raise ValueError("a_local_dir could not be found!")
  if a_remote_dir is None:
    raise ValueError("a_remote_dir is None.")
  if a_remote_dir == "":
    raise ValueError("a_remote_dir is an empty string.")
  # </editor-fold>
  remote_files = a_ftp.nlst(a_remote_dir)

  for root, dirs, files in os.walk(a_local_dir):
    relative_path = os.path.relpath(root, a_local_dir)
    remote_path = str(pathlib.PurePosixPath(a_remote_dir) / relative_path.replace("\\", "/"))

    try:
      a_ftp.mkd(remote_path)
    except ftplib.error_perm as e:
      print(f"Directory {remote_path} already exists.")

    # Sync files
    for file in files:
      local_file_path = os.path.join(root, file)
      remote_file_path = str(pathlib.PurePosixPath(remote_path) / file)
      if remote_file_path not in remote_files:
        print(f"Uploading '{local_file_path}' to '{remote_file_path}'")
        upload_file(a_ftp, local_file_path, remote_file_path)

    for remote_file in remote_files:
      if remote_file not in files:
        full_remote_path = str(pathlib.PurePosixPath(remote_path) / remote_file)
        if is_file(a_ftp, full_remote_path):
          print(f"Deleting {remote_file} from remote directory.")
          a_ftp.delete(full_remote_path)
        else:
          print(f"Deleting remote directory {remote_file}.")
          delete_remote_directory(a_ftp, full_remote_path)


def is_file(a_ftp, a_path) -> bool:
  """Checks if the given path is a file.

  Args:
    a_ftp: The ftp server connection.
    a_path: The path to check.

  Returns:
    True if the path is a filepath, False otherwise.

  Raises:
    ValueError: If a_ftp is None or a_path is None, an empty string.
  """
  # <editor-fold desc="Checks">
  if a_ftp is None:
    raise ValueError("a_ftp is None.")
  if a_path is None:
    raise ValueError("a_path is None.")
  if a_path == "":
    raise ValueError("a_path is an empty string.")
  # </editor-fold>
  try:
    a_ftp.size(a_path)  # Returns the file size if it's a file
    return True
  except ftplib.error_perm:
    return False


def delete_remote_directory(a_ftp, a_remote_dir) -> None:
  """Deletes a (full) remote directory.

  Args:
    a_ftp: The ftp server connection.
    a_remote_dir: The path to the remote directory.

  Raises:
    ValueError: If a_ftp is None or a_remote_dir is None, an empty string.
  """
  # <editor-fold desc="Checks">
  if a_ftp is None:
    raise ValueError("a_ftp is None.")
  if a_remote_dir is None:
    raise ValueError("a_remote_dir is None.")
  if a_remote_dir == "":
    raise ValueError("a_remote_dir is an empty string.")
  # </editor-fold>
  try:
    files = a_ftp.nlst(a_remote_dir)
  except ftplib.error_perm as e:
    print(f"Error listing directory {a_remote_dir}: {e}")
    return

  for file in files:
    # Skip "." and ".." (which might be returned by some FTP servers)
    if file in [".", ".."]:
      continue

    full_path = str(pathlib.PurePosixPath(a_remote_dir) / file)

    try:
      # Check if it's a directory by trying to change into it
      a_ftp.cwd(full_path)
      # It's a directory, so recurse into it
      delete_remote_directory(a_ftp, full_path)
    except ftplib.error_perm:
      # It's a file, so delete it
      print(f"Deleting file: {full_path}")
      a_ftp.delete(full_path)

  # Once the directory is empty, delete it
  print(f"Removing directory: {a_remote_dir}")
  try:
    a_ftp.rmd(a_remote_dir)
  except ftplib.error_perm as e:
    print(f"Error removing directory {a_remote_dir}: {e}")


if __name__ == "__main__":
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
  try:
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
    input("\nTransfer completed. Press any key to close.")
  except Exception as e:
    print(f"An error occurred: {e}")
    input("Press any key to close.")
    sys.exit(1)
