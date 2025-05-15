import json
import os
import re


############+++++++++++++++++++Update daemon.json with hardening flags+++++++++++++++++++++++++++++++++++++++++

def update_daemon(flag='no-new-privileges: True', path='/etc/docker/daemon.json'):
    try:
        if os.path.exists(path):
            with open(path, 'r') as file:
                daemon = json.load(file)
        else:
            daemon = {}

        daemon.update(flag)

        #write update back to file
        with open(path, 'w') as file:
            json.dump(daemon, file)

        print("File updated successfully.")
    except Exception as e:
        print(f"Something went wrong: {e}")


############+++++++++++++++++++Inject USER, HEALTHCHECK, and limits into Dockerfile +++++++++++++++++++++++++++++++++++++++++

def patch_dockerfile(path='Dockerfile',healthcheck_replace="HEALTHCHECK --interval=30s --timeout=30s --retries=3 CMD curl -f http://localhost:5000/ || exit 1\n"):
    
    changed=[]

    if not os.path.exists(path):
        print("Dockerfile not found.")
        return False

    with open(path, 'r') as doc:
            for line in doc:
                
                # Update healthcheck if it already exist
                if line.strip().startswith("HEALTHCHECK"):
                    data=line.replace(line,healthcheck_replace)
                    with open(path, 'w') as file:
                         try:
                          file.write(data)
                          print("HEALTHCHECK updated successfully")
                         except Exception as e:
                            print(f"Something went wrong: {e}")

                # Add healthcheck if it dosent exist
                elif line.strip().startswith("CMD"):
                    changed.append(healthcheck_replace) 
                    changed.append(line) 

                    with open(path, 'w') as doc:
                         try:
                          doc.writelines(changed)
                          print("HEALTHCHECK added successfully")
                         except Exception as e:
                            print(f"Something went wrong: {e}")

