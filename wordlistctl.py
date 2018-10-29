#!/usr/bin/env python3

__author__ = 'Sepehrdad Sh'
__organization__ = 'blackarch.org'
__license__ = 'GPLv3'
__version__ = '0.2alpha'
__project__ = 'wordlistctl.py'

__wordlist_path__ = '/usr/share/wordlists'

__urls__ = {
            'darkc0de':
                'https://github.com/danielmiessler/SecLists/raw/master/Passwords/darkc0de.txt',
            'rockyou':
                'https://github.com/danielmiessler/SecLists/raw/master/Passwords/Leaked-Databases/rockyou.txt.tar.gz',
            'cain-and-abel':
                'https://github.com/danielmiessler/SecLists/raw/master/Passwords/Software/cain-and-abel.txt',
            'john-the-ripper':
                'https://github.com/danielmiessler/SecLists/raw/master/Passwords/Software/john-the-ripper.txt',
            'crackstation':
                'https://crackstation.net/files/crackstation.txt.gz',
            'crackstation-human-only':
                'https://crackstation.net/files/crackstation-human-only.txt.gz',
            'Weakpass 2.0':
                'http://www.mediafire.com/file/q8u95nni5nrxuoc/weakpass_2.7z',
            'Weakpass 2.0 wifi':
                'http://www.mediafire.com/file/d5eyflor7gkftf5/weakpass_2_wifi.7z',
            'Weakpass 2.0 policy':
                'http://www.mediafire.com/file/uj824lip85rdqo4/weakpass_2p.7z',
            'Weakpass 1.0':
                'http://www.mediafire.com/file/k7ulswoloauzsu5/weakpass_1.gz',
            'Weakpass 1.0 wifi':
                'http://www.mediafire.com/file/42rsua4dr7r01tr/weakpass_wifi_1.gz',
            'Weakpass':
                'http://www.mediafire.com/file/d96hha7y7hwwd6a/weakpass.gz',
            'SecLists':
                'https://github.com/danielmiessler/SecLists/archive/master.zip',
            'HashesOrg':
                'http://www.mediafire.com/file/vi4y1kfs4semt9a/HashesOrg.gz',
            'MegaCracker':
                'http://www.mediafire.com/file/14vvacvc5qtu8ba/MegaCracker.txt.gz',
            'Sqlmap':
                'http://www.mediafire.com/file/0k71k1g39mcxgwu/sqlmap.txt.gz',
            'Hashkiller Passwords':
                'http://home.btconnect.com/md5decrypter/hashkiller-dict.rar',
            'WordlistBySheez_v8':
                'http://www.mediafire.com/file/8oazhwqzexid771/WordlistBySheez_v8.7z',
            'HyperionOnHackForumsNetRELEASE':
                'http://www.mediafire.com/file/118gd6bkcnn9j58/HyperionOnHackForumsNetRELEASE.txt.gz',
            'Backtrack_big_password_library':
                'http://www.mediafire.com/file/cml6ge2fppa4jiu/Backtrack_big_password_library.gz'
            }


def printerr(string, ex):
    print("{0} {1}".format(string, ex), file=sys.stderr)


def usage():
    __usage__ = "usage:\n"
    __usage__ += "  {0} -f <arg> | -d <arg> | <misc>\n\n"
    __usage__ += "options:\n\n"
    __usage__ += "  -f <num>   - download chosen wordlist\n"
    __usage__ += "             - ? to list wordlists\n"
    __usage__ += "  -d <dir>   - wordlists base directory (default: {1})\n"
    __usage__ += "  -s <regex> - wordlist to search using <regex> in base directory\n\n"
    __usage__ += "misc:\n\n"
    __usage__ += "  -v         - print version of wordlistctl and exit\n"
    __usage__ += "  -h         - print this help and exit\n"

    print(__usage__.format(__project__, __wordlist_path__))


def version():
    __str_version__ = "{0} v{1}".format(__project__, __version__)
    print(__str_version__)


def banner():
    __str_banner__ = "--==[ {0} by {1} ]==--\n".format(__project__, __organization__)
    print(__str_banner__)


def fetch_torrent(url, path):
    pass


def fetch_file(url, path):
    print("[*] downloading {0}".format(path.split('/')[-1]))

    try:

        chunk_size = 1024
        rq = requests.get(url, stream=True)
        total_size = int(rq.headers['content-length'])
        fp = open(path, 'wb')
        for data in tqdm(iterable=rq.iter_content(chunk_size=chunk_size), total=total_size / chunk_size, unit='KB'):
            fp.write(data)
        fp.close()

    except Exception as ex:

        printerr("Error while downloading {0}".format(url), ex)
        os.remove(path)


def download_wordlists(code):
    __wordlist_id__ = 0

    check_dir(__wordlist_path__)

    try:

        __wordlist_id__ = int(code)
        if __wordlist_id__ >= __urls__.__len__() + 1:
            raise IndexError
        elif __wordlist_id__ < 0:
            raise IndexError
        elif __wordlist_id__ == 0:
            for i in __urls__:
                fetch_file(__urls__[i], "{0}/{1}".format(__wordlist_path__, __urls__[i].split('/')[-1]))
        else:
            i = list(__urls__.keys())[__wordlist_id__ - 1]
            fetch_file(__urls__[i], "{0}/{1}".format(__wordlist_path__, __urls__[i].split('/')[-1]))

    except Exception as ex:

        printerr("Error unable to download wordlist", ex)
        return -1

    return 0


def print_wordlists():
    index = 1
    print("[+] available wordlists")
    print("    > 0  - all wordlists")
    for i in __urls__:
        print("    > {0}  - {1}".format(index, i))
        index += 1


def search_dir(regex):
    print('[+] searching for {0} in {1}'.format(regex, __wordlist_path__))
    os.chdir(__wordlist_path__)
    files = glob.glob("{0}".format(str(regex)))
    if files.__len__() <= 0:
        print("[-] wordlist not found")
        return
    for file in files:
        print("[+] wordlist found: {0}".format(os.path.join(__wordlist_path__, file)))


def check_dir(dir_name):
    try:

        if os.path.isdir(dir_name):
            pass
        else:
            print("[*] creating directory {0}".format(dir_name))
            os.mkdir(dir_name)

    except Exception as ex:

        printerr("unable to change base directory", ex)
        exit(-1)


def main(argv):
    global __wordlist_path__
    banner()

    try:

        opts, args = getopt.getopt(argv[1:], "hvf:d:s:")

    except Exception as ex:

        printerr("Error while parsing arguments", ex)
        return -1

    if opts.__len__() <= 0:
        usage()
        return 0

    try:

        for opt, arg in opts:
            if opt == '-h':
                usage()
                return 0
            elif opt == '-v':
                version()
                return 0
            elif opt == '-d':
                check_dir(arg)
                __wordlist_path__ = arg
            elif opt == '-f':
                if arg == '?':
                    print_wordlists()
                    return 0
                else:
                    return download_wordlists(arg)
            elif opt == '-s':
                search_dir(arg)
                return 0

    except KeyboardInterrupt:

        return 0

    except Exception as ex:

        printerr("Error while parsing arguments", ex)
        return -1

    return 0


if __name__ == '__main__':
    try:

        import sys
        import os
        import getopt
        import requests
        import glob
        from tqdm import tqdm

    except Exception as ex:

        printerr("Error while loading dependencies", ex)
        exit(-1)

    sys.exit(main(sys.argv))
