#!/usr/bin/python
# -*- coding: utf8 -*-
# ~/.aws/credentials 要有AWS key and secret
#
# 處理 credentials 設定值
# print (aws_key_id +":"+ aws_secret_id)
import ConfigParser, StringIO

#=== CONSTANTS ================================================================

# section name for options without section:
NOSECTION = 'NOSECTION'


#=== CLASSES ==================================================================

class SimpleConfigParser(ConfigParser.RawConfigParser):
    """
    Simple configuration file parser: based on ConfigParser from the standard
    library, slightly modified to parse configuration files without sections.

    Inspired from an idea posted by Fredrik Lundh:
    http://mail.python.org/pipermail/python-dev/2002-November/029987.html
    """

    def read(self, filename):
        text = open(filename).read()
        f = StringIO.StringIO("[%s]\n" % NOSECTION + text)
        self.readfp(f, filename)

    def getoption(self, option):
        'get the value of an option'
        return self.get(NOSECTION, option)


    def getoptionslist(self):
        'get a list of available options'
        return self.options(NOSECTION)


    def hasoption(self, option):
        """
        return True if an option is available, False otherwise.
        (NOTE: do not confuse with the original has_option)
        """
        return self.has_option(NOSECTION, option)

filename = '/etc/sysconfig/sshd'
cp = SimpleConfigParser()
cp.optionxform = str
cp.read(filename)
#print 'getoptionslist():', cp.getoptionslist()
for option in cp.getoptionslist():
    print "%s = %s" % (option, cp.getoption(option))
print "hasoption('HOSTNAME') =", cp.hasoption('HOSTNAME')
