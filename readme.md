
get leases data from router

telnet 192.168.1.1
or
ssh root@192.168.1.1

password

root@DD-WRT:~# nvram show | grep static

paste op into telnet-static-leases.txt
remove all text up to first mac address
remove all after final '='
save

run static-leases-to-csv.py

converts to a csv file of host info - 'host-details-table
in order col use =VALUE(RIGHT(C2,IF(LEN(C2)=13,3,2)))

run csv-to-static-leases.py

generates text to enter in router command lin


Worked for me on a WRT1900AC with Kong R30965M and I used the following:

Code:	
nvram set static_leasenum=38
nvram set static_leases="00:00:00:00:00:00:=Comp01=192.168.1.101= \
00:00:00:00:00:00:=Comp02=192.168.1.102= \
00:00:00:00:00:00:=Comp03=192.168.1.103= \
 ...
00:00:00:00:00:00:=Comp26=192.168.1.138="	


Ran "nvram set static_leasenum=38" by itself first then copy/paste (from Notepad++) all of "nvram set static_leases=" until the last double quote. Do not include last CRLF at end.

I used Putty via SSH to login to WRT1900AC. I used Notepad++ to set up command as text.

Key point for me was to have a space after each = , then the \ , and then a "CRLF" at the end of each line (in Notepad++) but do not copy last CRLF from Notepad++.

Then "nvram get static_leases" to check if OK and then check in GUI if OK, it was.

Then "nvram commit" and "reboot"

Thanks to the prior posters for helping me out.