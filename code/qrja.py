# This file contains the implementation of QRJA.

def QRJAL1GRB(m, n, a, b, y, w, Maxw = 1e6):
	# L1 QRJA, implemented using Gurobi, not used in the experiments.

	import gurobipy as gp
	solver = gp.Model()
	solver.setParam('OutputFlag', 0)

	objective = 0.0
	x = [solver.addVar(lb = 0, ub = Maxw, name=f"{i}") for i in range(n)]

	for i in range(m):
		d1 = solver.addVar(lb=0.0, ub=gp.GRB.INFINITY, name=f"d1 {i}")
		d2 = solver.addVar(lb=0.0, ub=gp.GRB.INFINITY, name=f"d2 {i}")
		solver.addConstr(d1 >= x[a[i]] - x[b[i]] - y[i])
		solver.addConstr(d2 >= x[b[i]] - x[a[i]] + y[i])
		objective += w[i] * d1 + w[i] * d2

	solver.setObjective(objective, gp.GRB.MINIMIZE)
	solver.optimize()

	return [x[i].X - x[0].X for i in range(n)]

def QRJAL1NetworkFlow(m, n, a, b, y, w, M = 1e6):
	# L1 QRJA, implemented using networkx, not used in the experiments.

	inty = [int(y[i] * M + 0.5) for i in range(m)]

	import networkx as nx

	G = nx.MultiDiGraph()
	G.add_nodes_from([i for i in range(n)])
	for i in range(m):
		if (a[i] != b[i]):
			G.add_edge(a[i], b[i], key=i, capacity=w[i], weight=-inty[i])
			G.add_edge(b[i], a[i], key=i, capacity=w[i], weight=inty[i])
	flow_cost, flow_dict = nx.network_simplex(G)

	f = [0 for i in range(m)]
	for i in range(m):
		if (a[i] != b[i]):
			f[i] += flow_dict[a[i]][b[i]][i]
			f[i] -= flow_dict[b[i]][a[i]][i]

	G = nx.MultiDiGraph()
	G.add_nodes_from([i for i in range(n + 1)])
	for i in range(n):
		G.add_edge(n, i, weight=0)
	for i in range(m):
		if (a[i] != b[i]):
			if (f[i] > -w[i]):
				G.add_edge(b[i], a[i], weight=inty[i])
			if (f[i] < w[i]):
				G.add_edge(a[i], b[i], weight=-inty[i])
	dist = nx.single_source_bellman_ford(G, source=n)[0]

	return [dist[i] / M for i in range(n)]

def QRJAL1(m, n, a, b, y, w, M = 1e6):
	# L1 QRJA, implemented using Gurobi and networkx.

	inty = [int(y[i] * M + 0.5) for i in range(m)]
		
	import gurobipy as gp
	solver = gp.Model()
	solver.setParam('OutputFlag', 0)

	objective = 0.0
	x = [0.0 for i in range(m)]
	inx  = [0.0 for i in range(n)]
	outx = [0.0 for i in range(n)]

	for i in range(m):
		x[i] = solver.addVar(lb=-w[i], ub=w[i], name=f"{i}")
		outx[a[i]] += x[i]
		inx[b[i]]  += x[i]
		objective += inty[i] * x[i]
	
	for i in range(n):
		solver.addConstr(inx[i] == outx[i])

	solver.setObjective(objective, gp.GRB.MAXIMIZE)
	solver.optimize()
	f = [x[i].X for i in range(m)]
	
	import networkx as nx
	G = nx.MultiDiGraph()
	G.add_nodes_from([i for i in range(n + 1)])
	for i in range(n):
		G.add_edge(n, i, weight=0)
	for i in range(m):
		if (a[i] != b[i]):
			if (f[i] > -w[i]):
				G.add_edge(b[i], a[i], weight=inty[i])
			if (f[i] < w[i]):
				G.add_edge(a[i], b[i], weight=-inty[i])
	dist = nx.single_source_bellman_ford(G, source=n)[0]

	return [dist[i] / M for i in range(n)]

def QRJAL2GRB(m, n, a, b, y, w, Maxw = 1e6):
	# L2 QRJA, implemented using Gurobi, not used in the experiments.

	import gurobipy as gp
	solver = gp.Model()
	solver.setParam('OutputFlag', 0)

	objective = 0.0
	x = [solver.addVar(lb = 0, ub = Maxw, name=f"{i}") for i in range(n)]

	for i in range(m):
		objective += w[i] * ((x[a[i]] - x[b[i]] - y[i]) ** 2)

	solver.setObjective(objective, gp.GRB.MINIMIZE)
	solver.optimize()

	return [x[i].X - x[0].X for i in range(n)]

def QRJAL2(m, n, a, b, y, w):
	# L2 QRJA, implemented using scipy.sparse.linalg.lsqr.

	import numpy as np
	from scipy.sparse import csr_matrix
	from scipy.sparse.linalg import lsqr

	r = np.zeros(m * 2)
	c = np.zeros(m * 2)
	d = np.zeros(m * 2)
	vb = np.zeros(m)

	for i in range(m):
		r[i * 2] = r[i * 2 + 1] = i
		c[i * 2] = a[i]
		c[i * 2 + 1] = b[i]
		d[i * 2] = np.sqrt(w[i])
		d[i * 2 + 1] = -np.sqrt(w[i])
		vb[i] = np.sqrt(w[i]) * y[i]

	A = csr_matrix((d, (r, c)), shape=(m, n))
	return lsqr(A, vb)[0]

def QRJALpBF(m, n, a, b, y, w, p, Maxw = 1e6):
	# Lp QRJA, not used in the experiments.
	# This is a slower implementation using Gurobi.

	import gurobipy as gp
	solver = gp.Model()
	solver.setParam('OutputFlag', 0)

	objective = 0.0
	x = [solver.addVar(lb = 0, ub = Maxw, name=f"{i}") for i in range(n)]

	for i in range(m):
		d1 = solver.addVar(lb=0.0, ub=gp.GRB.INFINITY, name=f"d1 {i}")
		d2 = solver.addVar(lb=0.0, ub=gp.GRB.INFINITY, name=f"d2 {i}")
		solver.addConstr(d1 >= x[a[i]] - x[b[i]] - y[i])
		solver.addConstr(d2 >= x[b[i]] - x[a[i]] + y[i])
		pd1 = solver.addVar(lb=0.0, ub=gp.GRB.INFINITY, name=f"pd1 {i}")
		pd2 = solver.addVar(lb=0.0, ub=gp.GRB.INFINITY, name=f"pd2 {i}")
		solver.addGenConstrPow(d1, pd1, p, options = "FuncPieces=-1 FuncPieceError=0.001")
		solver.addGenConstrPow(d2, pd2, p, options = "FuncPieces=-1 FuncPieceError=0.001")
		objective += w[i] * pd1 + w[i] * pd2

	solver.setObjective(objective, gp.GRB.MINIMIZE)
	solver.optimize()

	return [x[i].X - x[0].X for i in range(n)]

def QRJALp(m, n, a, b, y, w, p, Maxw = 1e6, eps = 1e-2, uppereps = 1.0):
	# Lp QRJA, not used in the experiments.
	# This is a faster implementation using Gurobi.

	def finished(x, y):
		return sum([(x[i] - y[i]) ** 2 for i in range(n)]) < eps
	
	def iteration(last):
		import gurobipy as gp
		solver = gp.Model()
		solver.setParam('OutputFlag', 0)

		objective = 0.0
		x = [solver.addVar(lb = 0, ub = Maxw, name=f"{i}") for i in range(n)]

		for i in range(m):
			lastd1 = max(last[a[i]] - last[b[i]] - y[i], 0.0)
			lastd2 = max(last[b[i]] - last[a[i]] + y[i], 0.0)
			d1 = solver.addVar(lb=0.0, ub=gp.GRB.INFINITY, name=f"d1 {i}")
			d2 = solver.addVar(lb=0.0, ub=gp.GRB.INFINITY, name=f"d2 {i}")
			solver.addConstr(d1 >= x[a[i]] - x[b[i]] - y[i])
			solver.addConstr(d2 >= x[b[i]] - x[a[i]] + y[i])
			if (lastd1 > eps):
				solver.addConstr(x[a[i]] - x[b[i]] - y[i] >= 0)
				dx1 = p * lastd1 ** (p - 1)
				dx2 = p * (p - 1) * lastd1 ** (p - 2)
				objective += w[i] * (dx1 * (d1 - lastd1) + dx2 / 2 * (d1 - lastd1) * (d1 - lastd1))
			elif (lastd2 > eps):
				solver.addConstr(x[b[i]] - x[a[i]] + y[i] >= 0)
				dx1 = p * lastd2 ** (p - 1)
				dx2 = p * (p - 1) * lastd2 ** (p - 2)
				objective += w[i] * (dx1 * (d2 - lastd2) + dx2 / 2 * (d2 - lastd2) * (d2 - lastd2))
			else:
				dx1 = p * eps ** (p - 1)
				dx2 = p * (p - 1) * eps ** (p - 2)
				objective += w[i] * (dx1 * d1 + dx2 / 2 * d1 * d1)
				objective += w[i] * (dx1 * d2 + dx2 / 2 * d2 * d2)

		solver.setObjective(objective, gp.GRB.MINIMIZE)
		solver.optimize()

		return [x[i].X - x[0].X for i in range(n)]
	
	last = [0.0 for i in range(n)]
	x = iteration(last)
	cnt = 0
	while not finished(x, last):
		last = x
		x = iteration(last)
		cnt = cnt + 1
		print(cnt)
	return x

def QRJA(m, n, a, b, y, w, p):
	if (p < 1):
		assert(False)

	if (p == 1):
		return QRJAL1(m, n, a, b, y, w)
	
	if (p == 2):
		return QRJAL2(m, n, a, b, y, w)

	return QRJALp(m, n, a, b, y, w, p)

def SubsampleQRJA(m, n, a, b, y, w, p, rate):
	# Import libraries
	import numpy as np
	import random

	# Subsampling
	subm = []
	for i in range(int(rate * m)):
		subm.append(random.randint(0, m - 1))
	suba = []
	subb = []
	suby = []
	subw = []
	for i in subm:
		suba.append(a[i])
		subb.append(b[i])
		suby.append(y[i])
		subw.append(w[i])

	# Run QRJA
	return QRJA(int(rate * m), n, suba, subb, suby, subw, p)