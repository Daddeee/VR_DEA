import pulp

class DEA:

	def __init__(self, inputs, outputs):
		assert inputs.shape[0] == outputs.shape[0]
		
		self.inputs = inputs
		self.outputs = outputs

		self.n = inputs.shape[0]
		self._n = range(self.n)

		self.s = outputs.shape[1]
		self._s = range(self.s)

		self.m = inputs.shape [1]
		self._m = range(self.m)


	def solve(self):
		status = {}
		efficiency = {}

		for i in self._n:
			prob = pulp.LpProblem("DMU_" + str(i), pulp.LpMaximize)

			u = pulp.LpVariable.dicts("u", self._s, lowBound=0)
			v = pulp.LpVariable.dicts("v", self._m, lowBound=0)
			
			# objective
			prob += pulp.LpAffineExpression([(u[s], self.outputs[i][s]) for s in self._s])
			
			# Set up constraints
			prob += pulp.LpAffineExpression([(v[m], self.inputs[i][m]) for m in self._m]) == 1,  "fix_denom_constraint"

			for j in self._n:
				prob += pulp.LpAffineExpression([(u[s], self.outputs[j][s]) for s in self._s]) - pulp.LpAffineExpression([(v[m], self.inputs[j][m]) for m in self._m]) <= 0, "DMU_constr_" + str(j)

			prob.solve()

			status[i] = pulp.LpStatus[prob.status]
			
			efficiency[i] = pulp.value(prob.objective)


		return status, efficiency




class CCR:

    def __init__(self, inputs, outputs):
        assert inputs.shape[0] == outputs.shape[0]
        
        self.inputs = inputs
        self.outputs = outputs

        self.n = inputs.shape[0]
        self._n = range(self.n)

        self.s = outputs.shape[1]
        self._s = range(self.s)

        self.m = inputs.shape [1]
        self._m = range(self.m)


    def solve(self):
        status = {}
        efficiency = {}

        for i in self._n:
            dp0 = pulp.LpProblem("dp0_DMU_" + str(i), pulp.LpMinimize)
            
            theta = pulp.LpVariable("theta")
            lambdas = pulp.LpVariable.dicts("lambda", self._n, lowBound=0)
            sminus = pulp.LpVariable.dicts("sminus", self._m, lowBound=0)
            splus = pulp.LpVariable.dicts("splus", self._s, lowBound=0)
            
            dp0 += theta

            for m in self._m:
                dp0 += theta*self.inputs[i][m] - pulp.LpAffineExpression([(lambdas[j], self.inputs[j][m]) for j in self._n]) - sminus[m] == 0
                
            for s in self._s:
                dp0 += pulp.LpAffineExpression([(lambdas[j], self.outputs[j][s]) for j in self._n]) - self.outputs[i][s] - splus[s] == 0

            dp0.solve()

            thetaopt = pulp.value(dp0.objective)

            dp1 = pulp.LpProblem("dp1_DMU_" + str(i), pulp.LpMaximize)
            
            lambdas = pulp.LpVariable.dicts("lambda", self._n, lowBound=0)
            sminus = pulp.LpVariable.dicts("sminus", self._m, lowBound=0)
            splus = pulp.LpVariable.dicts("splus", self._s, lowBound=0)
            
            dp1 += pulp.LpAffineExpression([(sminus[m], 1) for m in self._m] + [(splus[s], 1) for s in self._s])
            for m in self._m:
                dp1 += thetaopt*self.inputs[i][m] - pulp.LpAffineExpression([(lambdas[j], self.inputs[j][m]) for j in self._n] + [(sminus[m], -1)])  == 0
            for s in self._s:
                dp1 += pulp.LpAffineExpression([(lambdas[j], self.outputs[j][s]) for j in self._n]) + [(splus[s], -1)] - self.outputs[i][s] == 0
            
            dp1.solve()

            status[i] = pulp.LpStatus[dp1.status]
            
            efficiency[i] = thetaopt


        return status, efficiency




class BCC:
    
    def __init__(self, inputs, outputs):
        assert inputs.shape[0] == outputs.shape[0]
        
        self.inputs = inputs
        self.outputs = outputs

        self.n = inputs.shape[0]
        self._n = range(self.n)

        self.s = outputs.shape[1]
        self._s = range(self.s)

        self.m = inputs.shape [1]
        self._m = range(self.m)


    def solve(self):
        status = {}
        efficiency = {}

        for i in self._n:
            dp0 = pulp.LpProblem("dp0_DMU_" + str(i), pulp.LpMinimize)
            
            theta = pulp.LpVariable("theta")
            lambdas = pulp.LpVariable.dicts("lambda", self._n, lowBound=0)
            sminus = pulp.LpVariable.dicts("sminus", self._m, lowBound=0)
            splus = pulp.LpVariable.dicts("splus", self._s, lowBound=0)
            
            dp0 += theta

            dp0 += pulp.LpAffineExpression([(lambdas[j], 1) for j in self._n]) == 1

            for m in self._m:
                dp0 += theta*self.inputs[i][m] - pulp.LpAffineExpression([(lambdas[j], self.inputs[j][m]) for j in self._n]) - sminus[m] == 0
                
            for s in self._s:
                dp0 += pulp.LpAffineExpression([(lambdas[j], self.outputs[j][s]) for j in self._n]) - self.outputs[i][s] - splus[s] == 0

            dp0.solve()

            thetaopt = pulp.value(dp0.objective)

            dp1 = pulp.LpProblem("dp1_DMU_" + str(i), pulp.LpMaximize)
            
            lambdas = pulp.LpVariable.dicts("lambda", self._n, lowBound=0)
            sminus = pulp.LpVariable.dicts("sminus", self._m, lowBound=0)
            splus = pulp.LpVariable.dicts("splus", self._s, lowBound=0)
            
            dp1 += pulp.LpAffineExpression([(sminus[m], 1) for m in self._m] + [(splus[s], 1) for s in self._s])
            for m in self._m:
                dp1 += thetaopt*self.inputs[i][m] - pulp.LpAffineExpression([(lambdas[j], self.inputs[j][m]) for j in self._n] + [(sminus[m], -1)])  == 0
            for s in self._s:
                dp1 += pulp.LpAffineExpression([(lambdas[j], self.outputs[j][s]) for j in self._n]) + [(splus[s], -1)] - self.outputs[i][s] == 0
            
            dp1.solve()

            status[i] = pulp.LpStatus[dp1.status]
            
            efficiency[i] = thetaopt


        return status, efficiency