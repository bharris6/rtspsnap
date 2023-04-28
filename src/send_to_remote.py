#!/usr/bin/env python3
import argparse

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient


def send_to_remote(filepath, remote_host, username, key_file=None, remote_path=".", insecure=True):

    with SSHClient() as sshconn:
        sshconn.load_system_host_keys()

        if insecure:
            sshconn.set_missing_host_key_policy(AutoAddPolicy)

        if key_file:
            sshconn.connect(remote_host,
                            username=username,
                            key_filename=key_file)
        else:
            sshconn.connect(remote_host,
                            username=username)

        with SCPClient(sshconn.get_transport(), socket_timeout=90.0) as scpconn:
            scpconn.put(filepath, remote_path.encode())

if __name__ == '__main__':

    description = "Send a file to a remote machine"
    parser = argparse.ArgumentParser(usage=None, description=description)

    parser.add_argument("-f",
                        "--file",
                        type=str,
                        required=True,
                        help="Path to file to tranfer.")
    
    parser.add_argument("-i",
                        "--insecure",
                        action="store_true",
                        default=False,
                        help="Whether to ignore known_hosts")
    
    parser.add_argument("-r",
                        "--remote-host",
                        type=str,
                        required=True,
                        help="Remote host to transfer file to.")
    
    parser.add_argument("-p",
                        "--remote-path",
                        type=str,
                        required=False,
                        default=".",
                        help="Path to place file in on remote host.")

    parser.add_argument("-u",
                        "--username",
                        type=str,
                        required=True,
                        help="Username for connection to remote host.")

    parser.add_argument("-k",
                        "--key-path",
                        type=str,
                        required=False,
                        help="Path to private key file to use.")

    args = parser.parse_args()

    send_to_remote(args.file, args.remote_host, args.username, args.key_path, args.remote_path, args.insecure)
