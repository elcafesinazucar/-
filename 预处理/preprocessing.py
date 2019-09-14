import csv
import xlrd
import sys

filename = sys.argv[1]

from math import asin,sqrt,sin, pi,e

# 定义全局变量
rcp, fain, faic = (0.1314, 29, 35)

def handle_line(line):
    """
    把一行六个元素按逗号转化为 float 类型
    """
    p, rpp, fap_fain, fap_faic, sin_dilap, dilap = (float(i) for i in line.split(','))
    return p, rpp, fap_fain, fap_faic, sin_dilap, dilap
    
def gen_rows_by_line(p, rpp, fap_fain, fap_faic, sin_dilap, dilap):
    rps = fix_rps + [rpp]
    rpp = rps[-1]
    print(rps)
    for i in range(len(rps)):
        rp = rps[i]
        if rp <= rpp:
            asin_ = asin(2*sqrt(rp*rpp)/(rp+rpp)*fap_fain)*180/pi
            fai = asin_ + fain
            dila = asin(2*sqrt(rp*rpp)/(rp+rpp)*sin_dilap)*180/pi
        else:
            rp_minus_rpp_ = e ** (-((rp-rpp)/rcp) ** 2)
            fai = faic + rp_minus_rpp_ * fap_faic
            dila = dilap * rp_minus_rpp_
        yield [fai, dila, rp, p]

# ref log，使用前把代名称改成代码里需要的
with open(filename) as f:
    with open('sb.csv', mode='w') as sb_file:
        sb_writer = csv.writer(sb_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # 写入表头
        sb_writer.writerow(['fai', 'dila', 'rp', 'p'])
        
        # 批量写入行
        for line in f.readlines():
            sb_writer.writerows(list(gen_rows_by_line(*handle_line(line))))

