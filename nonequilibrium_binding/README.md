# NONEQUILIBRIUM MD

This is an application for nonequilibrium binding using the Asynchronous Replica Exchange
software.

Check out https://github.com/ComputationalBiophysicsCollaborative/AsyncRE.

<b>Note to self:</b>Must add the following code to def _checkInput() in async_re.py for noneq (no exchange) binding to work correctly:
	self.exchange = True
	if self.keywords.get('RE_TYPE') is not None and self.keywords.get('RE_TYPE') == 'NONEQ':
		self.exchange = False
