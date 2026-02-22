@echo off
chcp 65001 >nul
title HMO Auditor — Recuperacion de Acceso de Emergencia
color 0C
echo.
echo =====================================================
echo   HMO Auditor - RECUPERACION DE ACCESO
echo   SOLO personal autorizado con clave maestra HMO
echo =====================================================
echo.

:: Buscar Python
where python >nul 2>&1
if errorlevel 1 (
    where python3 >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python no encontrado. Instala Python 3.9+ primero.
        pause
        exit /b 1
    )
    set PYTHON=python3
) else (
    set PYTHON=python
)

:: Cambiar al directorio del script
cd /d "%~dp0"

echo Iniciando recuperacion de acceso...
echo.
%PYTHON% HMO_Auth.py

echo.
echo Proceso completado. Presiona cualquier tecla para cerrar.
pause >nul
