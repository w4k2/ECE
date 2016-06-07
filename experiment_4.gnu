#!/usr/local/bin/gnuplot
reset

load '_gnuconfigs/experiment_4.cfg'

file = 'results/experiment_4.csv'

set output 'plots/experiment_4.png'

plot  	file 	u ($1):(100*$2) w l ls 1 t ''
