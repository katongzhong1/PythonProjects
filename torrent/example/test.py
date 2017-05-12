# -*- coding: utf-8 -*-

from datetime import *
import time
import re
from time import sleep
import bencode
import urllib2
import base64
try:
        hash = row[1]
        url = "http://haofuli.duapp.com/go/info.php?hash=%s" % hash
        file = urllib2.urlopen(url).read()
        if "error!" == file:
            pass
        else:
            #decode
            try:
                fileEncode = bencode.bdecode(file)
            except Exception,e:pass
            if 'name.utf-8' in fileEncode['info']:
                filename=fileEncode['info']['name.utf-8']
            else:
                filename = fileEncode['info']['name']
            ##length
            if "length" in fileEncode['info']:
                length = fileEncode['info']['length']
            else:
                length = 0
            try:
                sql = "update bt_main set name = %s , length = %s , isTrue = 1 where id = %s"
                re = cur.execute(sql,(base64.b64encode(filename),length,id))
                conn.commit()
            except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])