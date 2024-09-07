#
# TEA - Task Event-based Async library for Python
# Copyright (C) 2024
# Martin Urban (martin.urban@studmail.w-hs.de)
# Hannah Kullik (hannah.kullik@studmail.w-hs.de)
#
# Source code is available at <https://github.com/urban233/TEA>
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
"""Defines invoke tasks."""
import pathlib
import shutil
import subprocess

from invoke import task


@task()
def build(c):
  """Builds the inno setup."""
  try:
    # Define project root directory
    tmp_project_root_path = pathlib.Path(__file__).parent.absolute()
    tmp_inno_setup_input_path = pathlib.Path(f"{tmp_project_root_path}/src/inno_setup/input")
    if not tmp_inno_setup_input_path.exists():
      tmp_inno_setup_input_path.mkdir(parents=True, exist_ok=True)
    # Compile and copy FooMusicTransfer .exe file
    tmp_dist_filepath = pathlib.Path(f"{tmp_project_root_path}/dist/foo_music_transfer.exe")
    c.run(f"pyinstaller --onefile {tmp_project_root_path}\\src\\python\\foo_music_transfer\\foo_music_transfer.py")
    shutil.copy(tmp_dist_filepath, tmp_inno_setup_input_path / "foo_music_transfer.exe")
    # Copy config.toml
    tmp_config_filepath = pathlib.Path(f"{tmp_project_root_path}/src/python/foo_music_transfer/config.toml")
    shutil.copy(tmp_config_filepath, tmp_inno_setup_input_path / "config.toml")
    # Copy logo.ico
    tmp_logo_filepath = pathlib.Path(f"{tmp_project_root_path}/assets/logo.ico")
    shutil.copy(tmp_logo_filepath, tmp_inno_setup_input_path / "logo.ico")
    # Compile inno setup script
    tmp_inno_setup_compiler_filepath = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    subprocess.run([tmp_inno_setup_compiler_filepath, f"{tmp_project_root_path}/src/inno_setup/setup.iss"])
    shutil.rmtree(tmp_inno_setup_input_path)
  except Exception as e:
    print(f"Error while running 'build' task: {e}")
  finally:
    print("Finished task 'build'.")
