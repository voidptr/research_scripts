## take extracted amplitudes from step 1, and calculate means and mann whitney u stats.
## step 2 in the pipeline.
## l

python run_combinatoric_scripts.py task_oscillation__output_differences_in_mean_and_mann_whitney_u_test.py "Echo" ../027/ ../027/27_Echo_Backbone__mann_whitney_u_stats__ mann_whitney_u_runlist.txt
python run_combinatoric_scripts.py task_oscillation__output_differences_in_mean_and_mann_whitney_u_test.py "Not" ../028/ ../028/28_Not_Backbone__mann_whitney_u_stats__ mann_whitney_u_runlist.txt
python run_combinatoric_scripts.py task_oscillation__output_differences_in_mean_and_mann_whitney_u_test.py "Nand" ../029/ ../029/29_Nand_Backbone__mann_whitney_u_stats__ mann_whitney_u_runlist.txt
python run_combinatoric_scripts.py task_oscillation__output_differences_in_mean_and_mann_whitney_u_test.py "And" ../030/ ../030/30_And_Backbone__mann_whitney_u_stats__ mann_whitney_u_runlist.txt
python run_combinatoric_scripts.py task_oscillation__output_differences_in_mean_and_mann_whitney_u_test.py "Orn" ../031/ ../031/31_Orn_Backbone__mann_whitney_u_stats__ mann_whitney_u_runlist.txt
python run_combinatoric_scripts.py task_oscillation__output_differences_in_mean_and_mann_whitney_u_test.py "Or" ../032/ ../032/32_Or_Backbone__mann_whitney_u_stats__ mann_whitney_u_runlist.txt
python run_combinatoric_scripts.py task_oscillation__output_differences_in_mean_and_mann_whitney_u_test.py "Andn" ../033/ ../033/33_Andn_Backbone__mann_whitney_u_stats__ mann_whitney_u_runlist.txt
python run_combinatoric_scripts.py task_oscillation__output_differences_in_mean_and_mann_whitney_u_test.py "Nor" ../034/ ../034/34_Nor_Backbone__mann_whitney_u_stats__ mann_whitney_u_runlist.txt
python run_combinatoric_scripts.py task_oscillation__output_differences_in_mean_and_mann_whitney_u_test.py "Xor" ../035/ ../035/35_Xor_Backbone__mann_whitney_u_stats__ mann_whitney_u_runlist.txt
python run_combinatoric_scripts.py task_oscillation__output_differences_in_mean_and_mann_whitney_u_test.py "Equ" ../036/ ../036/36_Equ_Backbone__mann_whitney_u_stats__ mann_whitney_u_runlist.txt

