$ErrorActionPreference = 'Continue'
$root = 'D:\Tools\ai-tool-index'
$today = Get-Date -Format 'yyyy-MM-dd'
$stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
function Get-Code($url) {
  $tmp = Join-Path $env:TEMP ('curl_' + [guid]::NewGuid().ToString())
  try { $code = & curl.exe -L --max-time 15 -s --output $tmp --write-out '%{http_code}' $url } catch { $code = 'ERR' }
  Remove-Item $tmp -ErrorAction SilentlyContinue
  return ($code | Select-Object -Last 1)
}
function Post-Json-Code($url, $file) {
  $tmp = Join-Path $env:TEMP ('curl_' + [guid]::NewGuid().ToString())
  try { $code = & curl.exe -L --max-time 30 -s --output $tmp --write-out '%{http_code}' -X POST $url -H 'Content-Type: application/json' --data-binary "@$file" } catch { $code = 'ERR' }
  Remove-Item $tmp -ErrorAction SilentlyContinue
  return ($code | Select-Object -Last 1)
}
$sites = @(
  @{domain='iworkviewer.com'; key='6d9c5b4e2a1f4c7b9e8d3a2f1c6b5e4d'; localSitemap='D:\Tools\iworkopener\out\sitemap.xml'},
  @{domain='livephotokit.com'; key='0f3e7a9c4b2d16850fa9c7e3b1d64a28'; localSitemap='D:\Tools\livephotokit\out\sitemap.xml'},
  @{domain='plantingcalendar.net'; key='gavin-ai-export-20260710-0c8847231c234f0d'; localSitemap='D:\Tools\plantingcalendar\out\sitemap.xml'},
  @{domain='freetdee.com'; key='gavin-ai-export-20260710-0c8847231c234f0d'; localSitemap='D:\Tools\freetdee\out\sitemap.xml'},
  @{domain='babypercent.com'; key='gavin-ai-export-20260710-0c8847231c234f0d'; localSitemap='D:\Tools\babypercent\out\sitemap.xml'},
  @{domain='invoicepad.net'; key='gavin-ai-export-20260710-0c8847231c234f0d'; localSitemap='D:\Tools\invoicepad\out\sitemap.xml'},
  @{domain='zoneplan.net'; key='gavin-ai-export-20260710-0c8847231c234f0d'; localSitemap='D:\Tools\zoneplan\out\sitemap.xml'},
  @{domain='pupvax.com'; key='gavin-ai-export-20260710-0c8847231c234f0d'; localSitemap='D:\Tools\pupvax\out\sitemap.xml'}
)
New-Item -ItemType Directory -Force -Path "$root\daily", "$root\logs" | Out-Null
$results = @()
foreach($s in $sites){
  $d=$s.domain
  $homeCode = Get-Code "https://$d/"
  $robots = Get-Code "https://$d/robots.txt"
  $sitemapStatus = Get-Code "https://$d/sitemap.xml"
  $urls = @()
  try {
    $xml = (& curl.exe -L --max-time 20 -s "https://$d/sitemap.xml") -join "`n"
    if($xml -match '<loc>') { $urls = [regex]::Matches($xml,'<loc>(.*?)</loc>') | ForEach-Object { $_.Groups[1].Value } | Select-Object -First 20 }
  } catch {}
  if($urls.Count -eq 0 -and (Test-Path $s.localSitemap)){
    $xml = Get-Content $s.localSitemap -Raw
    $urls = [regex]::Matches($xml,'<loc>(.*?)</loc>') | ForEach-Object { $_.Groups[1].Value } | Select-Object -First 20
  }
  if($urls.Count -eq 0){ $urls = @("https://$d/") }
  $payload = @{ host=$d; key=$s.key; keyLocation="https://$d/$($s.key).txt"; urlList=$urls } | ConvertTo-Json -Depth 5
  $payloadFile = "$root\logs\$today-$d-indexnow.json"
  $payload | Set-Content -Encoding UTF8 $payloadFile
  $indexStatus = Post-Json-Code 'https://www.bing.com/indexnow' $payloadFile
  $results += [pscustomobject]@{domain=$d; home=$homeCode; robots=$robots; sitemap=$sitemapStatus; urls=$urls.Count; indexnow=$indexStatus}
}
$dailyFile = "$root\daily\$today-ai-tool-indexing-maintenance.md"
$lines = @()
$lines += "# $today AI Tool Indexing Maintenance"
$lines += ""
$lines += "Run time: $stamp"
$lines += ""
$lines += "## Live checks and IndexNow"
$lines += ""
$lines += "| Site | Home | Robots | Sitemap | URLs submitted | IndexNow |"
$lines += "|---|---:|---:|---:|---:|---:|"
foreach($r in $results){ $lines += "| [$($r.domain)](https://$($r.domain)/) | $($r.home) | $($r.robots) | $($r.sitemap) | $($r.urls) | $($r.indexnow) |" }
$lines += ""
$lines += "## Public links"
$lines += ""
foreach($s in $sites){ $lines += "- [$($s.domain)](https://$($s.domain)/)" }
$lines += ""
$lines += "This daily note creates a public crawl path and records the indexing maintenance work for the eight tool sites."
$lines -join "`n" | Set-Content -Encoding UTF8 $dailyFile
$results | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 "$root\logs\$today-result.json"
Push-Location $root
git add daily logs run-ai8-daily-maintenance.ps1 2>$null
git commit -m "Daily indexing maintenance $today" 2>$null
git push origin HEAD 2>$null
$gitExit=$LASTEXITCODE
Pop-Location
"DONE $stamp gitExit=$gitExit dailyFile=$dailyFile"

