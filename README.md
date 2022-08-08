# picollo
A small photoBooth project. I know there are plenty of others and also this is the right moment to admit, some of them gave inspiration to Picollo. The main reason to create next one was that almost none of other photoBooth sends taken pictures directly to the printer. And also i am too lazy to bend other people code ....

1/ Have a Raspberry - mine is Pi 3, B+

2/ Have an installed Rapsbery :D - you can re-use the one from section 1. Raspbian is just perfect. Currently Buster is the most recommended version. Bullseye has serious troubles with Raspberry official screen (5" + 7"). Bullseye also has troubles with "older" printer. It might have changed to your "now".

3/ Have any display you want. in my case is 5" raspberry LCD. Check manufacturer recomendations.   
  <b>e.g. waveshare -> add to /boot/config.txt</b>  
  <pre>
  hdmi_group=2  
  hdmi_mode=87
  hdmi_cvt 800 480 60 6 0 0 0
  hdmi_drive=1
  dtoverlay=ads7846,cs=1,penirq=25,penirq_pull=2,speed=50000,keep_vref_on=0,swapxy=0,pmax=255,xohms=150,xmin=200,xmax=3900,ymin=200,ymax=3900</pre>

4/ Clone this repo somewhere

5/ Install Fpdf -> <pre>pip3 install fpdf2</pre>
  for more info -> https://pyfpdf.github.io/fpdf2/index.html
  
6/ create a shell script to disable screensaver and run your script
e.g. 
<pre>sudo nano picollo.sh</pre>
<pre>
xset s 0
xset -dpms
cd /home/pi/picollo
python3 ./picollo.py
</pre>
ctrl+x (Y as yes to save)

7/ make shell script executable
<pre>chmod a+x picollo.sh</pre>

8/ add your script into crontab, so it gets running after reboot
<pre>crontab -e</pre>
add a line at the end
<pre>@reboot /home/pi/picollo/picollo.sh</pre>


