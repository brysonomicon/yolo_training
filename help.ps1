# not useful for the python, just me testing somethign
#
$unique = (Get-ChildItem -File `
  | Select-Object @{ Name='BaseName'; Expression={$_.BaseName} } `
  | Group-Object -Property BaseName ` 
  | Where-Object {$_.Count -eq 1} `
  | Select-Object -ExpandProperty Name)

$unique.Count

