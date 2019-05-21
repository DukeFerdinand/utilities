import argparse

parser = argparse.ArgumentParser(
    description="Adds an entry to /etc/hosts. NOTE: sudo is required unless you setup permissions (e.g. polkit) for this script")
required_args = parser.add_argument_group("required arguments")
required_args.add_argument('--hostname', type=str, required=True,
                           help="Hostname to associate with an ip. For example: 'vagrant.box' or 'devmachine'")
parser.add_argument('--ip', type=str, required=False,
                    default='127.0.0.1', help="IP to associate with hostname. Defaults to 127.0.0.1")
parser.add_argument('--file', type=str, required=False,
                    default="/etc/hosts", help="Override file to use for comparision/writing. Default is /etc/hosts")
parser.add_argument('-r', action="store_true", dest="do_removal",
                    help="Remove entry from /etc/hosts")

args = parser.parse_args()


# If we don't specify to remove, assume write
if not args.do_removal:
    class NewHost:
        def __init__(self, hostname, ip):
            self.hostname = hostname
            self.ip = ip

        def host_string(self):
            # Tab character to respect /etc/hosts spacing
            return f"{self.ip}\t{self.hostname}"

    new_host = NewHost(args.hostname, args.ip)

    with open(args.file, 'r+') as host_file:
        line = host_file.readline()
        count = 1
        while line:
            line = line.strip()
            if new_host.hostname in line:
                raise Exception(
                    f"Hostname '{new_host.hostname}' already in use, please select a different name or modify the entry on line {count}")

            line = host_file.readline()
            count += 1
        host_file.write(new_host.host_string())
        host_file.close()
    print("Successfully updated /etc/hosts")
else:
    print(f"Removing entry '{args.hostname}' from {args.file}")
    with open(args.file, 'r+') as host_file:
        lines = host_file.readlines()
        host_file.seek(0)
        for line in lines:
            if args.hostname not in line:
                host_file.write(line)
        host_file.truncate()
    print("Done!")
