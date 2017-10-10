#!/env/python

import os
import sys
import argparse
import commands
import subprocess
import time
import logging
import socket

# Creates a directory tree.
def mkdir(name,mode=0777):
    if os.path.isdir(name) == False:
        try:
            os.makedirs(name, mode)

        except Exception as e:
            time.sleep(0.1)

            if (os.path.isdir(name) == True):
                # a parallel process has just created this directory
                pass
            else:
                print 'Error creating directory "%s":' % name
                print type(e), e

    return os.path.isdir(name)

# Log something, either through a logger object or a print statement
def log(logger, logLevel ,message):

    if logLevel:
        if isinstance(logLevel,basestring) and logLevel.upper() in levels:
            logLevel = levels[logLevel.upper()]

        if isinstance(logger,logging.Logger):

            logger.log(logLevel,message)

        else:

            formatDict = {logging.ERROR   : '-E- %s',
                          logging.WARNING : '-W- %s',
                          logging.INFO    : '-I- %s',
                          logging.DEBUG   : '-D- %s'
                         }

            print formatDict[logLevel]%(message)

# Executes a command and returns the status and output.
def execute(cmd, debug=None, output=True, logger=None, env=None, shell=False):
    stat    = 0
    bufsize = -1 ; # 0 | 1 | x = unbuffered | line buffered | use buffer of that size

    debug = ('debug' if debug else '')
    list2cmdline = lambda x: x if isinstance(x,basestring) else subprocess.list2cmdline(x)

    log(logger, debug, '')
    log(logger, debug, 'execute(' + list2cmdline(cmd) + ')')
    log(logger, debug, '=== ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +  ' - START on ' + socket.gethostname())

    try:
        process = subprocess.Popen(cmd,bufsize=bufsize,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,shell=shell);
    except Exception as e:
        stat = 1
        text = str(e)
        if not os.path.exists(cmd[0]):
            text += '\n-E- Missing binary: ' + cmd[0]

    if stat == 0:
        text = ''
        
        doWhileCondition = True

        # Get the command output and wait for the process to be finished
        while doWhileCondition:
            lines = process.stdout.readlines()
            for line in lines:
                if line:
                    text = text + line
                    sys.stdout.flush()
                    sys.stderr.flush()
                    if output:
                        # Strip the last character (newline character)
                        log(logger, debug, '\t' + line[:-1])

            if doWhileCondition:
                doWhileCondition = (process.poll() and process.wait()) is None

        # Get the return status from the command
        stat = process.wait()

        if text[-1:] == '\n': 
            text = text[:-1]

        log(logger,debug,'=== ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' - END (exit = ' + str(stat) + ')')
        log(logger,debug,'')

    return stat, text

# Parse command-line arguments
parser = argparse.ArgumentParser()

parser.add_argument('-tlx',  action='store', dest='tlx',    required=True,                                help='Top-left longitude coordinate of bbox.'          , type=float)
parser.add_argument('-tly',  action='store', dest='tly',    required=True,                                help='Top-left latitude coordinate of bbox.'           , type=float)
parser.add_argument('-brx',  action='store', dest='brx',    required=True,                                help='Bottom-left longitude coordinate of bbox.'       , type=float)
parser.add_argument('-bry',  action='store', dest='bry',    required=True,                                help='Bottom-left latitude coordinate of bbox.'        , type=float)
parser.add_argument('-type', action='store', dest='type',   required=True, choices=['LAI', 'NDVI', 'BA'], help='Product type.'                                               )
parser.add_argument('-in',   action='store', dest='input',  required=True,                                help='Full path to the input file to be customized.'               )
parser.add_argument('-out',  action='store', dest='output', required=True,                                help='Full path to the customized GEOTIFF output file.'            )

results = parser.parse_args()

# Dataset name inside NetCDF file
sds = results.type

if sds == 'BA': 
    sds = 'BA_DEKAD'

# Create output directory if not yet existing
mkdir(os.path.dirname(results.output))

input = results.input

if input.startswith("file://"):
    input = results.input[7:]

# Perform customization
status, output = execute( ["gdal_translate", "-of", "GTiff", "-projwin", "%.5f" % results.tlx, "%.5f" % results.tly, "%.5f" % results.brx, "%.5f" % results.bry, 'NETCDF:"%s":%s' % (input, sds), results.output] );

print output
sys.exit(status);



