#!/bin/bash

# Set paths relative to the script's location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
TOMCAT_PATH="$SCRIPT_DIR/../tomcat"
PROJECT_ROOT="$SCRIPT_DIR/.."
echo "Project root is" $PROJECT_ROOT
# Compile
echo "Compilation started!"
javac -classpath "$TOMCAT_PATH/lib/servlet-api.jar:$PROJECT_ROOT/lib/*" -d "$PROJECT_ROOT/target/classes" "$PROJECT_ROOT/src/main/java/servlets/ImageDisplayServlet.java"
echo "Compilation complete!"

# Create WAR file
echo "Creating WAR file..."
mkdir -p "$PROJECT_ROOT/target/pawsandwhiskers/WEB-INF/classes"
mkdir -p "$PROJECT_ROOT/target/pawsandwhiskers/WEB-INF/lib"
cp -r "$PROJECT_ROOT/src/main/webapps/" "$PROJECT_ROOT/target/pawsandwhiskers/"
cp -r "$PROJECT_ROOT/src/main/java/servlets/" "$PROJECT_ROOT/target/pawsandwhiskers/WEB-INF/classes/"
cp "$PROJECT_ROOT/lib/"* "$PROJECT_ROOT/target/pawsandwhiskers/WEB-INF/lib/"
cd "$PROJECT_ROOT/target/pawsandwhiskers/"
jar cvf "$PROJECT_ROOT/target/pawsandwhiskers.war" *

# Deploy to Tomcat
cp "$PROJECT_ROOT/target/pawsandwhiskers.war" "$TOMCAT_PATH/webapps/"

# Start Tomcat
"$TOMCAT_PATH/bin/startup.sh"

echo "Web application deployed and Tomcat started. Access it at: http://localhost:8080/pawsandwhiskers/"

# Wait for user input to stop Tomcat
read -p "Press Enter to stop Tomcat..."
"$TOMCAT_PATH/bin/shutdown.sh"

echo "Tomcat stopped."
