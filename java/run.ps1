#requires -Version 5
# Compiles the exercises and runs the spec. Needs JDK 21+ on PATH.
$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

if (-not (Get-Command javac -ErrorAction SilentlyContinue)) {
    Write-Host "No javac on PATH. Install a JDK 21+ first, e.g.:" -ForegroundColor Yellow
    Write-Host "  winget install Microsoft.OpenJDK.21"
    exit 2
}

$sources = Get-ChildItem -Recurse src -Filter *.java | ForEach-Object FullName
javac -d out $sources
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

java -cp out com.example.interview.Verify
exit $LASTEXITCODE
