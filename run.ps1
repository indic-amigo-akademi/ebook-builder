Param(
    [bool]$setup = $false,
    [bool]$exec_epub = $true,
    [bool]$exec_html = $true
)

if ($setup) {
    pip install --upgrade pip
    pip install -r requirements.txt
}

if ($exec_epub) {
    python scripts/create_epub.py
}

if ($exec_html) {
    python scripts/create_html.py --dev
}