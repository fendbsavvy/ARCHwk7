# Steps Taken

Five files were created: app.py, docker-compose.yml, Dockerfile, Makefile,  and requirements.txt, using code provided in week-7 folder in GitHub repository. Once the files were created, the commands ‘make build’ and ‘make start’ were run to build the docker image and start all services defined in docker-compose.yml. 

Once build was successful, http://<IP>:15000/ was entered into the browser address bar, which printed the message ‘Hello World’, indicating the app was accessible from the browser. To facilitate access, an Inbound rule was added to allow traffic to port 15000 form any address.

Several other requests were made from the browser to test the /ping and /calculate routes: “http://<IP>:15000/ping?ip=8.8.8.8 and http://<IP>:15000/calculate?expr=2%2B3, response indicates both routes were accessible from the browser. 

Ran ‘make check’, ‘make scan’ and make ‘host-security’. Identified vulnerabilities and misconfigurations were recorded and stored in files for future reference. 
Several vulnerabilities were noted, including Hardcoded password, Unsafe subprocess execution, subprocess open with shell=true, Unsafe use of eval(), and binding to all interfaces. 

## Code Remediation
Several steps were taken to remediate the vulnerabilities found, these included:
1.	Installed dotenv, and added import statement to app.py and load_dotenv using code:
from dotenv import load_dotenv
load_dotenv()

2.	Created .env file to store passwords and secrets.

3.	Edited app.py to remove hardcoded password by retrieving the value of the password from the .env file, using code:
PASSWORD=os.getenv('PASSWORD')

4.	Edited app.py to replace the unsafe function eval() with ast.literal_eval, using code: 
 result = ast.literal_eval(expression)

5.	Edited app.py to add input validation in both /ping and /calculate routes, for example this ensures the user can only enter an IP address: 
if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", ip):
    	return jsonify({"error": "Invalid IP address"}), 400

6.	Edited docker-compose to restrict app to localhost, using:
ports:
      - "127.0.0.1:15000:5000"



## Docker Hardening
Several steps were taken to harden the docker container, including: 
1.	Checked app uses a minimal base image, app was using python:3.9-alpine
2.	Checked app runs as a non-root user. The app had Group appgroup and user set to appuser
3.	Added a HEALTHCHECK directive by adding HEALTHCHECK --interval=30s --timeout=30s --retries=3 CMD curl -f http://localhost:5000/ || exit 1, to Dockerfile.

Once the app was hardened, requests were made from the browser to retest the /ping and /calculate routes: “http://127.0.0.1:15000/ping?ip=8.8.8.8” and “http://<IP>:15000/calculate?expr=2%2B3”, response indicated both routes were no longer accessible from the browser.
The command curl “http://<IP>:15000/ping?ip=8.8.8.8” was made from the terminal, response indicated the app was accessible from localhost. 

## Rescanning 
 Ran ‘make check’, ‘make scan’ and make ‘host-security’ and noted less vulnerabilities, one vulnerability that was rated ‘medium’ was downgraded to ‘low’.

# Vulnerabilities found and fixed
The following vulnerabilities were found and fixed: 
1.	Low -- [B105:hardcoded_password_string] Possible hardcoded password: 'supersecretpassword' --# Hard-coded password. This was fixed by using a .env file and adding the password to the file. The app could then access the password from the file.
2.	High -- [B602:subprocess_popen_with_shell_equals_true] subprocess call with shell=True identified, security issue. --  # Unsafe command execution. This was fixed by passing a list to the process instead of a string and setting shell=false.
3.	Medium -- [B307:blacklist] Use of possibly insecure function - consider using safer ast.literal_eval. -- # Dangerous use of eval. This was fixed by using ast.literal_eval instead. 
4.	Medium -- [B104:hardcoded_bind_all_interfaces] Possible binding to all interfaces. This was fixed by limiting the app to localhost. 

# Improved security.
The steps that were taken improved security by prevent certain attacks. Hardcoded passwords can be leaked if the code is shared or mistakenly uploaded to a public repository. Removing the hardcoded password prevents this exposure and reduce the likelihood of unauthorized access. Setting shell=False in subprocess commands helps to mitigate command injection vulnerabilities, while Using ast.literal_eval() instead of eval() prevents malicious code execution. Input validation will ensure user input is sanitized and prevents attacks such as SQL injection, cross-site scripting (XSS), and other input-based attacks. Finally Limiting the application to localhost restricts external access, reducing the attack surface and provide protection from external threats. 

# Reflections
This application made it clear how critical it is to implement robust security in modern applications in the cloud and when using containerization. When building applications, security must be a main focus from initial setup through the development process. Steps should be taken to limit external exposure and prevent attacks.


# References
MITRE. (2025). Drive-by Compromise (T1189). MITRE ATT&CK. Retrieved May 5, 2025, from https://attack.mitre.org/techniques/T1189/
OWASP Foundation. (n.d.). Threat modeling process. OWASP. Retrieved May 12, 2025, from https://owasp.org/www-community/Threat_Modeling_Process



