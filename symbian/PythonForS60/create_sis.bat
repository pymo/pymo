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
SET ICON=icon.svg
SET EXTRAMODULE=_codecs_cn
SET VERSION=1.2.0
SET VERSIONSTRING=v1_2_0_S60

REM put you zip tool here
SET ZIP="C:\Program Files\7-Zip\7z.exe"
REM Path to module-repo, inside Python For S60 
SET PYS60DIR=C:\Nokia\devices\Nokia_Symbian_Belle_SDK_v1.0\epoc32\winscw\c\data\python\PythonForS60
SET RESDIR=C:\Nokia\devices\Nokia_Symbian_Belle_SDK_v1.0\epoc32\winscw\c\Data\pymo

SET OPTS=--verbose  --version="%VERSION%" ^
--appname="%APPNAME%" --icon="%ICON%" ^
--extrasdir=extras --caps=%CAPBLS% --extra-modules="%EXTRAMODULE%"

mkdir %WMTMPDIR%\extras\data\pymo
copy  %RESDIR%\*.*  %WMTMPDIR%\extras\data\pymo
copy  ..\app.py  %WMTMPDIR%\
              
if not exist .\module-repo\ xcopy /E "%PYS60DIR%\module-repo" .\module-repo\
if not exist .\templates\   xcopy /E "%PYS60DIR%\templates"   .\templates\
if not exist ensymble.py    xcopy /E "%PYS60DIR%\ensymble.py" .
if not exist openssl.exe    xcopy /E "%PYS60DIR%\openssl.exe" .

echo "Copying extensions"
xcopy /E/Y extensions\* .\module-repo\dev-modules\

echo "Generating for Python 2.0.0"
%PYTHON% ensymble.py py2sis %OPTS% "%WMTMPDIR%" "%APPNAME%_%VERSIONSTRING%.sis"

echo "Zipping source files"
%ZIP% a -tzip "%APPNAME%_%VERSIONSTRING%.zip" "%APPNAME%_%VERSIONSTRING%.sis" "pips.sis" "PythonScriptShell_2.0.0_3_2.sis" "Python_2.0.0.sis"

