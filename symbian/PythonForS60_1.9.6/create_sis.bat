REM 
REM DO NOT TRY TO GENERATE THE SIS FILE IF YOUR PATH CONTAINS SPACES.
REM ENSYMBLE DOES NOT SUPPORT THEM ! COPY THIS PROJECT TO C:\
REM BEFORE RUNNING THIS SCRIPT.
REM
@echo off

SET PYTHON=C:\Python25\python.exe
SET APPNAME=pymo
SET CAPBLS=ReadUserData
SET SRCDIR=src
SET WMTMPDIR=src.tmp
SET ICON=..\PythonForS60\icon.svg  
SET VERSION=1.1.0
SET VERSIONSTRING=v1_1_0_S60_MR
SET EXTRAMODULE=_codecs_cn

REM put you zip tool here
SET ZIP="C:\Program Files\7-Zip\7z.exe"
REM Path to module-repo, inside Python For S60 
SET PYS60DIR=.\
SET RESDIR=..\pymo

SET OPTS=--verbose  --version="%VERSION%" ^
--appname="%APPNAME%" --icon="%ICON%" ^
--extrasdir=extras --caps=%CAPBLS% --extra-modules="%EXTRAMODULE%"

mkdir %WMTMPDIR%\extras\data\pymo
copy  %RESDIR%\*.*  %WMTMPDIR%\extras\data\pymo
copy  ..\app.py  %WMTMPDIR%\ 
copy  ..\default.py  %WMTMPDIR%\
              
if not exist .\module-repo\ xcopy /E "%PYS60DIR%\module-repo" .\module-repo\
if not exist .\templates\   xcopy /E "%PYS60DIR%\templates"   .\templates\
if not exist ensymble.py    xcopy /E "%PYS60DIR%\ensymble.py" .
if not exist openssl.exe    xcopy /E "%PYS60DIR%\openssl.exe" .
xcopy /E "%PYS60DIR%\PyS60Dependencies\*.sis" .

echo "Copying extensions"
xcopy /E/Y extensions\* .\module-repo\dev-modules\

echo "Generating for Python 1.9.6"
%PYTHON% ensymble.py py2sis %OPTS% "%WMTMPDIR%" "%APPNAME%_%VERSIONSTRING%.sis"

echo "Zipping source files"
%ZIP% a -tzip "%APPNAME%_%VERSIONSTRING%.zip" "%APPNAME%_%VERSIONSTRING%.sis" "PythonScriptShell_1.9.6_3_0.sis" "Python_1.9.6_fixed.sis" "MR版安装说明.txt"

del "*.sis"
RD /S /Q %WMTMPDIR%