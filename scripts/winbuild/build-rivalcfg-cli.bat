:: Make and/or activate the virtualenv
IF NOT EXIST build\winbuild.venv (
    mkdir build
    python -m venv build\winbuild.venv
)
CALL build\winbuild.venv\Scripts\activate.bat

:: Install dependencies.
pip install -r scripts\winbuild\requirements.txt
pip install -e .

:: Compile with nuitka
python -m nuitka ^
    --mode=standalone ^
    --follow-imports ^
    --python-flag=-O,isolated ^
    --no-deployment-flag=self-execution ^
    --assume-yes-for-downloads ^
    --windows-console-mode=force ^
    --windows-icon-from-ico=scripts\winbuild\rivalcfg.ico ^
    --output-dir=.\build\rivalcfg.winbuild ^
    --output-filename=rivalcfg.exe ^
    scripts\winbuild\rivalcfg-cli.py

:: Copy additional files...
copy LICENSE build\rivalcfg.winbuild\rivalcfg-cli.dist\LICENSE.txt
copy scripts\winbuild\README.dist.rst build\rivalcfg.winbuild\rivalcfg-cli.dist\README.txt

:: Leave the virtualenv
deactivate
