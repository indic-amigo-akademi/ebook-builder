Param(
    [bool]$setup = $false
)

if ($setup) {
    pip install --upgrade pip
    pip install -r requirements.txt
}

python scripts/create_epub.py