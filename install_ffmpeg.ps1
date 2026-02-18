$ErrorActionPreference = "Stop"
$workdir = "C:\Users\abdul\.gemini\antigravity\scratch\ffmpeg_tool"
New-Item -ItemType Directory -Force -Path $workdir | Out-Null
Set-Location $workdir

Write-Host "1. Downloading FFmpeg (This might take a minute)..."
$url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$zip = "$workdir\ffmpeg.zip"

try {
    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
} catch {
    Write-Error "Download failed. Please check your internet connection."
    exit 1
}

Write-Host "2. Extracting files..."
Expand-Archive -Path $zip -DestinationPath $workdir -Force

$ffmpegBinary = Get-ChildItem -Path $workdir -Recurse -Filter "ffmpeg.exe" | Select-Object -First 1

if ($ffmpegBinary) {
    $binPath = $ffmpegBinary.DirectoryName
    Write-Host "FFmpeg found at: $binPath"
    
    # Add to persistent User PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$binPath*") {
        Write-Host "3. Adding to System PATH..."
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$binPath", "User")
        Write-Host "Success! FFmpeg has been added to your PATH."
    } else {
        Write-Host "FFmpeg is already in your PATH."
    }
    
    Write-Host "-----------------------------------------------------"
    Write-Host "IMPORTANT: You must RESTART your terminal or the App"
    Write-Host "for the changes to take effect."
    Write-Host "-----------------------------------------------------"
} else {
    Write-Error "Could not find ffmpeg.exe after extraction."
}
