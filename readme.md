##Gateway monitor and email alert service for PFSense

Here is a basic tool I have written in Python that runs as a service on PFSense (FreeBSD). This is pretty simple to follow and has probably been poorly written and has gone against best practices, but it works for my needs and if you can do something with it then be my guest.

Simply it uses a built in php tool in PFSense that provides metrics on all configured gateways. (Ping, Loss, Status, etc). This is parsed and email alerts are sent if the gateway goes 'down' and the reason, i.e. highloss/highdelay/force_down.

Obviously to sent the email the firewall needs to be configured to fall back to another gateway in the event the monitored gateway is marked as down. This is acheived through the use of setting gateway groups as the default gateway in System > Routing > Gateways in PFSense.

Basic setup is as follows:

With a text editor change the following in gatewaymonitor.py: 

GATEWAY = "LTEGW" to the name of the gateway in PFSense that you want to monitor. Maybe in the future I will change this to be a list of gateways and a simple for loop would monitor more than one. But for now it only does one.

port = 587  # For starttls (Change to whatever you need for your email provider)
smtp_server = "smtp.office365.com" #Change to gmail or other smtp server of your choice
login_email = "xxx@email.com" #Login email for mailbox
sender_email = "xxy@email.com" #Sender email this is usually as above but can be another delegated mailbox
receiver_email = "xxz@email.com" #Wherever you want the offline alerts to go to.
password = "password" #Mailbox password as a plain text string. This is not the most secure method, I know, but if you have someone logged into your firewall and reading through this script then you have bigger issues than this.

Save and exit. 

In PFSense use Diagnostics > Command Prompt > Upload File to upload the two files in pfsense folder to the /root directory. The gain shell access to pfsense and in the terminal run the following:

mv /root/gatewaymonitor.sh /usr/local/etc/rc.d/gatewaymonitor.sh

chmod +x /usr/local/etc/rc.d/gatewaymonitor.sh

chmod +x /root/gatewaymonitor.py

touch /etc/rc.conf.local && echo "gwmonitor_enable=\"YES\"" >> /etc/rc.conf.local

Then reboot. In Diagnostics > Command Prompt you can issue the command ps -aux | grep python and you should see a process being run as "/usr/local/bin/python3.8 /root/gatewaymonitor.py"

Test the email alert by forcing your monitored gateway down.
