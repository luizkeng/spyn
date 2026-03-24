import subprocess
import os

nproc = subprocess.getoutput('nproc')
pwd = subprocess.getoutput('pwd')

subprocess.run('bash {}/dependency.sh'.format(pwd), shell=True)
subprocess.run('tar -xvf {}/qe/qe-7.3.tar.gz -C {}/qe/'.format(pwd, pwd), shell=True)
subprocess.run('bash {}/qe/qe-7.3/configure --enable-parallel'.format(pwd), shell=True)
subprocess.run('make -j {} pw -C {}/qe/qe-7.3/'.format(nproc, pwd), shell=True)
subprocess.run('make -j {} gipaw -C {}/qe/qe-7.3/'.format(nproc, pwd), shell=True)
subprocess.run('bash {}/simbolic.sh'.format(pwd), shell=True)

