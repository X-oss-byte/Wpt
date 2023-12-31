import logging
import os
import subprocess
import time
import sys
import urllib


class WPTServer(object):
    def __init__(self, wpt_root):
        self.logger = logging.getLogger()
        self.wpt_root = wpt_root

        # This is a terrible hack to get the default config of wptserve.
        sys.path.insert(0, os.path.join(wpt_root, "tools"))
        from serve.serve import build_config
        with build_config(self.logger) as config:
            self.host = config["browser_host"]
            self.http_port = config["ports"]["http"][0]
            self.https_port = config["ports"]["https"][0]

        self.base_url = f'http://{self.host}:{self.http_port}'
        self.https_base_url = f'https://{self.host}:{self.https_port}'

    def start(self, ssl_context):
        self.devnull = open(os.devnull, 'w')
        wptserve_cmd = [os.path.join(self.wpt_root, 'wpt'), 'serve']
        if sys.executable:
            wptserve_cmd[:0] = [sys.executable]
        self.logger.info(f"Executing {' '.join(wptserve_cmd)}")
        self.proc = subprocess.Popen(
            wptserve_cmd,
            stderr=self.devnull,
            cwd=self.wpt_root)

        for retry in range(5):
            # Exponential backoff.
            time.sleep(2 ** retry)
            exit_code = self.proc.poll()
            if exit_code != None:
                logging.warning('Command "%s" exited with %s', ' '.join(wptserve_cmd), exit_code)
                break
            try:
                urllib.request.urlopen(self.base_url, timeout=1)
                urllib.request.urlopen(self.https_base_url, timeout=1, context=ssl_context)
                return
            except urllib.error.URLError:
                pass

        raise Exception(f'Could not start wptserve on {self.base_url}')

    def stop(self):
        self.proc.terminate()
        self.proc.wait()
        self.devnull.close()

    def url(self, abs_path):
        return f'{self.https_base_url}/{os.path.relpath(abs_path, self.wpt_root)}'
