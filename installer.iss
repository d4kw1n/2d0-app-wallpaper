[Setup]
AppName=2Do
AppVersion=1.0
DefaultDirName={pf}\2Do
DefaultGroupName=2Do
OutputDir=.
OutputBaseFilename=2DoSetup
Compression=lzma
SolidCompression=yes
SetupIconFile=assets\logo.ico

[Files]
Source: "dist\\2Do.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\\*"; DestDir: "{app}\\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\2Do"; Filename: "{app}\\2Do.exe"
Name: "{userdesktop}\\2Do"; Filename: "{app}\\2Do.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"