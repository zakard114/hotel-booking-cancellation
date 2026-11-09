. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
$env:PYTHONUNBUFFERED = "1"
$env:JUPYTER_RUNTIME_DIR = "E:\IT_SPACES\AI\.cache\jupyter\runtime"
$env:JUPYTER_DATA_DIR = "E:\IT_SPACES\AI\.cache\jupyter"
New-Item -ItemType Directory -Force -Path $env:JUPYTER_RUNTIME_DIR, $env:JUPYTER_DATA_DIR | Out-Null
Set-Location "E:\IT_SPACES\AI\Projects\ml\hotel-booking-cancellation"
# notebook-dir = 프로젝트 루트. 브라우저에서는 /tree 또는 /notebooks/notebooks/notebook.ipynb
& "E:\IT_SPACES\AI\ZoomCamp\ML\.venv\Scripts\python.exe" -u -m nbclassic --ip=127.0.0.1 --port=8888 --notebook-dir=.
