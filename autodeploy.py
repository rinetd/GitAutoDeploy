#!/usr/bin/env python
import json
import os
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from subprocess import call
import re
import pdb
import logging

logging.basicConfig(level=logging.INFO,
                    format='\n%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s \n%(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filemode='w')

class GitOSCAutoDeploy(BaseHTTPRequestHandler):
    CONFIG_FILEPATH = './conf.json'
    config = None
    quiet = False
    daemon = False
    branch = None
    url = None

    @classmethod
    def getConfig(myClass):
        if (myClass.config == None):
            try:
                configString = open(myClass.CONFIG_FILEPATH).read()
            except:
                sys.exit('Could not load ' + myClass.CONFIG_FILEPATH + ' file')
            try:
                myClass.config = json.loads(configString)
            except:
                sys.exit(myClass.CONFIG_FILEPATH + ' file is not valid json')

            for repository in myClass.config['repositories']:
                if (not os.path.isdir(repository['path'])):
                    try:
                        os.mkdir(repository['path'])
                    except:
                        sys.exit('Can NOT make a repository directory' + repository['path'])
                        # sys.exit('Directory ' + repository['path'] + ' not found')
                # Check for a repository with a local or a remote GIT_WORK_DIR
                if not os.path.isdir(os.path.join(repository['path'], '.git')) \
                        and not os.path.isdir(os.path.join(repository['path'], 'objects')):
                    try:
                        os.system('git clone' + " " + repository['url'] + " " + repository['path'])
                    except:
                        sys.exit('Can NOT clone repository directory into ' + os.path.isdir(repository['path']))
                        # sys.exit('Directory ' + repository['path'] + ' is not a Git repository')
        return myClass.config
    def getHeader(self):
        content_type = self.headers.getheader('content-type')
        content_length = int(self.headers.getheader('content-length'))

        request_header = self.headers
        logging.debug('Password:[%s]' % self.headers.getheader('Password'))
        logging.debug('%s %s %s',self.command, self.path , self.request_version)
        logging.debug('%s' % self.headers)

        return request_header

    def getData(self):
        content_type = self.headers.getheader('content-type')
        content_length = int(self.headers.getheader('content-length'))
        if content_length <= 0:
            sys.exit('Get content-length from headers failed!')
        request_body = self.rfile.read(content_length)

        logging.debug('[%s]' % request_body)
        return request_body

    def do_GET(self):
        self.getHeader()
        self.getData()

    def do_POST(self):
        self.getHeader()
        event = self.headers.getheader('Password')

        if event == '123.56.234.219':
            if not self.quiet:
                print 'Ping event received'
            self.respond(204)
            return
        self.respond(204)

        urls = self.parseRequest()
        for url in urls:
            paths = self.getMatchingPaths(url)
	    print paths
            for path in paths:
                self.fetch(path)
                self.deploy(path)

    def validateurl(self):
        regex = re.compile(
                r'^(?:http|ftp)s?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        try:
            # TODO
            # There must a bug on way
            validatedurl = re.match(regex, self.url, 0)
        except Exception:
            sys.exit('Validate URL failed!')
        return validatedurl

    def parseRequest(self):
        body = self.getData()
        try:
            json.loads(body)
        except Exception:
            # do http decode
            import urllib
            body = urllib.unquote(body)
        ### new
            json.loads(body)
        ### old
        # try:
        #     json.loads(body)
        # except Exception:
        #     # do remove 5 character
        #     body = body[5:]
        ####
        payload = json.loads(body)
        self.branch = payload['hook']['push_data']['ref']
        for url in [payload['hook']['push_data']['repository']['url']]:
            self.url = url
            self.validateurl()
        return [payload['hook']['push_data']['repository']['url']]

    def getMatchingNaems(self, repoName):
        res = []
        config = self.getConfig()
        for repository in config['repositories']:
            if (repository['name'] == repoName):
                res.append(repository['path'])
        return res

    def getMatchingPaths(self, repoUrl):
        res = []
        config = self.getConfig()
        for repository in config['repositories']:
            if (repository['url'] == repoUrl):
                res.append(repository['path'])
        return res

    def respond(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def fetch(self, path):
        if (not self.quiet):
            print "\nPost push request received"
            print 'Updating ' + path
            os.system('cd "' + path + '" && git pull -f')
            os.system('chown -R www-data:www-data '+path)

	    print 'pull complete '
    def deploy(self, path):
        config = self.getConfig()
        for repository in config['repositories']:
            if (repository['path'] == path):
                if 'deploy' in repository:
                    branch = None
                    if 'branch' in repository:
                        branch = repository['branch']

                    if branch is None or branch == self.branch:
                        if (not self.quiet):
                            print 'Executing deploy command'
                            os.system('cd "' + path + '" && ' + repository['deploy'])
			    print 'deploy complete '
                    elif not self.quiet:
                        print 'Push to different branch (%s != %s), not deploying' % (branch, self.branch)
                break
def main():
    try:
        server = None
        for arg in sys.argv:
            if (arg == '-d' or arg == '--daemon-mode'):
                GitOSCAutoDeploy.daemon = True
                GitOSCAutoDeploy.quiet = True
            if (arg == '-q' or arg == '--quiet'):
                GitOSCAutoDeploy.quiet = True

        if (GitOSCAutoDeploy.daemon):
            pid = os.fork()
            if (pid != 0):
                sys.exit()
            os.setsid()
        if (not GitOSCAutoDeploy.quiet):
            print 'Github Autodeploy Service v0.2 started'
        else:
            print 'Github Autodeploy Service v 0.2 started in daemon mode'

        server = HTTPServer(('', GitOSCAutoDeploy.getConfig()['port']), GitOSCAutoDeploy)
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit) as e:
        if (e):  # wtf, why is this creating a new line?
            print >> sys.stderr, e

        if (not server is None):
            server.socket.close()

        if (not GitOSCAutoDeploy.quiet):
            print 'Goodbye'


if __name__ == '__main__':
    main()
