$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "C:\Users\YX\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
$psi.Arguments = "F:\Projects\JavaInterview\inspect_full.py"
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $false
$psi.RedirectStandardError = $false
$p = [System.Diagnostics.Process]::Start($psi)
$p.WaitForExit()
