import os
import sys

HOSTS_FILE = "/etc/hosts"
BLOCK_START = "# BEGIN BLOCKED SITES"
BLOCK_END = "# END BLOCKED SITES"

def block_site(site):
    if not site.startswith("www.") or not site.startswith("http"):
    	site = "www."+site
    # Check if the site is already blocked
    with open(HOSTS_FILE, "r") as f:
        content = f.read()
        if site in content:
            print(f"{site} is already blocked.")
            return

    # Block the site
    block_lines = [f"\n# Bloqueo de sitio web: {site}\n",f"127.0.0.1\t{site}\n"]
    with open(HOSTS_FILE, "a") as f:
        f.write("\n")
        f.writelines(block_lines)

    print(f"{site} has been blocked.")

def unblock_site(site):
    # Unblock the site
    with open(HOSTS_FILE, "r") as f:
        content = f.readlines()
    with open(HOSTS_FILE, "w") as f:
        for line in content:
            if site not in line:
                f.write(line)

    print(f"{site} has been unblocked.")
    
def unblock_all():
    prev_line = " "
    flag = "# Bloqueo de sitio web:"
    with open(HOSTS_FILE, "r") as f:
        content = f.readlines()
    with open(HOSTS_FILE, "w") as f:
        for line in content:   
            if flag not in prev_line:
               f.write(line)
            prev_line = line
            
    with open(HOSTS_FILE, "r") as f:
        content = f.readlines()
    with open(HOSTS_FILE, "w") as f:
        for line in content:   
            if flag not in line:
               f.write(line)
    print(f"All sites have been unblocked.")
    
def get_blocks():
    list_sites = []
    flag = "# Bloqueo de sitio web:"
    prev_line = " "
    with open(HOSTS_FILE, "r") as f:
        content = f.readlines()
        for line in content:
            if flag in prev_line:
                site = line.replace("127.0.0.1\t","")
                list_sites.append(site)
                print("\n"+site)
            prev_line = line
    return list_sites

if __name__ == "__main__":
    blocks=[]
    if len(sys.argv) != 3:
        print("Usage: python block_site.py [block|unblock] [site]")
        sys.exit(1)

    action = sys.argv[1]
    site = sys.argv[2]

    if action == "block":
        block_site(site)
    elif action == "unblock":
        unblock_site(site)
    elif action == "unblock-all":
        unblock_all()
    elif action == "get-all":
        blocks = get_blocks()
    else:
        print("Invalid action. Use 'block' or 'unblock'.")
        sys.exit(1)
