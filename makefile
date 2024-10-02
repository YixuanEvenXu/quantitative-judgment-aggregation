plotmain: plot/main.py
	python3 plot/main.py chess
	python3 plot/main.py marathon
	python3 plot/main.py f1
	python3 plot/main.py f1-core
	python3 plot/main.py codeforces
	python3 plot/main.py codeforces-core
	python3 plot/main.py cross-tables

plotmf: plot/mf.py
	python3 plot/mf.py chess
	python3 plot/mf.py marathon
	python3 plot/mf.py f1
	python3 plot/mf.py f1-core
	python3 plot/mf.py codeforces
	python3 plot/mf.py codeforces-core
	python3 plot/mf.py cross-tables

plotsubsample: plot/subsample.py 
	python3 plot/subsample.py chess
	python3 plot/subsample.py marathon
	python3 plot/subsample.py f1
	python3 plot/subsample.py f1-core
	python3 plot/subsample.py codeforces
	python3 plot/subsample.py codeforces-core
	python3 plot/subsample.py cross-tables

plotovertime: plot/overtime.py 
	python3 plot/overtime.py chess
	python3 plot/overtime.py marathon
	python3 plot/overtime.py f1
	python3 plot/overtime.py f1-core
	python3 plot/overtime.py codeforces
	python3 plot/overtime.py codeforces-core
	python3 plot/overtime.py cross-tables

plotentrywise: plot/entrywise.py 
	python3 plot/entrywise.py chess
	python3 plot/entrywise.py marathon
	python3 plot/entrywise.py f1
	python3 plot/entrywise.py f1-core
	python3 plot/entrywise.py codeforces
	python3 plot/entrywise.py codeforces-core
	python3 plot/entrywise.py cross-tables

analysis: code/analysis.py
	python3 code/analysis.py chess
	python3 code/analysis.py marathon
	python3 code/analysis.py f1
	python3 code/analysis.py f1-core
	python3 code/analysis.py codeforces
	python3 code/analysis.py codeforces-core
	python3 code/analysis.py cross-tables

main: code/main.py 
	python3 code/main.py chess > logs/main/chess.log
	python3 code/main.py marathon > logs/main/marathon.log
	python3 code/main.py f1 > logs/main/f1.log
	python3 code/main.py f1-core > logs/main/f1-core.log
	python3 code/main.py codeforces > logs/main/codeforces.log
	python3 code/main.py codeforces-core > logs/main/codeforces-core.log
	python3 code/main.py cross-tables > logs/main/cross-tables.log

subsample: code/subsample.py
	python3 code/subsample.py chess > logs/subsample/chess.log
	python3 code/subsample.py marathon > logs/subsample/marathon.log
	python3 code/subsample.py f1 > logs/subsample/f1.log
	python3 code/subsample.py f1-core > logs/subsample/f1-core.log
	python3 code/subsample.py codeforces > logs/subsample/codeforces.log
	python3 code/subsample.py codeforces-core > logs/subsample/codeforces-core.log
	python3 code/subsample.py cross-tables > logs/subsample/cross-tables.log

overtime: code/overtime.py
	python3 code/overtime.py chess > logs/overtime/chess.log
	python3 code/overtime.py marathon > logs/overtime/marathon.log
	python3 code/overtime.py f1 > logs/overtime/f1.log
	python3 code/overtime.py f1-core > logs/overtime/f1-core.log
	python3 code/overtime.py codeforces > logs/overtime/codeforces.log
	python3 code/overtime.py codeforces-core > logs/overtime/codeforces-core.log
	python3 code/overtime.py cross-tables > logs/overtime/cross-tables.log

entrywise: code/entrywise.py
	python3 code/entrywise.py chess > logs/entrywise/chess.log
	python3 code/entrywise.py marathon > logs/entrywise/marathon.log
	python3 code/entrywise.py f1 > logs/entrywise/f1.log
	python3 code/entrywise.py f1-core > logs/entrywise/f1-core.log
	python3 code/entrywise.py codeforces > logs/entrywise/codeforces.log
	python3 code/entrywise.py codeforces-core > logs/entrywise/codeforces-core.log
	python3 code/entrywise.py cross-tables > logs/entrywise/cross-tables.log

zero: code/zero.py
	python3 code/zero.py chess > logs/zero/chess.log
	python3 code/zero.py marathon > logs/zero/marathon.log
	python3 code/zero.py f1 > logs/zero/f1.log
	python3 code/zero.py f1-core > logs/zero/f1-core.log
	python3 code/zero.py codeforces > logs/zero/codeforces.log
	python3 code/zero.py codeforces-core > logs/zero/codeforces-core.log
	python3 code/zero.py cross-tables > logs/zero/cross-tables.log