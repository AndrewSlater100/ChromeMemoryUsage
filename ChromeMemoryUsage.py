# Monitors total memory usage of all Chrome processes
# Requirements: Python 3.6+ and Pandas
# Credit to github.com/tfiers
# For use with Windows O/S

print('Press Ctrl-C to stop program')
print('\n..', end='')
import pandas as pd
import subprocess
from io import StringIO
from time import sleep

def get_total_chrome_memory():
    # Call Windows command `tasklist` to get the Task Manager data
    out = subprocess.check_output('tasklist')
    # Decode binary data to a string, and convert to a file-like object so Pandas can read it
    data = StringIO(out.decode('utf-8'))
    # Parse tabular data to a DataFrame using Pandas
    df = pd.read_csv(data, sep=r'\s\s+', skiprows=[2], engine='python')
    # Select only Chrome rows
    chromes = df[df['Image Name'] == 'chrome.exe']

    def parse_mem(s):
        ''' Converts a 'Mem Usage' string to a float, with units [MB] '''
        return int(s[:-2].replace(',', '')) / 1e3

    # Transform the 'Mem Usage' column of strings to a column of floats
    mem = chromes['Mem Usage'].transform(parse_mem)
    # Sum to get Chrome's total memory usage
    return mem.sum()

if __name__ == '__main__':
    try:
        while True:
            usage = get_total_chrome_memory()
            # The carriage return '\r' brings us back to the beginning of the line.
            print(f'\rChrome is currently using {usage / 1e3:.3g} GB of memory     ', end='')
            sleep(0.5)
    except KeyboardInterrupt:
        print('\nThanks!')
