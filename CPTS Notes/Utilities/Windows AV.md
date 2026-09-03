
# Disable AV

We will want to disable the antivirus through the `Virus & threat protection settings` or by using this command in an administrative PowerShell console (right-click, run as admin)

```powershell
Set-MpPreference -DisableRealtimeMonitoring $true
```