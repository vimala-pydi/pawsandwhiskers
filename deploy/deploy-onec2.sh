#!/bin/bash

#cp -rf src/main/webapps/* target/pawsandwhiskers/
echo "compile"
#Run this from the target folder of the project
#yum install java-devel
#sudo yum install java-1.7.0-openjdk-devel -y
#Compile
javac -classpath "../tomcat/lib/servlet-api.jar:../lib/*" -d "./classes" "../src/main/java/servlets/ImageDisplayServlet.java"
echo "compile complete"

cp -rf src/main/webapps/* target/pawsandwhiskers/
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

