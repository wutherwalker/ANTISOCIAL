cd C:\Users\patri_000\oTree
otree collectstatic --noinput
@echo off
set ip_address_string="IPv4 Address"
for /f "usebackq tokens=2 delims=:" %%f in (`ipconfig ^| findstr /c:%ip_address_string%`) do (
    echo Your IP Address is: %%f
	start cmd @cmd /k "otree devserver %%f:8000"
	timeout 10
	start firefox http://%%f:8000
	goto eof
)

pause

exit