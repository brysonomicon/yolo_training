param(
  [string]$objnames1,
  [string]$dataset1,
  [string]$objnames2,
  [string]$dataset2,
  [string]$outputpath
)

function PopulateNamesTable {
  param(
    [string]$fileLines,
    [hashtable]$namesTable
  )
  $i = 0
  foreach ($line in $fileLines) {
    namesTable[i++] = $line
  }
}

function PopulateMergedNamesTable {
  param(
    [string]$fileLines,
    [hashtable]$mergednamesTable
  )
  $i = 0
  foreach ($line in $fileLines) {
    mergednamesTable[$line] = i++
  }
}

$exists = (( Test-Path $objnames1 ) `
      -and ( Test-Path $dataset1 )  `
      -and ( Test-Path $objnames2 ) `
      -and ( Test-Path $dataset2 )  `
      -and ( Test-Path $outputpath ))

if (-not $exists) { throw "Input path(s) are invalid." }

$objnames1filelines = ( Get-Content $objnames1 )
$objnames2filelines = ( Get-Content $objnames2 )
$mergednames        = @(($objnames1filelines), ($objnames2filelines)); $mergednames > "$outputpath\mergedobj.names"

$classnames1        = @{}
$classnames2        = @{}
$mergedclassnames   = @{}

PopulateNamesTable `
  -fileLines  $objnames1filelines `
  -namesTable $classnames1

PopulateNamesTable `
  -fileLines $objnames2filelines `
  -namesTable $classnames2

PopulateMergedNamesTable `
  -fileLines $mergedfilelines `
  -mergednamesTable $mergedclassnames

"$dataset1,`nData count`t$([int]((Get-ChildItem $dataset1).Count / 2))";
"$dataset2,`nData count`t$([int]((Get-ChildItem $dataset2).Count / 2))";

