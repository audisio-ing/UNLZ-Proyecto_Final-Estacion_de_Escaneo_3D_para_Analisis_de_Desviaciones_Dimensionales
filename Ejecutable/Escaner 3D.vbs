Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Obtener la carpeta del script
strScriptFolder = objFSO.GetParentFolderName(WScript.ScriptFullName)
strDatosFolder = objFSO.BuildPath(strScriptFolder, "Datos")
strMainPy = objFSO.BuildPath(strDatosFolder, "Main.py")

' Verificar que existe Main.py
If Not objFSO.FileExists(strMainPy) Then
    WScript.Echo "ERROR: No se encontro Main.py en " & strDatosFolder
    WScript.Quit 1
End If

' Ejecutar Python con Main.py sin mostrar ventana (0 = oculta)
objShell.CurrentDirectory = strDatosFolder
objShell.Run "python Main.py", 0, False
