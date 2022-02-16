from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server
import numpy as np
import itertools

app = Flask(__name__)
import warnings
warnings.filterwarnings('ignore')


def calculate_rewards(score,rule,inv):
    score_rule = {x:y**rule for x,y in score.items()}
    cal_share = {x:(len(list(score.keys()))*inv)*(y/np.sum(list(score_rule.values()))) for x,y in score_rule.items()}
    score_rule_dev = len(list(score.keys()))*inv - sum(cal_share.values())

    if score_rule_dev > 0:
        cal_share[min(score, key=score.get)] += score_rule_dev
    elif  score_rule_dev < 0:
        cal_share[max(score, key=score.get)] -= score_rule_dev
    else:
        pass

    profit_loss = {x:(y-inv) for x,y in cal_share.items()}
    neg = {x:y for x,y in sorted(profit_loss.items(), key=lambda item: item[1], reverse=False) if y<0}
    pos = {x:y for x,y in sorted(profit_loss.items(), key=lambda item: item[1], reverse=True) if y>0}
    pos_comb = list(itertools.product(list(neg.keys()), list(pos.keys())))

    payment = {}
    for i in pos_comb:
        if np.abs(profit_loss[i[0]]) <= np.abs(profit_loss[i[1]]):
            payment['{} pays {}'.format(i[0], i[1])] = np.abs(profit_loss[i[0]])
            profit_loss[i[1]] = np.abs(profit_loss[i[1]]) - np.abs(profit_loss[i[0]])
            profit_loss[i[0]] = np.abs(profit_loss[i[0]]) - np.abs(profit_loss[i[0]])

        elif np.abs(profit_loss[i[0]]) > np.abs(profit_loss[i[1]]):
            payment['{} pays {}'.format(i[0], i[1])] = np.abs(profit_loss[i[1]])
            profit_loss[i[0]] = np.abs(profit_loss[i[0]]) - np.abs(profit_loss[i[1]])
            profit_loss[i[1]] = np.abs(profit_loss[i[1]]) - np.abs(profit_loss[i[1]])
        else:
            print("Eh! you didn't code efficiently")
    payment = {x: np.round(y,2) for x, y in payment.items() if y > 0}

    return payment

def check_form(data):
    # for checking Name
    if data['atanu'] <= 0:
        return ('atanu', 'Invalid atanu score!')
    if data['bhaskar'] <= 0:
        return ('bhaskar', 'Invalid bhaskar score!')
    if data['rajanikanta'] <= 0:
        return ('atanu', 'Invalid rajanikanta score!')

    put_table([['ATANU','BHASKAR','RAJANIKANTA'],[data['atanu'],data['bhaskar'],data['rajanikanta']]])
    check = checkbox(options=['Scores are correct'])
    if check:
        # Create a radio button
        Contribution = slider("Contribution",min_value=0,max_value=100,step=10)
        Rule = radio("Rule", options=['Linear', 'Square', 'Cube'], required=True)
        power_dict = {'Linear':1, 'Square':2, 'Cube':3}
        score_dict = {'ATANU':data['atanu'],'BHASKAR':data['bhaskar'],'RAJANIKANTA':data['rajanikanta']}
        put_text("\nContribution is :",Contribution)
        put_text("Rule is :", Rule)
        for k, v in calculate_rewards(score_dict,power_dict[Rule],Contribution).items():
            put_text(k, v)
        # put_text(calculate_rewards(score_dict,power_dict[Rule],Contribution))

# Taking input from the user
data = input_group("Fill informations:",[
    input('Atanu', name='atanu', type=NUMBER,required=True, PlaceHolder="@atanuscore"),
    input('Bhaskar', name='bhaskar', type=NUMBER,required=True, PlaceHolder="@bhaskarscore"),
    input('Rajanikanta', name='rajanikanta', type=NUMBER,required=True, PlaceHolder="@rajaniscore")],validate=check_form, cancelable=True)



app.add_url_rule('/tool', 'webio_view', webio_view(check_form),
            methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    start_server(check_form, port=8080, debug=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(check_form, port=args.port)