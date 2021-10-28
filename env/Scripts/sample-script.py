#!"d:\work\ce 4th year\sem 7\sgp\sgp_final\env\scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'yfinance==0.1.63','console_scripts','sample'
__requires__ = 'yfinance==0.1.63'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('yfinance==0.1.63', 'console_scripts', 'sample')()
    )
