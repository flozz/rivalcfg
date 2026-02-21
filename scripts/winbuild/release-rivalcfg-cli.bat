:: Get the Rivalcfg version
FOR /F %%i IN ('python -c "import tomllib;print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"') DO (
    SET VERSION=%%i
)

:: Output name
SET OUTPUT_NAME=rivalcfg-cli_v%VERSION%_windows_x86_64

:: Create required folders
mkdir build
mkdir build\rivalcfg.winbuild
mkdir dist

:: Release
xcopy /E /Y build\rivalcfg.winbuild\rivalcfg-cli.dist build\rivalcfg.winbuild\%OUTPUT_NAME%\
cd build\rivalcfg.winbuild
powershell Compress-Archive %OUTPUT_NAME% ..\..\dist\%OUTPUT_NAME%.zip
cd ..\..
