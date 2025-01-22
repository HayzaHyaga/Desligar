!define APPNAME "Agendar Desligamento"
!define EXEFILE "seu_script.exe"
!define OUTPUT "Instalador-AgendarDesligamento.exe"

SetCompressor lzma

OutFile "${OUTPUT}"
InstallDir "$PROGRAMFILES\${APPNAME}"

Section
    SetOutPath "$INSTDIR"
    File "dist\${EXEFILE}"
    CreateShortcut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${EXEFILE}"
SectionEnd