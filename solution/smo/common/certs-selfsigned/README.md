# Create RSA Private Key and CSR (Certificate Signing Request) 

   openssl req -new -newkey rsa:4096 -nodes -keyout smo.o-ran-sc.org.key -out smo.o-ran-sc.org.csr -subj "/CN=smo.o-ran-sc.org"

# Create a config file containing the SANs

   smo.o-ran-sc.org.ext - Hand coded file containing the SANs and related information to be used in later stages

# Generate the Certificate using the key, csr and config file 

   openssl x509 -req -in smo.o-ran-sc.org.csr -signkey smo.o-ran-sc.org.key -out smo.o-ran-sc.org.crt -days 365 -extfile smo.o-ran-sc.org.ext

# Verify the Certificate

   openssl x509 -in smo.o-ran-sc.org.crt -noout -text

# Install/Trust the Certificate (if you dont want to see the warning in the browser or when running curl)

   sudo cp smo.o-ran-sc.org.crt /usr/local/share/ca-certificates/
   sudo update-ca-certificates

# Java applications require certificates in .jks format

   ## Step 1 - Convert to .p12 format 
	openssl pkcs12 -export -in smo.o-ran-sc.org.crt -inkey smo.o-ran-sc.org.key -out smo.o-ran-sc.org.p12 -name traefikp12 -passout pass:changeit

   ## Step 2 - Convert .p12 to .jks - 
	keytool -importkeystore -srckeystore smo.o-ran-sc.org.p12 -srcstoretype PKCS12 -destkeystore smo.o-ran-sc.org.jks -deststoretype JKS -deststorepass changeit -srcstorepass changeit -alias traefikp12


   
