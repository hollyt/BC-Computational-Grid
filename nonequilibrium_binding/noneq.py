''' APPLICATION for nonequilibrium binding using the ASyncRE software.'''

import sys
import time
import math
import random
import logging
from async_re import async_re
from bedam_async_re import bedam_async_re_job

class noneq_async_re_job(bedam_async_re_job):
    def _setLogger(self):
        self.logger = logging.getLogger("async_re.noneq_async_re")

    def _checkInput(self):
        async_re._checkInput(self)
        # Make sure this is the correct app 
        if self.keywords.get('RE_TYPE') != 'NONEQ':
            self._exit("RE_TYPE is not NONEQ")
        # NONEQ runs with IMPACT
        if self.keywords.get('ENGINE') != 'IMPACT':
            self._exit("ENGINE is not IMPACT")
        # Input files
        self.extfiles = self.keywords.get('ENGINE_INPUT_EXTFILES')
        if not (self.extfiles is None):
            if self.extfiles != '':
                self.extfiles = self.extfiles.split(',')
        # List of temperatures
        if self.keywords.get('TEMPERATURES') is None:
            self._exit("TEMPERATURES needs to be specified")
        temperatures = self.keywords.get('TEMPERATURES').split(',')
        # Read in number of replicas from .inp file 
        # self.nreplicas = 
        #executive file's directory
        if self.keywords.get('JOB_TRANSPORT') is 'SSH':
            if self.keywords.get('EXEC_DIRECTORY') is None:
                self._exit("EXEC DIRECTORY needs to be specified")

    def _buildInpFile(self, replica):
        """
        Builds input file for a BEDAM replica based on template input file
        BASENAME.inp for the specified replica at lambda=lambda[stateid] for the
        specified cycle.
        """
        basename = self.basename
        stateid = self.status[replica]['stateid_current']
        cycle = self.status[replica]['cycle_current']

        template = "%s.inp" % basename
        inpfile = "r%d/%s_%d.inp" % (replica, basename, cycle)

        lambd = self.stateparams[stateid]['lambda']
        temperature = self.stateparams[stateid]['temperature']
        # read template buffer
        tfile = self._openfile(template, "r")
        tbuffer = tfile.read()
        tfile.close()
        # make modifications
        tbuffer = tbuffer.replace("@n@",str(cycle))
        tbuffer = tbuffer.replace("@nm1@",str(cycle-1))
        tbuffer = tbuffer.replace("@lambda@",lambd)
        tbuffer = tbuffer.replace("@temperature@",temperature)
        # write out
        ofile = self._openfile(inpfile, "w")
        ofile.write(tbuffer)
        ofile.close()

        # update the history status file
        ofile = self._openfile("r%d/state.history" % replica, "a")
        ofile.write("%d %d %s %s\n" % (cycle, stateid, lambd, temperature))
        ofile.close()

    def _extractLast_lambda_BindingEnergy_TotalEnergy(self,repl,cycle):
        """
        Extracts binding energy from Impact output
        """
        output_file = "r%s/%s_%d.out" % (repl,self.basename,cycle)
        datai = self._getImpactData(output_file)
        nf = len(datai[0])
        nr = len(datai)
        # [nr-1]: last record
        # [nf-2]: lambda (next to last item)
        # [nf-1]: binding energy (last item)
        #    [2]: total energy item (0 is step number and 1 is temperature)
        #
        # (lambda, binding energy, total energy)
        return (datai[nr-1][nf-2],datai[nr-1][nf-1],datai[nr-1][2])

    def print_status(self):
        """
        Writes to BASENAME_stat.txt a text version of the status of the RE job

        It's fun to follow the progress in real time by doing:

        watch cat BASENAME_stat.txt
        """
        logfile = "%s_stat.txt" % self.basename
        ofile = self._openfile(logfile,"w")
        log = "Replica  State  Lambda Temperature Status  Cycle \n"
        for k in range(self.nreplicas):
            stateid = self.status[k]['stateid_current']
            log += "%6d   %5d  %s %s %5s  %5d \n" % (k, stateid, self.stateparams[stateid]['lambda'], self.stateparams[stateid]['temperature'], self.status[k]['running_status'], self.status[k]['cycle_current'])
        log += "Running = %d\n" % self.running
        log += "Waiting = %d\n" % self.waiting

        ofile.write(log)
        ofile.close()

    def _getPot(self,repl,cycle):
        (lmb, u, etot) = self._extractLast_lambda_BindingEnergy_TotalEnergy(repl,cycle)
        # removes lambda*u from etot to get e0. Note that this is the lambda from the
        # output file not the current lambda.
        e0 = float(etot) - float(lmb)*float(u)
        return (e0,float(u))

    def _getPar(self,repl):
        sid = self.status[repl]['stateid_current']
        lmb = float(self.stateparams[sid]['lambda'])
        tempt = float(self.stateparams[sid]['temperature'])
        kb = 0.0019872041
        beta = 1./(kb*tempt)
        return (beta,lmb)

    def _reduced_energy(self,par,pot):
        # par: list of parameters
        # pot: list of potentials
        # This is for temperature/binding potential beta*(U0+lambda*u)
        beta = par[0]
        lmb = par[1]
        e0 = pot[0]
        u = pot[1]
        return beta*(e0 + lmb*u)

if __name__ == '__main__':

    # Parse arguments:
    usage = "%prog <ConfigFile>"

    if len(sys.argv) != 2:
        print "Please specify ONE input file"
        sys.exit(1)

    commandFile = sys.argv[1]

    print ""
    print "===================================="
    print "NONEQUILIBRIUM IMPACT"
    print "===================================="
    print ""
    print "Started at: " + str(time.asctime())
    print "Input file:", commandFile
    print ""
    sys.stdout.flush()

    rx = bedamtempt_async_re_job(commandFile, options=None)

    rx.setupJob()

    rx.scheduleJobs()
