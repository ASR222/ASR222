# Renders each plate to ../assets/<name>.png at 2x. Usage: powershell -File design/render.ps1
$edge = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
$plates = @{ hero = 420; cortex = 500; hazebusters = 500; warehouse = 400 }
foreach ($name in $plates.Keys) {
  $out = Join-Path $PSScriptRoot "..\assets\$name.png"
  $src = "file:///" + (Join-Path $PSScriptRoot "$name.html").Replace('\', '/')
  $out = [IO.Path]::GetFullPath($out)
  & $edge --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --virtual-time-budget=6000 "--window-size=880,$($plates[$name])" "--screenshot=$out" $src | Out-Null
}
