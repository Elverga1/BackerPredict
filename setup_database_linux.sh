#!/bin/bash
sudo systemctl start mariadb
sudo systemctl enable mariadb
sudo mysql < Database/schema.sql
sudo mysql < Database/seed.sql
sudo mysql < Database/indexes.sql

sudo mysql <<EOF
CREATE USER IF NOT EXISTS 'bakeruser'@'localhost' IDENTIFIED BY 'Baker123!';
GRANT ALL PRIVILEGES ON bakerpredict.* TO 'bakeruser'@'localhost';
FLUSH PRIVILEGES;
EOF

cat > Backend/.env <<EOF
DB_HOST=localhost
DB_USER=bakeruser
DB_PASSWORD=Baker123!
DB_NAME=bakerpredict
EOF
