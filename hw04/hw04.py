import argparse
import os
import multiprocessing
import requests
import threading

from requests.exceptions import HTTPError, ReadTimeout, ConnectionError
from time import time
from urllib.parse import urlparse, unquote


def download_image(destination_path: str, url_str: str) -> None:
    """
    Download image and save it into directory. Prints download time in ns or Error Code
    :param destination_path: Destination directory
    :param url_str: Image url
    """
    error_code = 0
    filename = extract_filename_from_url(url_str)
    start_time = time()
    try:
        with open(os.path.join(destination_path, filename), 'wb') as f:
            f.write(requests.get(url_str).content)
    except FileNotFoundError:
        error_code = -1000
    except PermissionError:
        error_code = -1001
    except OSError:
        error_code = -1002
    except HTTPError:
        error_code = -2000
    except ReadTimeout:
        error_code = -2001
    except ConnectionError:
        error_code = -2002
    if error_code == 0:
        #sleep(3)
        end_time = time()
        print(f'{filename} download time {(time() - start_time):.2f} s (from  {start_time:.2f} till {end_time:.2f})')
    else:
        print(url_str, f'Error: {error_code}')


def extract_filename_from_url(url_str: str) -> str:
    """
    Extracts filename from url
    :param url_str: File url
    :return: filename
    """
    return unquote(os.path.basename(urlparse(url_str).path))


def multiprocessing_downloads(destination_path: str, urls_list: list) -> None:
    """
    Downloads files from url_list using multiprocessing
    :param destination_path: Destination path
    :param urls_list: List of URLs
    :return:
    """
    print('Starting multiprocessing downloads')
    start_time = time()
    processes = []
    for url_str in urls_list:
        p = multiprocessing.Process(target=download_image, args=(destination_path, url_str))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

    print(f'Total time: {time() - start_time}')


def multithreading_downloads(destination_path: str, urls_list: list) -> None:
    """
    Downloads files from url_list using multithreading
    :param destination_path: Destination path
    :param urls_list: List of URLs
    :return:
    """
    print('Starting multithreading downloads')
    start_time = time()
    threads = []
    for url_str in urls_list:
        t = threading.Thread(target=download_image, args=(destination_path, url_str))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    print(f'Total time: {time() - start_time}')


def sync_downloads(destination_path: str, urls_list: list) -> None:
    """
    Downloads files from url_list using sync downloads
    :param destination_path: Destination path
    :param urls_list: List of URLs
    :return:
    """
    start_time = time()
    for url_str in urls_list:
        download_image(destination_path, url_str)
    print(f'Total time: {time() - start_time}')


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(
        description='Downloading files to destination path from URLs list'
    )

    parse_type = args_parser.add_mutually_exclusive_group(required=True)

    parse_type.add_argument(
        '-m',
        dest='parse_action',
        action='store_const',
        const=multithreading_downloads,
        help='Download using multithreading'
    )
    parse_type.add_argument(
        '-p',
        dest='parse_action',
        action='store_const',
        const=multiprocessing_downloads,
        help='Download using multiprocessing'
    )
    parse_type.add_argument(
        '-s',
        dest='parse_action',
        action='store_const',
        const=sync_downloads,
        help='Download using sync'
    )
    args_parser.add_argument('--threads', dest='parse_type',
                             action='store_const', const='threads')
    args_parser.add_argument('--path', type=str, help='Destination directory')
    args_parser.add_argument('--urls', type=str, nargs='+', help='Image URLS')

    parsing_method = args_parser.parse_args().parse_action
    destination_directory = args_parser.parse_args().path
    urls_list = args_parser.parse_args().urls

    parsing_method(destination_directory, urls_list)
