import urllib 
import csv
import numpy as np
import codecs
from bs4 import BeautifulSoup
from itertools import *
import mechanize
import webbrowser
import re
from readcol import *
from urllib2 import HTTPError
import socket
import os
socket.setdefaulttimeout(5)


def str2float(x):
    y=np.array([float(x[i]) for i in range(len(x))])
    return y



def crts_download(ra=153.82315, dec=42.47681, ID='a', outdir='./CRTS_data_bls1/', rad=0.05):
    """
    rad=0.05 # unit arcmin  the value corresponds to 3 arcsec
    output: CRTS if found

    """
    global file2
    timeout_occurred = False
    url = 'http://nunuku.caltech.edu/cgi-bin/getcssconedb_release_img.cgi'
    br = mechanize.Browser()
    try:
        br.open(url, timeout=100.0)
        br.select_form(nr = 0)
        br['RA'] = str(ra)
        br['Dec'] = str(dec)
        br['Rad'] = str(rad)
        br['IMG'] = ['nun']    # These are for the radio buttons.
        br['DB'] = ['photcat']
        br['OUT'] = ['csv']
        br['SHORT'] = ['short']
        response = br.submit()
        content = response.read()
    except (socket.timeout, mechanize.HTTPError,mechanize.URLError):
        #if isinstance(exc.reason, socket.timeout):
        timeout_occurred = True
        try: 
            print "First try"
            br.open(url, timeout=100) 
            br.select_form(nr = 0)
            br['RA'] = str(ra)
            br['Dec'] = str(dec)
            br['Rad'] = str(rad)
            br['IMG'] = ['nun']    # These are for the radio buttons.
            br['DB'] = ['photcat']
            br['OUT'] = ['csv']
            br['SHORT'] = ['short']
            response = br.submit()
            content = response.read()
                #except mechanize.URLError as exc:
                #if isinstance(exc.reason, socket.timeout):
        except  (socket.timeout, mechanize.HTTPError,mechanize.URLError):  #  socket.error
            timeout_occurred = True
            print "Second try"
            br.open(url, timeout=100)
            br.select_form(nr = 0)
            br['RA'] = str(ra)
            br['Dec'] = str(dec)
            br['Rad'] = str(rad)
            br['IMG'] = ['nun']    # These are for the radio buttons.
            br['DB'] = ['photcat']
            br['OUT'] = ['csv']
            br['SHORT'] = ['short']
            response = br.submit()
            content = response.read()
            
               
    #with open('results.html', 'w') as f:
    #    f.write(content)
    
    ds=[m.start() for m in re.finditer(', data: ', str(content))]
    df=[m.start() for m in re.finditer(',]}', str(content))]
    if len(ds)>0:
        file1=open(outdir+ID+'_crts', "w")
        for j in range(len(ds)):
            ta=str(content)[ds[j]+9:df[j]]
            aa=ta.split(',')
            ncol=3
            nrow=len(aa)/ncol
            aa1=np.reshape(aa, (nrow, ncol))
            
            for i in range(nrow):
                mjd, fl, efl=aa1[i]
                mjd=mjd.split('[')[1]
                efl=efl.split(']')[0]
                file1.write('{0}\t {1}\t {2}\n'.format(mjd, fl, efl))

        file1.close() 
    else:
        file2.write('{0}\t {1}\t {2}\t {3}\n'.format(ID, ra, dec, 'Not found'))

    #except (UnboundLocalError):
    #    print "passing TIMEOUT"
    #    file2.write('{0}\t {1}\t {2}\t {3}\n'.format(ID, ra, dec, 'pass timeout'))
    #    pass
    #except HTTPError:
    #print "passing HTTPError"
    #file2.write('{0}\t {1}\t {2}\t {3}\n'.format(ID, ra, dec, 'Not found'))
    #pass    
    #except socket.timeout as e:
    #    print "passing TIMEOUT"
    #    file2.write('{0}\t {1}\t {2}\t {3}\n'.format(ID, ra, dec, 'Not found'))
    #    pass
        
        
# run the download function
bls1=readcol("crts_coord_BLS1.list")

outdir='./CRTS_data_BLS1_ob2ob/'
ID=bls1[:, 0]
ra=str2float(bls1[:, 1])
dec=str2float(bls1[:, 2])
file2=open(outdir+"log", "w")
for i in range(14487, len(ID)):
    print "index:", i, "ID:", ID[i]
    crts_download(ra=ra[i], dec=dec[i], ID=ID[i], outdir=outdir, rad=0.05) 
    # rad =0.05' i.e 3'' following Graham et al. 2015

file2.close()



