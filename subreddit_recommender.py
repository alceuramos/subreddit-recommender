import sys
import subprocess

    
def main(subredit='cats'):
    program_list = ['run_reddit.py', 'run_user.py', 'data.py']

    for program in program_list:
        subprocess.call(['python', program, subredit])
        print("Finished:" + program)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()