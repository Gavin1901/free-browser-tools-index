param(
    [Parameter(Mandatory = $false)]
    [string]$Date = (Get-Date -Format 'yyyy-MM-dd')
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$manifestPath = Join-Path $root "logs\$Date-backlink-manifest.json"
$sweepPath = Join-Path $root "logs\$Date-platform-sweep.json"

function Fail([string]$Message) {
    Write-Output "ai_outbound_closeout=FAIL"
    Write-Output "reason=$Message"
    exit 1
}

if (-not (Test-Path -LiteralPath $manifestPath)) {
    Fail "missing_backlink_manifest:$manifestPath"
}

if (-not (Test-Path -LiteralPath $sweepPath)) {
    Fail "missing_platform_sweep:$sweepPath"
}

$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$sweep = Get-Content -LiteralPath $sweepPath -Raw -Encoding UTF8 | ConvertFrom-Json

if ($manifest.Count -lt 5) {
    Fail "public_backlinks_below_daily_floor:$($manifest.Count)"
}

$duplicateUrls = $manifest |
    Group-Object url |
    Where-Object Count -gt 1

if ($duplicateUrls) {
    Fail "duplicate_urls_in_manifest"
}

$invalidLinks = @(
    $manifest | Where-Object {
        -not $_.url -or
        -not $_.target_domain -or
        -not $_.platform -or
        $_.public_verified -ne $true -or
        $_.target_link_verified -ne $true -or
        (($_.http_status -ne 200) -and ($_.verification_method -ne 'browser'))
    }
)

if ($invalidLinks.Count -gt 0) {
    Fail "unverified_public_links:$($invalidLinks.Count)"
}

$allowedStates = @(
    'published',
    'pending_review',
    'login_blocked',
    'platform_blocked',
    'duplicate_avoided'
)

$badSweep = @(
    $sweep | Where-Object {
        -not $_.platform -or
        $_.status -notin $allowedStates
    }
)

if ($badSweep.Count -gt 0) {
    Fail "platform_sweep_has_nonterminal_rows:$($badSweep.Count)"
}

$unattempted = @(
    $sweep | Where-Object {
        $_.feasible_unattempted -eq $true
    }
)

if ($unattempted.Count -gt 0) {
    Fail "feasible_unattempted:$($unattempted.Count)"
}

$publicCount = $manifest.Count
$referringDomains = @(
    $manifest |
        ForEach-Object { ([uri]$_.url).Host.ToLowerInvariant() } |
        Sort-Object -Unique
).Count

$targetDomains = @(
    $manifest |
        ForEach-Object { $_.target_domain.ToLowerInvariant() } |
        Sort-Object -Unique
).Count

$publishedPlatforms = @(
    $sweep |
        Where-Object status -eq 'published' |
        ForEach-Object platform |
        Sort-Object -Unique
).Count

Write-Output "ai_outbound_closeout=PASS"
Write-Output "date=$Date"
Write-Output "public_backlinks=$publicCount"
Write-Output "referring_domains=$referringDomains"
Write-Output "target_domains=$targetDomains"
Write-Output "published_platforms=$publishedPlatforms"
Write-Output "platform_rows=$($sweep.Count)"
exit 0
