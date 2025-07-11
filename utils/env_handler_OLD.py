import os
#from trio import current_effective_deadline
import logging

def update_env_entry(env_fPath, key, new_keyvalue):
    #If .env file does not exist 
    if not os.path.exists(env_fPath):
        with open(env_fPath, "w") as f:
            f.write(f"{key}={new_keyvalue}\n")
        logging.info(f"ENV_HANLDER: Added {key} New File was Created.")
        return
    
    #If File does exist
    value_updated = False
    lines = []

    #open file with read permission
    with open(env_fPath, "r") as rEnv_file:
        #search key in file
        for line in rEnv_file:
            if line.startswith(f"{key}="):
                #read current keyvalue and test if the new one is the same
                current_value = line.strip().split("=", 1)[1]
                
                # if current is the same
                if current_value == new_keyvalue:
                    logging.info(f"ENV_HANLDER: {key} already correct in env file. No changes made.")
                    return #end func
                
                #if current is not the same
                else:
                    logging.info(f"ENV_HANLDER: {key} updated from {current_value} to {new_keyvalue}.")
                    line = f"{key}={new_keyvalue}\n" #create the update
                    value_updated = True
            lines.append(line)

    #if file exist but not the key
    if not value_updated and not any(line.startswith(f"{key}=") for line in lines):
        lines.append(f"{key}={new_keyvalue}\n")
        logging.info(f"Added {key} with value: {new_keyvalue}")
    
    #actually write
    with open(env_fPath, "w") as wEnv_file:
        wEnv_file.writelines(lines)
    

