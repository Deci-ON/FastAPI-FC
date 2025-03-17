sudo su
mkdir -p /etc/apt/keyrings
curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/keyrings/microsoft.asc
chmod 644 /etc/apt/keyrings/microsoft.asc
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/microsoft.asc] https://packages.microsoft.com/ubuntu/24.04/prod noble main" | tee /etc/apt/sources.list.d/microsoft.list
exit
