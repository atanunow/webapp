from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server

import pickle
import numpy as np
# model = pickle.load(open('regression_rf.pkl', 'rb'))
app = Flask(__name__)


def bmicalculator():
    height = input("Please enter the height in cm", type=FLOAT)
    weight = input("Please enter the weight in Kg", type=FLOAT)

    bmi = weight / (height / 100) ** 2

    bmi_output = [(16, 'Severely underweight'), (18.5, 'Underweight'),
                  (25, 'Normal'), (30, 'Overweight'),
                  (35, 'Moderately obese'), (float('inf'), 'Severely obese')]

    for tuple1, tuple2 in bmi_output:
        if bmi <= tuple1:
            put_text('Your BMI is :%.1f and the person is :%s' % (bmi, tuple2))
            break


# if __name__ == '__main__':
#     bmicalculator()

app.add_url_rule('/tool', 'webio_view', webio_view(bmicalculator),
            methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(bmicalculator, port=args.port)