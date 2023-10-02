def gen(user, run_numbers):
    f = open("download.sh", "w")
    for i in run_numbers:
        f.write("scp " + user + "@lxplus.cern.ch:/eos/experiment/ntof/processing/official/done/run" +
                str(i) + ".root" + " " + ".\n")
    f.close()
