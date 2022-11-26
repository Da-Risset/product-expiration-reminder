import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


def main():
    for i in range(4000, 4429):
        os.system("python run.py -i dicts/{}.txt --output_dir data/{} -c 100 -k 15 -rk -bl 3 -rbl -tc '#000000,#888888' -f 64".format(i, i))
        print("Done with {}".format(i))

if __name__ == "__main__":
    main()