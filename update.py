import os
import sys
import gzip
import tldextract
import socket
import requests
import time

red_ticket = False


def locate_the_mainland(domains):
    global red_ticket
    ipgeo = 'http://ip.api.com/json/'
    ipgeo_limit = 150
    ipgeo_counter = 0
    ipgeo_timeout = 60
    lines = []

    for domain in domains:
        print('[+] Checking {}'.format(domain))

        if domain.endswith('.cn'):
            # lines.append(domain)
            red_ticket = True
        else:
            addr = socket.gethostbyname(domain)

            if ipgeo_counter < ipgeo_limit:
                if requests.get(ipgeo + addr).json()['country'] == 'China':
                    lines.append(domain)
                    ipgeo_counter += 1
            else:
                ipgeo_counter = 0
                print('[!] API limit exceeded. Sleep...')
                time.sleep(ipgeo_timeout)

    return lines


def line_analyzing(lines):
    domains = []

    for line in lines:
        line = line.split()

        if 'dnsmasq' not in line[4]:
            continue

        ext = tldextract.extract(line[6])
        if ext.registered_domain not in domains:
            domains.append(ext.registered_domain)

    return domains


def log_parsing(path):
    lines = []

    for filename in os.listdir(path):
        if 'syslog' not in filename:
            continue

        log = os.path.abspath(os.path.join(path, filename))

        if log.endswith('.gz'):
            with gzip.open(log, 'rt', encoding='utf-8') as data:
                lines += [line.rstrip() for line in data]
        else:
            with open(log, encoding='utf-8') as data:
                lines += [line.rstrip() for line in data]

    return lines


if __name__ == '__main__':
    if sys.argv[1] and os.path.exists(sys.argv[1]):
        lines = log_parsing(sys.argv[1])
        domains = line_analyzing(lines)
        lines = locate_the_mainland(domains)

        with open('master.txt', 'w') as output:
            output.write('''
                    #
                    # This file is created to be used with Algo VPN adblock
                    # See adblock.sh for more info:
                    #   https://github.com/trailofbits/algo/blob/master/roles/dns_adblocking/templates/adblock.sh.j2
                    #
                    ''')

            if red_ticket:
                print('[+] Add wildcard .CN ccTLD to block list')
                output.write('127.0.0.1\t.cn')

            if len(lines) > 0:
                for line in lines:
                    print('[+] Add {} to block list'.format(line))
                    output.write('127.0.0.1\t{}'.format(line))


