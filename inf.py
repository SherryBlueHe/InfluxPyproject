import pandas as pd
import argparse
import numpy as np
from influxdb import InfluxDBClient
brics = pd.read_csv("/Users/hoshang/Documents/infdb.csv", index_col=0);

#print(brics)
def read_data():
    with open('/Users/hoshang/Documents/infdb.csv') as f: #Input the name of your csv file here
        return [x.split(',') for x in f.readlines()[1:]]
def read_header():
    with open('/Users/hoshang/Documents/infdb.csv') as f: #Input the name of your csv file here
        return [x.split(',') for x in f.readlines()[:1]]

def main(host='localhost', port=8086):       #input your port number which has been set for influx
    """Instantiate the connection to the InfluxDB client."""
    user = 'hoshang'
    password = 'test'
    dbname = 'influxpy'
    # Temporarily avoid line protocol time conversion issues #412, #426, #431.
    protocol = 'json'

    client = InfluxDBClient(host, port, user, password, dbname)

    print("Create DataFrame");
    b=read_header();
    arr = np.array([b]);
    narr=np.delete(arr,0)
    length=len(narr);
    print(narr); # getting /n (new line?,why?)
    narr[length-1]=narr[length-1].replace("\n",""); #for some reason my final column is getting /n,
    #  I guess there is an issue with the csv file conversion, sub string /n replaced with blank(not efficient)
    print(narr); #removed /n
    print("Create database: " + dbname)
    client.create_database(dbname)

    a = read_data();
    j=0;
    for i in range(len(narr)):
        j=j+1;
        for metric in a:
            metric[j]=metric[j].replace("\n",""); # same as line 31
            influx_metric = [{
                'measurement': 'patients',
                'tags': {
                    'patient': narr[i]
                },
                'time': metric[0],
                'fields': {
                    'value': metric[j]
                }
            }]
            client.write_points(influx_metric)

    print("Read DataFrame")
    print(client.query("select * from patients")) # all values are now without /n

   # print("Delete database: " + dbname)
    #client.drop_database(dbname)


def parse_args():
    """Parse the args from main."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)

