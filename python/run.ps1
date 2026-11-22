#requires -Version 5
# Runs the spec against the exercises. Pass -Fixed for the reference solutions.
param([switch]$Fixed, [switch]$Quiet)
$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "No python on PATH. Install Python 3.9+ first, e.g.:" -ForegroundColor Yellow
    Write-Host "  winget install Python.Python.3.12"
    exit 2
}

$args = @()
if ($Fixed) { $args += '--fixed' }
if ($Quiet) { $args += '-q' }

python verify.py @args
exit $LASTEXITCODE
