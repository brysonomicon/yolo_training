param(
  [Parameter(Mandatory=$true)]
  [string]$ModelPath,

  [Parameter(Mandatory=$true)]
  [string]$SourceFilePath
)

./.venv/Scripts/Activate.ps1;    # make sure that the virtual environment is active

Get-Content $SourceFilePath | Foreach-Object {
  yolo detect predict `
    model=$ModelPath `
    source=$_; 
  }

