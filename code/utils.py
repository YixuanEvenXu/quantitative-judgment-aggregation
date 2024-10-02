def run_qrja(cnt_matches, cnt_contestants, standings, p, rate = -1):
	# Import QRJA
	import sys
	from qrja import QRJA
	from qrja import SubsampleQRJA

	# Initialize predictions
	predictions = []

	# Initialize pairwise contest results
	a = []
	b = []
	y = []
	w = []

	# Predict results for each contest
	for i in range(cnt_matches):
		print(f"Predicting contest {i + 1} / {cnt_matches}", file=sys.stderr)
		contest = standings[i]

		# Run QRJA to get QRJA ratings
		if (rate == -1):
			x = QRJA(len(a), cnt_contestants, a, b, y, w, p)
		else:
			x = SubsampleQRJA(len(a), cnt_contestants, a, b, y, w, p, rate)

		# Make prediction for this contest
		prediction = []
		for row in contest:
			player = row['id']
			score  = row['score']
			prediction.append({'id' : player, 'score' : x[player]})
		predictions.append(prediction)
		
		# Update pairwise contest results
		for ti in range(len(contest)):
			for tj in range(ti):
				a.append(contest[ti]['id'])
				b.append(contest[tj]['id'])
				y.append(contest[ti]['score'] - contest[tj]['score'])
				w.append(1)
	
	# Return predictions
	return predictions

def run_mean(cnt_matches, cnt_contestants, standings):
	# Initialize predictions
	predictions = []
	
	# Initialize scores
	scoresum = [0 for i in range(cnt_contestants)]
	scorecnt = [0 for i in range(cnt_contestants)]
	
	# Predict results for each contest
	for contest in standings:
		
		# Make prediction for this contest
		prediction = []
		for row in contest:
			player = row['id']
			prediction.append({'id' : player, 'score' : scoresum[player] / scorecnt[player] if scorecnt[player] > 0 else -1})
		predictions.append(prediction)
		
		# Update scores
		for row in contest:
			player = row['id']
			score  = row['score']
			scoresum[player] += score
			scorecnt[player] += 1
	
	# Return predictions
	return predictions

def run_median(cnt_matches, cnt_contestants, standings):
	# Initialize predictions
	predictions = []
	
	# Initialize scores
	scores = [[] for i in range(cnt_contestants)]
	
	# Predict results for each contest
	for contest in standings:
		
		# Make prediction for this contest
		prediction = []
		for row in contest:
			player = row['id']
			prediction.append({'id' : player, 'score' : scores[player][len(scores[player]) // 2] if len(scores[player]) > 0 else -1})
		predictions.append(prediction)
		
		# Update scores
		for row in contest:
			player = row['id']
			score  = row['score']
			scores[player].append(score)
			scores[player].sort()
	
	# Return predictions
	return predictions

def run_zero(cnt_matches, cnt_contestants, standings):
	# Initialize predictions
	predictions = []

	# Predict results for each contest
	for contest in standings:
		
		# Make prediction for this contest
		prediction = []
		for row in contest:
			player = row['id']
			prediction.append({'id' : player, 'score' : 0})
		predictions.append(prediction)
	
	# Return predictions
	return predictions

def run_borda(cnt_matches, cnt_contestants, standings):
	# Initialize predictions
	predictions = []
	
	# Initialize scores
	scores = [0 for i in range(cnt_contestants)]
	
	# Predict results for each contest
	for contest in standings:
		
		# Make prediction for this contest
		prediction = []
		for row in contest:
			player = row['id']
			prediction.append({'id' : player, 'score' : scores[player]})
		predictions.append(prediction)
		
		# Update scores
		for i in range(len(contest)):
			player = contest[i]['id']
			scores[player] += 1 - 2 * (i - 1) / max((len(contest) - 1), 1)
	
	# Return predictions
	return predictions

def run_kemeny_young(cnt_matches, cnt_contestants, standings):
	import sys
	
	# Initialize predictions
	predictions = []
	
	# Initialize pairwise competition history
	wins = [[0 for j in range(cnt_contestants)] for i in range(cnt_contestants)]
	
	# Predict results for each contest
	for i in range(cnt_matches):
		print(f"Predicting contest {i + 1} / {cnt_matches}", file=sys.stderr)
		contest = standings[i]
		
		# Formulate Kemeny-Young as a mixed integer program and solve with Gurobi
		n = len(contest)
		import gurobipy as gp
		solver = gp.Model()
		solver.setParam('OutputFlag', 0)
		objective = 0.0
		x = [[solver.addVar(vtype=gp.GRB.BINARY) for i in range(n)] for j in range(n)]
		for i in range(n):
			for j in range(i):
				idi = contest[i]['id']
				idj = contest[j]['id']
				objective += wins[idi][idj] * x[i][j]
				objective += wins[idj][idi] * x[j][i]
				solver.addConstr(x[i][j] + x[j][i] == 1)
				for k in range(j):
					solver.addConstr(x[i][j] + x[j][k] + x[k][i] <= 2)
					solver.addConstr(x[i][k] + x[k][j] + x[j][i] <= 2)
		solver.setObjective(objective, gp.GRB.MAXIMIZE)
		solver.optimize()
		x = [[x[i][j].X if i != j else 0 for j in range(n)] for i in range(n)]
		
		# Make prediction for this contest
		prediction = []
		for i in range(n):
			player = contest[i]['id']
			score  = sum([x[i][j] for j in range(n)])
			prediction.append({'id' : player, 'score' : score})
		predictions.append(prediction)
		
		# Update pairwise competition history
		for i in range(n):
			for j in range(i):
				idi = contest[i]['id']
				idj = contest[j]['id']
				wins[idj][idi] += 1
	
	# Return predictions
	return predictions

def run_matrix_factorization(cnt_matches, cnt_contestants, standings, rank = 1, iters = 1000, lr = 1e-2):
	class MatrixFactorization:
		# Matrix factorization algorithm
		def __init__(self, n, m, rank, iters, gamma = lr):
			# Initialize the parameters
			#     n: number of rows
			#     m: number of columns
			#     rank: rank of the factorization
			#     iters: number of iterations
			#     gamma: learning rate
			self.n = max(n, rank + 1)
			self.m = max(m, rank + 1)
			self.rank = rank
			self.iters = iters
			self.gamma = gamma

			# Initialize the algorithm
			self.ready = False
			self.r = []
			self.c = []
			self.v = []
			self.M = 0.0
		
		def add_entry(self, i, j, v):
			# Add an known entry to the matrix
			self.r.append(i)
			self.c.append(j)
			self.v.append(v)
			self.M = max(self.M, abs(v))
		
		def train(self, debug = True):
			# Import packages
			import sys
			import numpy as np
			from scipy.sparse import csr_matrix
			from scipy.sparse.linalg import svds

			# Initialize the algorithm
			N = len(self.v)
			self.v = [self.v[i] / self.M for i in range(N)]
			self.A = csr_matrix((self.v, (self.r, self.c)), shape = (self.n, self.m))
			self.U, s, self.V = svds(self.A, k = self.rank)
			self.U = self.U @ np.diag(np.sqrt(s))
			self.V = np.diag(np.sqrt(s)) @ self.V

			# Use stochastic gradient descent to train the algorithm
			for it in range(self.iters):
				XY_d = self.U @ self.V
				XY_v = [XY_d[self.r[i], self.c[i]] for i in range(N)]
				XY_s = csr_matrix((XY_v, (self.r, self.c)), shape = (self.n, self.m))
				diff = self.A - XY_s
				loss = np.sum(diff.power(2)) / N
				dU = -2 * diff @ self.V.T
				dV = -2 * self.U.T @ diff
				self.U -= self.gamma * dU
				self.V -= self.gamma * dV
				if (debug and (it + 1) % 100 == 0):
					print(f"Epoch {it + 1} / {self.iters}, Loss = {loss}", file=sys.stderr)

			# Ready to predict
			self.ready = True
			self.ret = self.U @ self.V
		
		def predict(self, x):
			# Predict the performance of contestant x
			if (not self.ready):
				self.train()
			import numpy as np
			return np.mean(self.ret[:, x]) * self.M
	
	# Initialize predictions
	predictions = []

	# Predict results for each contest
	import sys
	import numpy as np
	for i in range(cnt_matches):
		print(f"Predicting contest {i + 1} / {cnt_matches}", file=sys.stderr)
		contest = standings[i]

		# Run matrix factorization
		algorithm = MatrixFactorization(i, cnt_contestants, rank, iters)
		for j in range(i):
			contestj = standings[j]
			for row in contestj:
				algorithm.add_entry(j, row['id'], row['score'])
		algorithm.train(True)

		# Make prediction for this contest
		prediction = []
		for row in contest:
			player = row['id']
			prediction.append({'id' : player, 'score' : algorithm.predict(player)})
		predictions.append(prediction)
	
	# Return predictions
	return predictions

def run_matrix_factorization_add(cnt_matches, cnt_contestants, standings, iters = 1000, lr = 1e-2):
	class MatrixFactorization:
		# Matrix factorization algorithm
		def __init__(self, n, m, iters, gamma = lr):
			# Initialize the parameters
			#     n: number of rows
			#     m: number of columns
			#     iters: number of iterations
			#     gamma: learning rate
			self.n = n
			self.m = m
			self.iters = iters
			self.gamma = gamma

			# Initialize the algorithm
			self.ready = False
			self.r = []
			self.c = []
			self.v = []
			self.M = 0.0
		
		def add_entry(self, i, j, v):
			# Add an known entry to the matrix
			self.r.append(i)
			self.c.append(j)
			self.v.append(v)
			self.M = max(self.M, abs(v))
		
		def train(self, debug = True):
			# Import packages
			import sys
			import numpy as np
			from scipy.sparse import csr_matrix
			from scipy.sparse.linalg import svds

			# Initialize the algorithm
			N = len(self.v)
			self.v = [self.v[i] / self.M for i in range(N)]
			self.A = csr_matrix((self.v, (self.r, self.c)), shape = (self.n, self.m))
			self.U = np.array([np.mean(self.A[i, :]) for i in range(self.n)])
			self.V = np.array([np.mean(self.A[:, j]) for j in range(self.m)])
			if (N == 0):
				ready = True
				return

			# Use stochastic gradient descent to train the algorithm
			for it in range(self.iters):
				XY_v = [self.U[self.r[i]] + self.V[self.c[i]] for i in range(N)]
				XY_s = csr_matrix((XY_v, (self.r, self.c)), shape = (self.n, self.m))
				diff = self.A - XY_s
				loss = np.sum(diff.power(2)) / N
				dU = -2 * np.sum(diff, axis = 1)
				dV = -2 * np.sum(diff, axis = 0)
				dU = np.array([dU[i, 0] for i in range(self.n)])
				dV = np.array([dV[0, i] for i in range(self.m)])
				self.U -= self.gamma * dU
				self.V -= self.gamma * dV
				if (debug and (it + 1) % 100 == 0):
					print(f"Epoch {it + 1} / {self.iters}, Loss = {loss}", file=sys.stderr)

			# Ready to predict
			self.ready = True
		
		def predict(self, x):
			# Predict the performance of contestant x
			if (not self.ready):
				self.train
			return self.V[x] * self.M
	
	# Initialize predictions
	predictions = []

	# Predict results for each contest
	import sys
	import numpy as np
	for i in range(cnt_matches):
		print(f"Predicting contest {i + 1} / {cnt_matches}", file=sys.stderr)
		contest = standings[i]

		# Run matrix factorization
		algorithm = MatrixFactorization(i, cnt_contestants, iters)
		for j in range(i):
			contestj = standings[j]
			for row in contestj:
				algorithm.add_entry(j, row['id'], row['score'])
		algorithm.train(True)

		# Make prediction for this contest
		prediction = []
		for row in contest:
			player = row['id']
			prediction.append({'id' : player, 'score' : algorithm.predict(player)})
		predictions.append(prediction)
	
	# Return predictions
	return predictions