import argparse
from multiprocessing import Process
import yaml

from aski.dash_files.app_callbacks import run_app
from aski.flask_servers.app import create_app, run_app_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('yaml_file',
                        help='YAML file that describes the NLP pipeline',
                        )
    parser.add_argument('-p', type=int, default=5001, required=False, help="defines port ot be used")

    args = parser.parse_args()

    with open(args.yaml_file, mode="rt", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    app = create_app(data)
    port = args.p

    p = Process(target=run_app, args=(data,port))
    p1 = Process(target=run_app_server, args=(app,))

    p.start()

    try: 
        p1.start()
        p1.join()
    except: 
        print("Flask server may already be running...")


    p.join()

