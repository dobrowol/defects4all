import subprocess

def pytest_sessionstart(session):
    subprocess.call("rm -rf tests/out", shell=True)    
    subprocess.call("rm -rf ./tests/data/issue_test2/sequence", shell=True)    
