; Script generated by the Inno Script Studio Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
WizardImageFile=compiler:WizClassicImage.bmp
AppName=FooMusicTransfer
AppVersion=0.2.0
AppCopyright=Martin Urban
AppId={{192F52C3-D86D-4735-9929-C2DF593CB534}
DefaultDirName={userappdata}\FooMusicTransfer
AppPublisher=Martin Urban
VersionInfoProductName=FooMusicTransfer
MinVersion=10.0.19045
OutputDir=out
OutputBaseFilename=foo_music_transfer_setup-0_2_0-win64
VersionInfoCopyright=GNU GPL-3.0
DisableDirPage=True
DisableProgramGroupPage=True
ArchitecturesInstallIn64BitMode=x64
WizardStyle=modern
DisableReadyPage=True
DisableFinishedPage=True
UninstallDisplayName=FooMusicTransfer
UninstallDisplayIcon={app}\assets\logo.ico
LicenseFile=LICENSE.txt
; This is necessary if the setup will exceed 2 GB
DiskSpanning=no
; DiskSliceSize=2100000000
PrivilegesRequired=none

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Dirs]
Name: "{userappdata}\FooMusicTransfer"
Name: "{userappdata}\FooMusicTransfer\bin"

[Files]
Source: "input\foo_music_transfer.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "input\config.toml"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs;
Source: "input\logo.ico"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs;


[Icons]
Name: "{userdesktop}\Foo Music Transfer"; Filename: "{app}\bin\foo_music_transfer.exe"; IconFilename: "{app}\assets\logo.ico"
Name: "{userstartmenu}\Foo Music Transfer"; Filename: "{app}\bin\foo_music_transfer.exe"; IconFilename: "{app}\assets\logo.ico"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
