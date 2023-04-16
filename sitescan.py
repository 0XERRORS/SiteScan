import requests
from bs4 import BeautifulSoup
import re
import subprocess

# Function to install packages using pip
def install_package(package):
    try:
        subprocess.check_output(['pip', 'install', package])
        print(f'Successfully installed {package}.')
    except subprocess.CalledProcessError as e:
        print(f'Error installing {package}: {e.output}.')
    except Exception as e:
        print(f'Error: {e}')


# Function to get links from a webpage
def get_page_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('http'):
                links.append(href)
        return links
    except requests.exceptions.HTTPError as e:
        print(f'Error fetching URL: {e}')
    except Exception as e:
        print(f'Error: {e}')


# Function to get API endpoints and their extensions
def get_api_endpoints(links):
    api_endpoints = []
    for link in links:
        if 'api' in link:
            path = re.findall(r'/([a-zA-Z]+)/?$', link)
            if path:
                api_endpoints.append((link, path[0]))
    return api_endpoints


# Function to perform Nmap scan on a domain
def nmap_scan(domain):
    try:
        cmd = f'nmap {domain}'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        ip = re.findall(r'Nmap scan report for (.+)\n', output)
        ip = ip[0] if ip else 'Unknown'
        ports = re.findall(r'([0-9]+)/tcp', output)
        ports = ports if ports else []
        return ip, ports
    except subprocess.CalledProcessError as e:
        print(f'Error performing Nmap scan: {e.output}.')
    except Exception as e:
        print(f'Error performing Nmap scan: {e}')


if __name__ == '__main__':
    # Install BeautifulSoup and requests if not already installed
    try:
        import pyfiglet
        import bs4
        import requests
    except ImportError:
        print('Missing dependencies. Installing required packages...')
        install_package('beautifulsoup4')
        install_package('requests')
        import bs4
        import requests

    url = input('Enter the domain:▷ ')
    url = 'http://' + url if not url.startswith('http') else url
    links = get_page_links(url)
    if links:
        print(f'Links found on {url}:')
        for link in links:
            print(link)
        api_endpoints = get_api_endpoints(links)
        if api_endpoints:
            print('\nAPI Endpoints:')
            for endpoint, extension in api_endpoints:
                print(f'Endpoint: {endpoint}\nExtension: {extension}\n')
        else:
            print('No API endpoints found.')
    else:
        print('No links found.')

    # Perform Nmap scan on the domain
    domain = url.split('//')[1]
    ip, ports = nmap_scan(domain)
    print(f'Domain: {domain}\nIP Address: {ip}\nPorts: {ports}')
