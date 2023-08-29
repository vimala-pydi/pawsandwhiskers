#!/bin/bash


echo "compile"
#Run this from the target folder of the project
#yum install java-devel
#Compile
javac -classpath "../tomcat/lib/servlet-api.jar:../lib/*" -d "./classes" "../src/main/java/servlets/ImageDisplayServlet.java"
echo "compile complete"

echo "create war file"
mkdir -p ./pawsandwhiskers
cp -rf ./classes/ ./pawsandwhiskers/WEB-INF/
cp -rf ../lib ./pawsandwhiskers/WEB-INF/
cd pawsandwhiskers
jar cvf pawsandwhiskers.war *

#deploy to tomcat
rm -Rf /var/lib/tomcat/webapps/pawsandwhiskers
rm -Rf /var/lib/tomcat/webapps/pawsandwhiskers.war
cp pawsandwhiskers.war /var/lib/tomcat/webapps/

