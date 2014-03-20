import os
import logging

import requests.sessions
import requests.cookies

import internetarchive.config
import internetarchive.item


class ArchiveSession(object):

    FmtString = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # __init__()
    #_____________________________________________________________________________________
    def __init__(self, config=None):
        super(ArchiveSession, self).__init__()
        config = config if config else internetarchive.config.get_config()
        self.cookies = requests.cookies.cookiejar_from_dict(config.get('cookies', {}))
        if not 'logged-in-user' in self.cookies:
            self.cookies['logged-in-user'] = os.environ.get('IA_LOGGED_IN_USER')
        if not 'logged-in-sig' in self.cookies:
            self.cookies['logged-in-sig'] = os.environ.get('IA_LOGGED_IN_SIG')

        self.config = config
        self.secure = config.get('secure', False)

        s3_config = self.config.get('s3', {})
        self.access_key = s3_config.get(('access_key'), os.environ.get('IA_S3_ACCESS_KEY'))
        self.secret_key = s3_config.get(('secret_key'), os.environ.get('IA_S3_ACCESS_KEY'))

    # __init__()
    #_____________________________________________________________________________________
    def set_file_logger(self, log_level, path, logger_name='internetarchive'):
        """Convenience function to quickly configure any level of
        logging to a file.

        :type log_level: int
        :param log_level: A log level as specified in the `logging` module

        :type path: string
        :param path: Path to the log file. The file will be created
        if it doesn't already exist.

        """
        log = logging.getLogger(logger_name)
        log.setLevel(logging.DEBUG)
        fh = logging.FileHandler(path)
        fh.setLevel(log_level)
        formatter = logging.Formatter(self.FmtString)
        fh.setFormatter(formatter)
        log.addHandler(fh)


def get_session(config=None):
    """
    Return a new ArchiveSession object

    """
    return ArchiveSession(config)
