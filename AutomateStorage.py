#!/usr/bin/python2

import commands
import cgi

#for handling html 
print "Content-Type: text/html"
print

nod=cgi.FormContent()['m1'][0]
size=cgi.FormContent()['m2'][0]
nod1=int(nod)
size=int(size)
p=size/nod1
ch=1
if ch==1:
 k=commands.getstatusoutput("sudo docker run -dit --name mastermain newjpg:v2")
 if k[0]==0:
	 print "<h1>your master node hasbeen created</h1>"
 else:
	 print "<h1>your master has not been created</h1>" 
	 print k[1]
 commands.getstatusoutput("sudo chown apache  /mycode/scripts")
 k=commands.getstatusoutput("sudo docker inspect mastermain | jq '.[].NetworkSettings.Networks.bridge.IPAddress'")
 if k[0]==0:
	 print "<e>your ip address</e>"
	 master= k[1].strip('"')
	 print "<h1>"+master+"</h1>"
 else:
	 print "<b>i think have any problem</b>"
	 print k[1]
 k="<?xml version='1.0'?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>/mastermy</value>\n</property>\n</configuration>"
 f=open("masterhdfsfile.txt",'w')
 f.write(k)
 f.close()
 k1="<?xml version='1.0'?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{0}:10001</value>\n</property>\n</configuration>".format(master)
 f=open("mastercorefile.txt",'w')
 f.write(k1)
 f.close()
 yml="""
---
 - hosts: web   
   tasks: 
      
      - command: "docker cp   /mycode/scripts/masterhdfsfile.txt mastermain:/etc/hadoop/hdfs-site.xml"  
      - command: "docker cp   /mycode/scripts/mastercorefile.txt mastermain:/etc/hadoop/core-site.xml"
      - command: "docker exec mastermain hadoop namenode  -format "
      - command: "docker exec mastermain hadoop-daemon.sh start namenode"
      
"""
 f=open("masterkk.yml",'w')
 f.write(yml)
 f.close()

 f=commands.getstatusoutput("sudo ansible-playbook /mycode/scripts/masterkk.yml")
 print f
 if f[0]==0:
	 print "<h1>your namenode configure succesfully</h1>"
 else:
	 print "<h1>have any problem</h1>"
#datanode
 m=list()
 i=1

 while i<=nod1:
   k="<?xml version='1.0'?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>dfs.data.dir</name>\n<value>/kapil</value>\n</property>\n</configuration>"
   f=open("datahdfsfile{0}.txt".format(i),'w')
   f.write(k)
   f.close()
   k1="<?xml version='1.0'?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{0}:10001</value>\n</property>\n</configuration>".format(master)
   f=open("datacorefile{0}.txt".format(i),'w')
   f.write(k1)
   f.close()
   yml="""
---
- hosts: web
  tasks:
   - lvol:
      vg: "shivg"
      lv: "lvmain{0}" 
      size: {1}
   - file:
       path: "/slavemain{0}"
       state: directory
   - filesystem:
       fstype: ext4
       dev: '/dev/shivg/lvmain{0}'
   - mount:
       path: "/slavemain{0}"
       src: "/dev/shivg/lvmain{0}"
       fstype: ext4
       state: mounted
   - command: "docker run -dit  --name=slavemy{0}  -v  /slavemain{0}:/kapil newjpg:v2"
   - command: "docker cp /mycode/scripts/datahdfsfile{0}.txt slavemy{0}:/etc/hadoop/hdfs-site.xml"  
   - command: "docker cp /mycode/scripts/datacorefile{0}.txt slavemy{0}:/etc/hadoop/core-site.xml"
   - command: "docker exec slavemy{0} hadoop-daemon.sh start datanode"
""".format(i,p)
   f=open("kk.yml",'w')
   f.write(yml)
   f.close()
   f=commands.getstatusoutput("sudo ansible-playbook /mycode/scripts/kk.yml")
   print f
   commands.getoutput("rm -f datahdfsfile{0}".format(i)) 
   commands.getoutput("rm -f datacorefile{0}".format(i))
   m.append("slavemy{0}".format(i))
     
   i=i+1
#jobtracker
 k=commands.getstatusoutput("sudo docker run -dit --name jobmain3 newjpg:v2")
 if k[0]==0:
	print "<h1 color='gray'>your jobtracker is created</h1>"
 else:
	print "<h1 bgcolor='gray'>your jobtracker is not created</h1>"

	print k[1]

 k=commands.getstatusoutput("sudo docker inspect jobmain3 | jq '.[].NetworkSettings.Networks.bridge.IPAddress'")
 if k[0]==0:
	print "<span><font face='italic' size='30px' color='gray'>your IP Address of jobtracker is...</font></span>"
	jobtrack= k[1].strip('"')
	print "<h1>"+jobtrack+"</h1>"
 else:
	print "<span><font face='' size='' color=''>your IP Address of jobtracker is not found.</font></span>"
	print k[1]


 
 commands.getstatusoutput("sudo systemctl start docker")
 corejob="<?xml version='1.0'?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{0}:10001</value>\n</property>\n</configuration>".format(master)
 f=open("corejobtracker.txt",'w')
 f.write(corejob)
 f.close()
 mapjob="<?xml version='1.0'?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>hdfs://{0}:9001</value>\n</property>\n</configuration>".format(jobtrack)
 f=open("jobminitracker.txt",'w')
 f.write(mapjob)
 f.close()

 c=commands.getstatusoutput("sudo docker cp corejobtracker.txt jobmain3:/etc/hadoop/core-site.xml")
 if c[0] == 0:
	print "<h1>file transfer successfully</h1>"
 else:
	print "<h1>file is not transfer successfully</h1>"
 c=commands.getstatusoutput("sudo docker cp jobminitracker.txt jobmain3:/etc/hadoop/mapred-site.xml")
 if c[0]== 0:
	print "<h1>file transfer successfully</h1>"
 else:
	print "<h1>file is not transfer successfully</h1>"
 c=commands.getstatusoutput("sudo docker exec jobmain3  hadoop-daemon.sh start jobtracker")
 if c[0] == 0:
	print "<h1>job tracker start successfully</h1>"
 else:
	print "<h1>jobtracker is not start successfully</h1>"



 
