$body = @'
{
    "query": "Nhà 3 tầng Cầu Giấy dưới 5 tỷ",
    "search_realtime": true,
    "max_results": 5
}
'@

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/search" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -TimeoutSec 120

    $result = $response.Content | ConvertFrom-Json
    
    Write-Host "`n=== SEARCH RESULTS ===" -ForegroundColor Green
    Write-Host "Total: $($result.total)" -ForegroundColor Cyan
    Write-Host "From Cache: $($result.from_cache)" -ForegroundColor Cyan
    Write-Host "Execution Time: $($result.execution_time_ms)ms" -ForegroundColor Cyan
    Write-Host "Sources: $($result.sources -join ', ')" -ForegroundColor Cyan
    
    if ($result.results) {
        Write-Host "`nResults Count: $($result.results.Count)" -ForegroundColor Yellow
        $result.results | Select-Object -First 3 | ForEach-Object {
            Write-Host "`n- $($_.title)" -ForegroundColor White
            Write-Host "  Platform: $($_.source_platform)" -ForegroundColor Gray
            Write-Host "  URL: $($_.source_url)" -ForegroundColor Gray
        }
    }
    
    if ($result.errors) {
        Write-Host "`nErrors:" -ForegroundColor Red
        $result.errors | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    }
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
