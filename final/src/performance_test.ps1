For ($i=1; $i -le 4; $i++) {
    Measure-Command {start-process py.exe -ArgumentList (".\log_parser\main.py", "D:\VMs\share\DE\logs\access.log", "result.json", $i) -Wait} | Out-String | Set-Content  (".\t"+$i+".txt")
}

For ($i=6; $i -le 11; $i+=2) {
    Measure-Command {start-process py.exe -ArgumentList (".\log_parser\main.py", "D:\VMs\share\DE\logs\access.log", "result.json", $i) -Wait} | Out-String | Set-Content  (".\t"+$i+".txt")
}

For ($i=12; $i -le 20; $i+=4) {
    Measure-Command {start-process py.exe -ArgumentList (".\log_parser\main.py", "D:\VMs\share\DE\logs\access.log", "result.json", $i) -Wait} | Out-String | Set-Content  (".\t"+$i+".txt")
}