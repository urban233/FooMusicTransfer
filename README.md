# Foo Music Transfer

[**Overview**](#overview)
| [**What is Foo Music Transfer?**](#what-is-foo-music-transfer)
| [**Installation**](#installation)
| [**Getting Started**](#getting-started)
| [**Source**](#source)
| [**Contribute**](#contribute)

> [!IMPORTANT]
> 📣 **Foo Music Transfer is a CLI tool and has NO graphical user interface!** 📣
>
> As of this writing, only a command-line tool is available.
> This means there is **no** user-friendly graphical interface!
> Therefore, this software is intended for users familiar with
> Windows PowerShell and have prior experience using CLI tools.
>
> Foo Music Transfer is a best-effort, open-source project. This means support is not
> guaranteed, and the duration of the project's maintenance is uncertain.

<p align="center">
  <img alt="Logo" src="https://github.com/urban233/FooMusicTransfer/blob/main/assets/png/logo256.png"  width="225"/>
</p>

## What is Foo Music Transfer?

> Foo Music Transfer is a music transfer application that works 
> with an offline music library and the iOS version of Foobar2000.

## Overview<a id="overview"></a>
Foobar2000 lacks a built-in tool to sync local music files with its mobile app.
While there are other software tools available for this purpose, the recommended tool
from Foobar2000's developers is proprietary and not free.
Foo Music Transfer aims to provide an easier, hassle-free method for syncing your music library.
This program is intended for users who can operate Windows PowerShell, as Foo Music Transfer is currently only available as a command-line tool.

## Installation<a id="installation"></a>
To install Foo Music Transfer, run the installation setup (based on Inno Setup) from the [Releases](https://github.com/urban233/FooMusicTransfer/releases) tab.

Simply run the setup wizard and launch the application by double-clicking
the desktop icon created during installation.

### Installation Path
Foo Music Transfer will be installed in the `AppData\Roaming` directory
of the active user.

## Getting Started<a id="getting-started"></a>
To transfer music from your local library to your mobile device,
you can choose from the following options:
- Running a **one-time** configured transfer job
- Running a **default** configured transfer job

### Running a One-Time Configured Transfer Job
If you prefer not to save the transfer parameters
(e.g., IP address, port number, etc.), you can run
a one-time configured transfer job that will guide you
through the required parameters.
Once all parameters are entered, the job will begin.

### Running a Default Configured Transfer Job
If you plan to use the same configuration in the future,
you can use a configuration file. Access this by pressing
the `e` key (mnemonic for **e**dit configuration) when the program prompts you to choose
an action.

**IMPORTANT**: You **must** use double backslashes if you enter a path for the `input_path`!

You can then edit the configuration file and add your
preferred settings for future use.
Please note that only one configuration can be used at a time.
After editing, restart the program and load the configuration by pressing the
`l` key (mnemonic for **l**oad configuration).

## Source<a id="source"></a>
You can also build Foo Music Transfer from the source code.
To create the standalone executable, use PyInstaller in a
virtual environment.

```bash
$ pyinstaller --onefile /path/to/foo_music_transfer.py
```

In addition to compiling the executable from the source, you can also create the Inno Setup installer yourself. 
To do so, run the build invoke command.

```bash
$ invoke build
```

Ensure that you have invoke, pyinstaller, and the Inno Setup 6 compiler installed on your computer.

## Contribute<a id="contribute"></a>
- If you find any bugs or typos in the program or documentation, feel free to report them, and they may be fixed promptly.
- If you have any feature requests, please open an issue describing the new feature.
- If you clone the repository and develop additional features, feel free to open a pull request.
- If you'd like to contribute more documentation, you're welcome to do so. Please open a pull request.
