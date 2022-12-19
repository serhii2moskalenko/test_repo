import socket

"""
Let's find out the IP address of the site using Python
"""

def get_ip():
    hostname=input('Plese enter URL(address):  ')
    try:
        return f'Hostname: {hostname}\nIP address: {socket.gethostbyname(hostname)}'
    except socket.gaierror as error:
        return f'Invalid URL - {error}'


def main():
    print(get_ip())


if __name__ == '__main__':
    main()
