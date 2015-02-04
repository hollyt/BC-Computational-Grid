#!/usr/bin/gnuplot

# Usage: gnuplot -e "outfile='<outputfile_path.png>'; infile='<inputfile_path.dat>'" stacked_histogram.gp

set terminal png font "Helvetica" 12

if (!exists("outfile")) print "Please enter the path of desired output file.\nUsage: gnuplot -e \"outfile='<outputfile_path.png>'; infile='<inputfile_path.dat>'\" stacked_histogram.gp
set output outfile
 
set key outside top right
set grid y
set style data histograms
set style histogram rowstacked
set boxwidth 0.5
set style fill solid 1.0 border -1
set ytics 10 nomirror
set ylabel "Number of Completed Jobs"
set xlabel "Date"
set ytics 1000 nomirror

if (!exists("infile")) print "Please enter the path of your input file.\nUsage: gnuplot -e \"outfile='<outputfile_path.png>'; infile='<inputfile_path.dat>'\" stacked_histogram.gp
plot infile  using 2 t "Success" lc rgb '#E0FFFF', '' using 3:xtic(1) t "Failed" lc rgb '#FFC0CB'
