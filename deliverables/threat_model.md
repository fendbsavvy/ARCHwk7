# Threat Model: Secure Containerized Microservices

## 1. Overview
### Threat modeling performed on the flask insecure application, following STRIDE and MITRE ATT&CK methodologies. The vulnerabilities were identified from the scans performed on the flask app and then used to develop this threat model.

---

## 2. STRIDE Analysis
|Threat Category |Vulnerability |Impact |Mitigation |
|----------------|--------------|-------|-----------|
|Spoofing |Hardcoded password (B105) |Unauthorized access |Used environment variables, created .env file to store passwords.|
|Tampering |Unsafe subprocess execution (B602, B404) |Malicious commands execution |Input validation, used subprocess with shell=False, pass a list of strings to subprocess instead of a string.|
|Repudiation |No logging |Unauthorized changes not logged |Could add logging of app
|Information Disclosure |Hardcoded password (B105) |Unauthorized access to code repositories and restricted files. |Used environment variables, created .env file to store passwords.|
|Denial of Service (DoS) |Unsafe eval() (B307), Bind-all interfaces (B104) |Can use eval(), ping, and opened ports to conduct DoS attacks. |Replaced eval() with ast.literal_eval, restrict access to localhost|
|Elevation of Privilege |Unsafe subprocess execution (B602); Running as root user |Unauthorized system-level access. |Used non root user; Docker hardening|

---

## 3. MITRE ATT&CK for Containers

|Tactic |Technique ID |Technique Name |Relevant Vulnerability|
|-------|-------------|---------------|----------------------|
|Initial Access |T1190 |Exploit Public-Facing Application |B104 Binding to all interfaces ; external access to /ping /calculate|
|Execution| T1609 |Container Administration Command |Ensure not running as root user, fixed B602 Unsafe subprocess execution vulnerability|
|Persistence |T1078 |Valid Accounts |Ensure not running as root user, fixed B404, B602 Unsafe subprocess execution vulnerability|
|Privilege Escalation |T1611 |Escape to Host |Fixed B602 subprocess vulnerability- Unsafe subprocess execution|
|Defense Evasion| T1070 |Indicator Removal |B307 unsafe eval() usage|
|Credential Access |T1552.001 |Unsecured Credentials: Credentials In Files |B105 Hardcoded password|
|Discovery| T1046 |Network Service Discovery |B104 Binding to all interfaces ; external access to /ping /calculate|
|Impact |T1499 |Endpoint Denial of Service |B104 Binding to all interfaces ; external access to /ping /calculate |

---

## 4. Controls Mapping

|Vulnerability |Relevant Security Controls|
|--------------|--------------------------|
|B404 Unsafe subprocess |OWASP ASVS V5, NIST SP 800-53: SI-7|
|B105 Hardcoded password |OWASP Top Ten A07:2021, CIS Docker Benchmark|
|B602 Subprocess with shell=True |OWASP ASVS V5, NIST SP 800-53: AC-6|
|B307 Insecure eval usage |OWASP Top Ten A03:2021|
|B104 Binding to all interfaces |CIS Docker Benchmark, OWASP ASVS A05:2021|

---

## 5. Conclusion

This threat model identifies the major flaws in the system and informs the remediation and architecture redesign. The final implementation significantly reduces the attack surface and enforces least privilege, defense in depth, and secure defaults.
