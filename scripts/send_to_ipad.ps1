param(
  [Parameter(Mandatory = $true)]
  [string]$ImagePath,
  [string]$ServerUrl = "http://YOUR-PC-IP:8787/upload"
)

if (-not (Test-Path $ImagePath)) {
  Write-Error "File not found: $ImagePath"
  exit 1
}

try {
  $response = Invoke-RestMethod -Uri $ServerUrl -Method Post -Form @{ image = Get-Item $ImagePath }
  Write-Host "Uploaded: $($response.updated_at)"
} catch {
  Write-Error "Upload failed: $($_.Exception.Message)"
  exit 1
}
