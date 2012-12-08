set xdata time
set timefmt "%Y-%m-%d"
set format x "%Y-%m"
set datafile separator " "
set terminal png
set output "logon_plot.png"
plot "logon_output.dat" using 1:2 with lines;
