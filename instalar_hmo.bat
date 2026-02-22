@echo off
chcp 65001 >nul
title HMO Auditor — Instalacion

echo.
echo =====================================================
echo   HMO Auditor Elite - Instalacion en este equipo
echo =====================================================
echo.

:: Verificar Git
where git >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git no esta instalado.
    echo Descargalo desde https://git-scm.com y vuelve a ejecutar este script.
    pause
    exit /b 1
)

:: Verificar Python
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado.
    echo Descargalo desde https://python.org/downloads y vuelve a ejecutar.
    pause
    exit /b 1
)

set INSTALL_DIR=%USERPROFILE%\HMO_Auditor

echo Directorio de instalacion: %INSTALL_DIR%
echo.

if exist "%INSTALL_DIR%" (
    echo La aplicacion ya esta instalada. Actualizando...
    cd /d "%INSTALL_DIR%"
    git pull origin main
) else (
    echo Clonando repositorio...
    git clone https://github.com/hmotecnologico-create/HMO_AUDITOR.git "%INSTALL_DIR%"
    cd /d "%INSTALL_DIR%"
)

echo.
echo Instalando dependencias...
python -m pip install -r requirements.txt --quiet

echo.
echo Creando acceso directo en el escritorio...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%USERPROFILE%\Desktop\HMO Auditor.lnk'); $s.TargetPath = 'cmd'; $s.Arguments = '/k cd /d \"%INSTALL_DIR%\" && streamlit run streamlit_app.py'; $s.IconLocation = '%INSTALL_DIR%\assets\favicon.ico,0'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Save()"

echo.
echo =====================================================
echo   Instalacion completada!
echo   Usa el acceso directo "HMO Auditor" en tu escritorio
echo   Usuario inicial: admin
echo   Contrasena inicial: HMO2024!  (debes cambiarla al primer login)
echo =====================================================
echo.
pause
