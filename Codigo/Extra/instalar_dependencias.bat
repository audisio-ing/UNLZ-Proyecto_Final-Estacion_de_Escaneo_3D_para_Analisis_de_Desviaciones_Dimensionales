@echo off
REM Script de instalación automática de dependencias
REM Instala todos los paquetes necesarios para ejecutar el sistema

echo ====================================
echo Instalando dependencias...
echo ====================================
echo.

REM Verificar que pip esté disponible
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado o pip no está disponible.
    echo Por favor, instala Python desde https://www.python.org/
    pause
    exit /b 1
)

echo Actualizando pip...
python -m pip install --upgrade pip

echo.
echo Instalando paquetes desde librerias.txt...
python -m pip install -r librerias.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Hubo un problema durante la instalación.
    pause
    exit /b 1
)

echo.
echo ====================================
echo Instalación completada exitosamente!
echo ====================================
echo.
echo Ahora puedes ejecutar:
echo   python Main.py
echo.
pause
