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
        if self.keywords.get('RE_TYPE') != 'NONEQ':
            self._exit("RE_TYPE is not NONEQ")
        
        if self.keywords.get('ENGINE') != 'IMPACT':
            self._exit("ENGINE is not IMPACT")
        
        self.extfiles = self.keywords.get('ENGINE_INPUT_EXTFILES')
        if not (self.extfiles is None):
            if self.extfiles != '':
                self.extfiles = self.extfiles.split(',')
        
        if self.keywords.get('TEMPERATURES') is None:
            self._exit("TEMPERATURES needs to be specified")
        temperatures = self.keywords.get('TEMPERATURES').split(',')
        
        if self.keywords.get('JOB_TRANSPORT') is 'SSH':
            if self.keywords.get('EXEC_DIRECTORY') is None:
                self._exit("EXEC DIRECTORY needs to be specified")

        if self.keywords.get('TOTAL_STEPS') is not None:
            self.total_steps = int(self.keywords.get('TOTAL_STEPS'))
        
        if self.keywords.get('NUM_CHUNKS') is not None:
            self.num_chunks = int(self.keywords.get('NUM_CHUNKS'))

    def _buildBEDAMStates(self,lambads,temperatures):
	pass

    def _buildInpFile(self, replica):
        """
        Builds input file for a BEDAM replica based on template input file
        BASENAME.inp for the specified replica at lambda=lambda[stateid] for the
        specified chunk.
        """
        basename = self.basename
        stateid = self.status[replica]['stateid_current']
        chunk = self.status[replica]['chunk_current']

        template = "%s.inp" % basename
        inpfile = "r%d/%s_%d.inp" % (replica, basename, chunk)

        # read template buffer
        tfile = self._openfile(template, "r")
        tbuffer = tfile.read()
        tfile.close()
        # make modifications
        tbuffer = tbuffer.replace("@n@",str(chunk))
        tbuffer = tbuffer.replace("@nm1@",str(chunk-1))
        tbuffer = tbuffer.replace("@ss@",str((chunk-1)*(self.total_steps/self.num_chunks) + 1))
        # write out
        ofile = self._openfile(inpfile, "w")
        ofile.write(tbuffer)
        ofile.close()

    def _doExchange_pair(self,repl_a,repl_b):
	pass

    def _extractLast_lambda_BindingEnergy_TotalEnergy(self,repl,chunk):
        """
        Extracts binding energy from Impact output
        """
        output_file = "r%s/%s_%d.out" % (repl,self.basename,chunk)
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
	pass

    def _getPot(self,repl,chunk):
        (lmb, u, etot) = self._extractLast_lambda_BindingEnergy_TotalEnergy(repl,chunk)
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

    rx = noneq_async_re_job(commandFile, options=None)

    rx.setupJob()

    rx.scheduleJobs()
