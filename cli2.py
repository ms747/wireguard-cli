import json
import subprocess

class Client:
    # Client variables
    name        = None
    private_key = None
    public_key  = None
    cidr        = None

    # Client Constructor
    def __init__(self, name, private_key, public_key, cidr):
        self.name        = name
        self.private_key = private_key
        self.public_key  = public_key
        self.cidr        = cidr

class Server:
    # Server variables
    clients     = []
    cidr        = None
    port        = None
    name        = None
    private_key = None
    public_key  = None
    path        = None
    public_ip   = None

    # Create private/public key pairs
    def create_keys(self):
        private_key = subprocess.run(["wg", "genkey"], encoding="utf-8", stdout=subprocess.PIPE).stdout.strip()
        public_key  = subprocess.run(["wg", "pubkey"], encoding="utf-8", stdout=subprocess.PIPE, input=private_key).stdout.strip()
        return (private_key, public_key)

    # Create keys for server and set the interface
    def generate_server_config(self, path, interface):
        self.name = interface
        self.private_key, self.public_key = self.create_keys()

    # Add Client/Peer to the Server
    def add_client(self, name, cidr):
        private, public = self.create_keys()
        self.clients.append(Client(name, private, public, cidr).__dict__)

    # Save the config
    def save_config(self):
        server = { "name":        self.name,
                   "public_ip":   self.public_ip,
                   "private_key": self.private_key,
                   "public_key":  self.public_key,
                   "cidr":        self.cidr,
                   "port":        self.port,
                   "clients":     self.clients }
        with open(self.path, "w") as config:
          json.dump(server, config, indent=4)

    # Server constructor
    def __init__(self, public_ip, cidr, port, interface, path):
        self.path = path
        self.cidr = cidr
        self.port = port
        self.public_ip = public_ip
        self.generate_server_config(self.path, interface)

def main():
    print("WG CLI 0.1")
    public_ip = input("Enter Public IP : ")
    interface = input("Enter interface name : ")
    cidr      = input("Enter interface cidr (e.g ip/netmask) : ")
    port      = input("Enter port : ")

    server = Server(public_ip, cidr, port, interface, f"{interface}-config.json")

    while True:
        client_name = input("Enter client name : ")
        client_cidr = input("Enter client cidr : ")
        server.add_client(client_name, client_cidr)
        new_client  = input("Press q to quit : ")

        if new_client == "q":
            break

    print("Generating...")

    server.save_config()

if __name__ == "__main__":
    main()
