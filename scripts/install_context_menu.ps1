param(
  [string]$ScriptPath = "C:\ShareImgWinIPad\send_to_ipad.ps1",
  [string]$ServerUrl = "http://YOUR-PC-IP:8787/upload"
)

$command = "powershell.exe -ExecutionPolicy Bypass -File `"$ScriptPath`" -ImagePath `"%1`" -ServerUrl `"$ServerUrl`""

New-Item -Path "Registry::HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\image\shell\SendToiPad" -Force | Out-Null
Set-ItemProperty -Path "Registry::HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\image\shell\SendToiPad" -Name "MUIVerb" -Value "iPadへ送る"
New-Item -Path "Registry::HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\image\shell\SendToiPad\command" -Force | Out-Null
Set-ItemProperty -Path "Registry::HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\image\shell\SendToiPad\command" -Name "(default)" -Value $command

Write-Host "Context menu installed."
