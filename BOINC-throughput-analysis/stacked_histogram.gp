set terminal png font "Helvetica" 12
 
set output '2014.11.18-2014.11.25.png'
set key right

set grid y
set style data histograms
set style histogram rowstacked
set boxwidth 0.5
set style fill solid 1.0 border -1
set ytics 10 nomirror
set yrange [:1300]
set ylabel "Number of Completed Jobs"
set xlabel "Date"
set ytics 100
 
plot '2014.11.18-2014.11.25.dat' using 2 t "Success" lc rgb '#E0FFFF', '' using 3:xtic(1) t "Failed" lc rgb '#FFC0CB'
