#!/usr/bin/env python3
# Import python libraries
import cv2
import copy
import os
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from itertools import chain
import os.path, time
import re
from scipy import stats
from itertools import chain
from statistics import mean
import pandas as pd
from sklearn.metrics import mean_squared_error
import seaborn as sns

sns.set_theme()

total_table = []
beacon_count = 0

col_amount = 6

drug_names = [['111'], ['1112', '111_2'], ['113'], ['1132', '113_2'], ['A-1155463'], ['A-1210477'], ['ABBVIE1'],
              ['ABBVIE10'], ['ABBVIE11'], ['ABBVIE12'], ['ABBVIE13'], ['ABBVIE14'], ['ABBVIE15'], ['ABBVIE16'],
              ['ABBVIE2'], ['ABBVIE3'], ['ABBVIE4'], ['ABBVIE5'], ['ABBVIE6'], ['ABBVIE7'], ['ABBVIE8'], ['ABBVIE9'],
              ['ABT-199', 'VEN'], ['ADAVOSERTIB'], ['ALISERTIB', 'Ali', 'ali', 'alisertib', 'Alisertib'],
              ['AR-A014418'], ['AR-A014418_1'], ['ASO'], ['ASO_CONTROL', 'ASO CONTROL'],
              ['ASO_CONTROL1', 'ASO CONTROL1'], ['ASO_CONTROL2', 'ASO CONTROL2'], ['ASO_IRF4_1', 'ASO IRF4(1)'],
              ['ASO_IRF4_2', 'ASO IRF4(2)'], ['ASO_IRF4x2', 'ASO IRF4x2'], ['ASO_PYK2', 'ASO PYK2', 'PYK2 ASO'],
              ['ASO_STAT3', 'ASO STAT3', 'STAT3 ASO'], ['AZ-628'], ['AZD1208', 'ASD1208'], ['AZD1480'], ['AZD7762'],
              ['BARASERTIB'], ['BARASERTIB_1'], ['BAY1816032'], ['BAY1816032_1'],
              ['BI2536', 'BI2536 ', 'Bl2536', 'Bl2536 '], ['BMS-265246'], ['BMS-265246(high)'], ['BMS-265246(low)'],
              ['BMS-265246_1'], ['BMS754807', 'BMS-754807', 'BMS754807 '], ['BMS777607'], ['BORTEZOMIB_BAD'],
              ['BTZ', 'BORTEZOMIB', 'Bortezomib'], ['BTZ(24h)', '24h+BTZ'], ['BTZ1', 'BORTEZOMIB1'],
              ['BTZ2', 'BORTEZOMIB2'], ['BTZ3', 'BORTEZOMIB3'], ['BTZ4', 'BORTEZOMIB4'], ['BTZ5', 'BORTEZOMIB5'],
              ['BTZ6', 'BORTEZOMIB6'], ['BTZ7', 'BORTEZOMIB7'], ['BTZ8', 'BORTEZOMIB8'], ['BTZ_1'], ['CB2'],
              ['CEP-33779'], ['CEP-33779_1'], ['CFZ', 'CARFILZOMIB', 'Carfilzomib', 'CRAFILZOMIB'],
              ['CFZ1', 'CARFILZOMIB1'], ['CFZ2', 'CARFILZOMIB2'], ['CFZ3', 'CARFILZOMIB3'], ['CFZ4', 'CARFILZOMIB4'],
              ['CFZ5', 'CARFILZOMIB5'], ['CFZ6', 'CARFILZOMIB6'], ['CFZ7', 'CARFILZOMIB7'], ['CFZ70', 'CARFILZOMIB70'],
              ['CFZ8', 'CARFILZOMIB8'], ['CFZ_1'], ['CFZ_2'], ['CFZ_3'], ['CFZ_4'], ['CFZ_5'], ['CFZ_6'], ['CFZ_7'],
              ['CFZ_8'], ['CGP-60474'], ['CISPLATINUM', 'CIS'], ['CLE'], ['COBIMETINIB', 'COB'], ['COLCHICINE'],
              ['CONTROL'], ['CONTROL1'], ['CONTROL2'], ['CONTROL3'], ['CONTROL4'], ['CONTROL5'], ['CONTROL6'],
              ['CONTROL7'], ['CONTROL_1'], ['CONTROL_10'], ['CONTROL_11'], ['CONTROL_12'], ['CONTROL_13'],
              ['CONTROL_14'], ['CONTROL_15'], ['CONTROL_16'], ['CONTROL_17'], ['CONTROL_18'], ['CONTROL_19'],
              ['CONTROL_2'], ['CONTROL_20'], ['CONTROL_21'], ['CONTROL_22'], ['CONTROL_23'], ['CONTROL_24'],
              ['CONTROL_3'], ['CONTROL_4'], ['CONTROL_5'], ['CONTROL_6'], ['CONTROL_7'], ['CONTROL_8'], ['CONTROL_9'],
              ['CP-724714'], ['CP43'], ['CP43_1'], ['CPD22', 'Cpd22'], ['CPD22_1'],
              ['CRIZOTINIB', 'crizotinib', 'Crizotinib', 'rizotinib'], ['CURCUMIN'], ['CYCLOPHOSPHAMIDE', 'CYC'],
              ['DABRAFENIB', 'Da', 'da', 'Dabrafeni', 'Dabrafenib', 'dabrafenib'], ['DARATUMUMAB', 'DAR'],
              ['DARATUMUMAB-80C'], ['DARATUMUMAB-80F'], ['DASATINIB', 'Dasatanib', 'dasatinib', 'Dasatinib'],
              ['DEFACTINIB', 'DEF', 'Defa', 'Defactinib', 'DEFACTINIB(VS6063)', 'Defactinib(VS-6063)',
               'Defactinib (VS-6063)'], ['DEFACTINIB1'], ['DEFACTINIB2'], ['DEFACTINIB3'],
              ['DEX', 'Dexametha', 'Dexamethasone', 'DEXAMETHASONE'], ['DEX2'], ['DINACICLIB', 'Dinaciclib'],
              ['DINACICLIB_1'], ['DMSO'], ['DMSO2'], ['DORSOMORPHIN'], ['DORSOMORPHIN_1'], ['DOVITINIB'],
              ['DOX', 'ADR', 'Adriamycin', 'Adriamycin (Dox)', 'Adriamy', 'ADRIAMYCIN', 'Doxorubi', 'Doxorubicin',
               'DOXORUBICIN'], ['DOX1', 'ADR1', 'ADRIAMYCIN1'], ['DOX2', 'ADR2', 'ADRIAMYCIN2'],
              ['DOX3', 'ADR3', 'ADRIAMYCIN3'], ['DS'], ['DUMMY1'], ['DUMMY10'], ['DUMMY11'], ['DUMMY12'], ['DUMMY13'],
              ['DUMMY14'], ['DUMMY15'], ['DUMMY16'], ['DUMMY2'], ['DUMMY3'], ['DUMMY4'], ['DUMMY5'], ['DUMMY6'],
              ['DUMMY7'], ['DUMMY8'], ['DUMMY9'], ['ELEVENOSTAT'], ['ELOTUZUMAB'], ['EN460'], ['ENZASTAURIN'],
              ['ENZASTAURIN_1'], ['ERLOTINIB', 'Erlotinib'], ['ETOPOSIDE'], ['F8'], ['FOR'], ['FOR10'], ['FOR2'],
              ['FOR28'], ['FOR29'], ['FRAX597'], ['FRAX597_1'], ['FXM'], ['GDC-0980'], ['GGTI', 'GGT'], ['GGTI(SIM)'],
              ['GGTI2'], ['GSK461364'], ['GSK461364_1'], ['HDAC11 ASO'], ['HP9060'], ['HSP90'], ['I-BET-762'],
              ['IBRUTINIB', 'Ibrutinib', 'ibrutinib'],
              ['IDELALISIB', 'idealisib', 'Idelali', 'idelali', 'idelalisib', 'Idelalsib', 'Idelalisib', 'IDEALISIB'],
              ['INCB054329'], ['INK128', 'INK 128'], ['INK128_1'], ['IRAK1-4(INHIBITOR)407601'],
              ['IRAK1-4(INHIBITOR)PF06650833'], ['IRF4 ASO-1'], ['IRF4 ASO-2'], ['ISOTYPE'],
              ['IXAZOMIB', 'IXAZUMAB', 'IXAZUMIB', 'IXA'], ['JNK-IN-8', 'JNK-IN-8 (specific)'], ['JNK-IN-8_1'], ['JQ1'],
              ['KPT', 'KPT330', 'KPT-330', 'KPT330 (Selinexor)'], ['KPT-DEX-BTZ'], ['KPT-DEX-DOX'],
              ['KPT-DEX-ELOTUZUMAB'], ['KPT1', 'KPT(1)'], ['KPT2'], ['LCL161'],
              ['LEN', 'LENALIDOMIDE', 'Lenalidomide', 'REVLIMID'], ['LINIFANIB', 'Linifanib', 'linifanib'], ['LJI308'],
              ['LJI308_1'], ['LOSMAPIMOD'], ['LOSMAPIMOD_1'], ['LY2584702'], ['LY2584702_1'], ['LY2603618'],
              ['MA7-038'], ['MARK-INHIBITOR', 'MARK_INHIBITOR', 'MARK INHIBITOR'], ['MARK3'], ['MARK3_1'],
              ['ME-POMALIDOMIDE'], ['MEL', 'Mel', 'MELPHALAN', 'Melphalan'], ['MEL1', 'MELPHALAN1'],
              ['MEL2', 'MELPHALAN2'], ['MEL3', 'MELPHALAN3'], ['MEL4', 'MELPHALAN4'], ['MEL5', 'MELPHALAN5'],
              ['MEL6', 'MELPHALAN6'], ['MEL7', 'MELPHALAN7'], ['MEL8', 'MELPHALAN8'], ['MK2206', 'MK-2206'],
              ['MK2206_1'], ['MOMELOTINIB', 'Momelotinib', 'momelotinib'],
              ['MOTESANIB', 'Mote', 'mote', 'motesanib', 'Motesanib'], ['MTI101', 'MT101', 'MTI-101'],
              ['MTI1012', 'MTI-1012'], ['MTX'], ['MYC'], ['NICLOSAMIDE'], ['NU-7441'], ['NU-7441_1'], ['NVP2'], ['ONX'],
              ['OPR', 'OPROZ', 'Oprozomib'], ['OPR2', 'OPROZ2'], ['OTSSP167'],
              ['PALBOCICLIB', 'PABLOCICLIB', 'Palbo', 'palbo', 'palbociclib', 'Palbociclib'],
              ['PANOBINOSTAT', 'PAN', 'PANO', 'Panobino', 'Panobinostat'], ['PANOBINOSTAT1'], ['PANOBINOSTAT2', 'PAN2'],
              ['PANOBINOSTAT3'], ['PDI'], ['POM', 'POMALIDOMIDE', 'Pomalidomide'], ['POM2'],
              ['PONATINIB', 'Ponatinib', 'ponatinib'], ['PREXASERTIB', 'PRX'], ['PYRVINIUM'], ['QST', 'Qui'], ['QST2'],
              ['QUISINOSTAT', 'Quisinostat'], ['R406'], ['R406_1'], ['RABUSERTIB'], ['RABUSERTIB_1'],
              ['RALIMETINIB', 'Ralimetinib', 'ralimetinib'], ['RICOLINOSTAT', 'ACY-1215', 'ROCILINOSTAT'],
              ['RUXOLITINIB', 'Ruxolitinib', 'ruxolitinib'], ['S63845'], ['SARACATINIB'], ['SARACATINIB_1'],
              ['SCH772984'], ['SCH772984_1'], ['SELUMETINIB', 'elumetinib', 'selumetinib', 'Selumetinib'],
              ['SILMITASERTIB'], ['SILMITASERTIB_1'], ['SNS-032'], ['SORAFENIB'], ['SORAFENIB_1'],
              ['SR3029', 'SR-3029'], ['SR30292'], ['SR3029_2'], ['SR4835'], ['SR5037'], ['TAI-1'], ['TAI-1_1'],
              ['TGR-1202'], ['THZ1'], ['TOZASERTIB', 'Toza', 'toza', 'tozasertib', 'Tozasertib'],
              ['TRAMETINIB', 'Trametinib', 'trametinib'], ['UMI-77'], ['VANDETANIB', 'Vandetanib'], ['VE-822'],
              ['VE-822_1'], ['VEMURAFENIB', 'emurafenib', 'vemurafenib', 'Vemurafenib'], ['VINCRISTINE'],
              ['VOLASERTIB', 'Volasertib', 'VOL'], ['VOLASERTIB_1'], ['VOLASERTIB_2'], ['VOLASERTIB_3'],
              ['VOLASERTIB_4'], ['VOLASERTIB_5'], ['VOLASERTIB_6'], ['VOLASERTIB_7'], ['VOLASERTIB_8'],
              ['VS4718', 'VS-4718'], ['VX745']]
pt_s_dir = [["/home/qibing/disk_m2/",
             ["Pt280_SOCCO", "Pt281_SOCCO", "Pt282_SOCCO", "Pt283_SOCCO", "Pt285_SOCCO", "Pt290_SOCCO", "Pt291_SOCCO",
              "Pt292_SOCCO", "Pt293_SOCCO", "Pt294_SOCCO", "Pt297_SOCCO", "Pt298_SOCCO", "Pt299_SOCCO", "Pt300_SOCCO",
              "Pt301_SOCCO", "Pt303_SOCCO", "Pt304_SOCCO", "Pt306_SOCCO_SPORE", "Pt307_SOCCO_SPORE",
              "Pt315_SOCCO_SPORE", "Pt421_SOCCO", "Pt422_SOCCO", "Pt423_SOCCO", "Pt426_SOCCO", "Pt428_SOCCO"]],
            ["/home/qibing/disk_m1/",
             ["Pt315_SOCCO_SPORE", "Pt323_SOCCO", "Pt325_SOCCO", "Pt348_SOCCO", "Pt373_SOCCO", "Pt375_SOCCO",
              "Pt380_SOCCO", "Pt382_SOCCO", "Pt386_SOCCO", "Pt387_SOCCO", "Pt388_SOCCO", "Pt389_SOCCO", "Pt390_SOCCO",
              "Pt392_SOCCO", "Pt393_SOCCO", "Pt394_SOCCO", "Pt395_SOCCO", "Pt397_SOCCO", "Pt398_SOCCO", "Pt400_SOCCO",
              "Pt401_SOCCO", "Pt403_SOCCO", "Pt409_SOCCO", "Pt415_SOCCO", "Pt419_SOCCO"]],
            ["/home/qibing/disk_16t/qibing/",
             ["Pt170", "Pt171", "Pt174", "Pt176", "Pt177", "Pt178", "Pt180", "Pt181", "Pt182", "Pt184", "Pt186",
              "Pt187", "Pt193", "Pt196", "Pt198", "Pt199", "Pt200", "Pt201", "Pt203", "Pt204", "Pt205", "Pt206",
              "Pt207", "Pt210", "Pt211", "Pt212", "Pt213", "Pt219", "Pt220", "Pt222", "Pt223", "Pt224", "Pt226",
              "Pt227", "Pt229", "Pt230", "Pt235", "Pt236", "Pt238", "Pt242"]]]

# pt_sel = ['Pt174', 'Pt180', 'Pt181', 'Pt196', 'Pt199', 'Pt210', 'Pt220', 'Pt224', 'Pt230', 'Pt298_SOCCO', 'Pt323_SOCCO', 'Pt400_SOCCO', 'Pt415_SOCCO']
drugs = drug_sel = ['BTZ', 'DEX', 'IXAZOMIB', 'PANOBINOSTAT', 'POM', 'CFZ', 'LEN', 'DARATUMUMAB']
drug_sel = ['BORTEZOMIB','IXAZOMIB','PANOBINOSTAT','CARFILZOMIB','DEXAMETHASONE','POMALIDOMIDE','LENALIDOMIDE','DARATUMUMAB']
# drugs = drug_sel = ['BTZ','DEX','IXAZOMIB','PANOBINOSTAT','POM']

path_di_0 = "/home/qibing/disk_16t/qibing/output/"
path_di = [path_di_0]
out_path = "/home/qibing/disk_16t/qibing/output/result/plot_individual_line/"

os.makedirs(out_path, exist_ok=True)
print(out_path)

processes = []

cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
plt.rcParams.update({'font.size': 16})

# pt_s = ["Pt323_SOCCO"]
pt_sel = ['Pt196']
drugs = drug_sel = ['LENALIDOMIDE']

# drugs = ["BTZ"]
pt_disks = [pt_sel]


def main():
    linear_regression()
    # my_heatmap_2()


def linear_regression():
    pt_dict = {pt: disk[0] for disk in pt_s_dir for pt in disk[1]}
    pt_amount = 0
    for i in range(len(pt_disks)):
        pt_amount += len(pt_disks[i])

    r_square_a = np.zeros((pt_amount, len(drugs)), np.float)
    b = np.zeros((pt_amount, len(drugs)), np.float)
    rmse_s = np.zeros((pt_amount, len(drugs), 5), np.float)

    r_square_a[:, :] = np.nan
    b[:, :] = np.nan
    rmse_s[:, :, :] = np.nan

    plt.figure(1, figsize=(8 * 3, 6 * 2))
    pt_i = 0
    # drug_i = 0

    pt_idx = 0
    for pt_s in range(len(pt_disks)):
        for pt in pt_disks[pt_s]:
            raw_path = pt_dict[pt]
            print(pt)
            plt.figure(2, figsize=(6 * col_amount, 6 * len(drugs)))
            plt.clf()

            pt_skip = False

            control_table = []
            ten_ctrl_bea_s = []
            ten_ctrl_bea_s_imgJ = []

            control_table_imj = []

            drug_i = 0
            life_span = 0
            for drug in ["CONTROL"] + drugs:

                drug_skip = False

                if (pt_skip):
                    break

                with open(raw_path + pt + "/GraphPadFiles/PtSample/ExperimentalDesign.txt", "r") as f:
                    lines = f.readlines()

                    g2 = []
                    m = 0
                    concentrations = []

                    match_list = []
                    # actually this is duplicate in the long match list, but this is useful when add new drug,which is not in the drug_name list.
                    match_list.append(drug)
                    match_list.append(drug + "_")
                    match_list.append(drug + "_2")

                    for d1 in range(len(drug_names)):
                        if drug in drug_names[d1]:
                            for d2 in range(len(drug_names[d1])):
                                match_list.append(drug_names[d1][d2])
                                match_list.append(drug_names[d1][d2] + "_")
                                match_list.append(drug_names[d1][d2] + "_2")
                            break

                    for l in lines:
                        m = re.search(';(.+?);', l)
                        m_1 = m.group(1)

                        # if (drug + "_" == m_1 or drug + "_2" == m_1 or drug == m_1):# the drug == m_1 is for control
                        # abbr = drug_abbr_dict.get(drug)
                        if (m_1 in match_list):  # the drug == m_1 is for control
                            bea_str = l[0:m.start()]
                            bea_str = re.sub("Beacon-", "", bea_str)
                            bea_1 = bea_str.split(",")
                            g2.append(bea_1)

                            if (len(concentrations) == 0):
                                concentrations_str = l[m.end():]
                                concentrations = concentrations_str.split(",")

                    if (len(g2) == 0):
                        print(pt, " no drug ", drug, file=log_f)
                        continue

                bea_s = g2[0] + g2[1]
                bea_arr = np.array(bea_s)
                bea_arr = bea_arr.astype(np.int64)
                bea_arr = np.unique(bea_arr)
                print(bea_arr)

                loop_cnt = 0

                if (drug == "CONTROL"):

                    control_num = 0
                    for beacon in bea_arr:
                        # input_path = path_di[pt_s] + pt + "/TimeLapseVideos/info_ucf/Beacon_" + str(beacon) + "_live_dead_table.txt"
                        input_path = path_di[pt_s] + pt + "/info_ucf/Beacon_" + str(beacon) + "_live_dead_table.txt"
                        # input_path = "/home/qibing/disk_16t/Pt210/info_ucf/Beacon_" + str(beacon) + "_live_dead_table.txt"
                        if (not os.path.exists(input_path)):
                            print("file not exist.", input_path)
                            continue
                            # break

                        input_path_imj = raw_path + pt + "/TimeLapseVideos/Results/Results_" + "{0:0=3d}".format(
                            beacon) + ".csv"

                        if (not os.path.exists(input_path_imj)):
                            print("file not exist.", input_path_imj)
                            exit()

                        table = np.loadtxt(input_path)
                        # table_imj = np.loadtxt(input_path_imj)
                        table_imj = np.genfromtxt(input_path_imj, delimiter=',')[1:]
                        life_span = len(table_imj)

                        if (np.sum(table[0]) == 0 or table[0][0] == 0 or table[0][2] == 0 or np.sum(table[-1]) == 0):
                            print("Bad Beacon: ", pt, drug, beacon)
                            continue

                        # if(np.sum(table[-1]) == 0):
                        #     print("Row delete: ", input_path, len(table) - 1)
                        #     table = np.delete(table, len(table) - 1, 0)

                        dose = table[:, 2][-life_span:]
                        ten_ctrl_bea_s.append(dose)
                        dose = dose / dose[0]
                        control_table.append(dose)

                        # dose_imj = re.sub("Beacon-...,", "", table_imj)
                        dose_imj = table_imj
                        ten_ctrl_bea_s_imgJ.append(dose_imj)
                        dose_imj = dose_imj / dose_imj[0]
                        control_table_imj.append(dose_imj)

                        control_num += 1

                    control = sum(control_table)
                    # control = control / len(bea_arr)
                    if (control_num < 10):
                        print(pt, drug, beacon, "ctrl num is less than 10:", control_num)
                    control = control / control_num

                    control_imj = sum(control_table_imj)
                    control_imj = control_imj / control_num
                    # continue

                    doses = [[] for i in range(5)]
                    doses_imj = [[] for i in range(5)]
                    bea_idx = 0

                    # print(bea_arr)

                    # # for beacon in bea_arr:
                    # for bea_idx in range(len(bea_arr)):
                    #     # input_path_imj = path_di + pt + "/TimeLapseVideos/Results/Results_" + "{0:0=3d}".format(bea_arr[bea_idx]) + ".csv"
                    #     input_path_imj = raw_path + pt + "/TimeLapseVideos/Results/Results_" + "{0:0=3d}".format(bea_arr[bea_idx]) + ".csv"
                    #     # dose_imj = re.sub("Beacon-...,", "", table_imj)
                    #     table_imj = np.genfromtxt(input_path_imj, delimiter=',')[1:]
                    #     # dose_imj = re.sub("Beacon-...,", "", table_imj)
                    #     dose_imj = table_imj
                    #     print(dose_imj)
                    #     ten_ctrl_bea_s_imgJ.append(dose_imj)
                    #     dose_imj = dose_imj / dose_imj[0]
                    #     control_table_imj.append(dose_imj)

                    #     # input_path = path_di[pt_s] + pt + "/TimeLapseVideos/info_ucf/Beacon_" + str(bea_arr[bea_idx]) + "_live_dead_table.txt"
                    #     input_path = path_di[pt_s] + pt + "/info_ucf/Beacon_" + str(bea_arr[bea_idx]) + "_live_dead_table.txt"
                    #     # input_path = "/home/qibing/disk_16t/Pt210/info_ucf/Beacon_" + str(bea_arr[bea_idx]) + "_live_dead_table.txt"
                    #     if(not os.path.exists(input_path)):
                    #         print("file not exist.", input_path)
                    #         continue
                    #         # break

                    #     table = np.loadtxt(input_path)

                    #     if(np.sum(table[0]) == 0):
                    #         print("Bad Beacon: ", pt, drug, beacon)
                    #         continue

                    #     if(np.sum(table[-1]) == 0):
                    #         print("Row delete: ", input_path, len(table) - 1)
                    #         table = np.delete(table, len(table) - 1, 0)

                    #     dose = table[:, 2]
                    #     ten_ctrl_bea_s.append(dose)
                    #     # print(len(ten_ctrl_bea_s))
                    #     dose = dose / dose[0]
                    #     control_table.append(dose)

                    #     control_num += 1

                    # control = sum(control_table)
                    # # control = control / len(bea_arr)
                    # if(control_num < 10):
                    #     print(pt, drug, beacon, "ctrl num is less than 10:", control_num)
                    # control = control / control_num

                    # control_imj = sum(control_table_imj)
                    # control_imj = control_imj / control_num
                    # continue

                doses = [[] for i in range(5)]
                doses_imj = [[] for i in range(5)]
                bea_idx = 0

                ten_doses = [[] for i in range(10)]
                ten_doses_imgJ = [[] for i in range(10)]

                # for beacon in bea_arr:
                for bea_idx in range(len(bea_arr)):
                    input_path_imj = raw_path + pt + "/TimeLapseVideos/Results/Results_" + "{0:0=3d}".format(
                        bea_arr[bea_idx]) + ".csv"
                    # dose_imj = re.sub("Beacon-...,", "", table_imj)
                    table_imj = np.genfromtxt(input_path_imj, delimiter=',')[1:]
                    dose_imj = table_imj
                    ten_doses_imgJ[bea_idx].append(dose_imj)
                    dose_imj = dose_imj / dose_imj[0]
                    doses_imj[bea_idx % 5].append(dose_imj)

                    input_path = path_di[pt_s] + pt + "/info_ucf/Beacon_" + str(
                        bea_arr[bea_idx]) + "_live_dead_table.txt"
                    # input_path = "/home/qibing/disk_16t/Pt210/info_ucf/Beacon_" + str(bea_arr[bea_idx]) + "_live_dead_table.txt"
                    if (not os.path.exists(input_path)):
                        print("file not exist.", input_path)
                        continue

                    table = np.loadtxt(input_path)

                    if (np.sum(table[0]) == 0):
                        print("Bad Beacon: ", pt, drug, bea_arr[bea_idx])
                        continue

                    if (np.sum(table[-1]) == 0):
                        print("Row delete: ", input_path, len(table) - 1)
                        table = np.delete(table, len(table) - 1, 0)

                    dose = table[:, 2][-life_span:]
                    # print(bea_arr[bea_idx], dose)
                    ten_doses[bea_idx].append(dose)
                    dose = dose / dose[0]
                    doses[bea_idx % 5].append(dose)

            # x = np.arange(0, len(doses[0][0]), 1) / 48.0
            # print(ten_ctrl_bea_s_imgJ)
            x = np.arange(0, len(ten_ctrl_bea_s_imgJ[0]), 1)
            diff = len(ten_ctrl_bea_s[0]) - len(ten_ctrl_bea_s_imgJ[0])

            plt.figure(1)

            plt.subplot(2, 3, 1)
            plt.title(pt + "_Control")
            # plt.ylim(0, 2e6)
            for i in range(len(ten_ctrl_bea_s)):
                plt.plot(x, ten_ctrl_bea_s[i][diff:], '--', label=str(i))
            plt.legend(loc='best')

            plt.subplot(2, 3, 2)
            plt.title(pt + "_" + drug)
            # plt.ylim(0, 2e6)
            for i in range(len(ten_doses)):
                if (len(ten_doses[i]) > 0):  # and i%5 == 0
                    plt.plot(x, ten_doses[i][0][diff:], label=str(bea_arr[i]))
            plt.legend(loc='best')

            plt.subplot(2, 3, 3)
            plt.xlabel("Time(day)")
            plt.ylabel("Viability")
            # plt.ylim(0.0, 1.15)
            plt.ylim(0.0, 1.5)
            plt.title("Viability_" + pt + "_" + drug)
            five_doses = [[] for i in range(5)]
            for i in range(5):
                if (len(doses[i]) == 0):
                    continue

                if (len(doses[i]) > 0):
                    five_doses[i].append(sum(doses[i]) / len(doses[i]))
                else:
                    # five_doses[i].append(0)
                    print("There is not result for Drug:", pt, drug)
                    drug_skip = True
                five_doses[i][0] = five_doses[i][0] / control
                plt.plot(x, five_doses[i][0][diff:], label=concentrations[i])
                # break
            plt.legend(loc='best')

            plt.subplot(2, 3, 4)
            plt.title(pt + "_ctrl_imgJ")
            # plt.ylim(0, 2e6)
            for i in range(len(ten_ctrl_bea_s_imgJ)):
                plt.plot(x, ten_ctrl_bea_s_imgJ[i], label=str(i))
            plt.legend(loc='best')

            plt.subplot(2, 3, 5)
            plt.title(pt + "_" + drug + "_imgJ")
            # plt.ylim(0, 2e6)
            # print("qibing: ", len(ten_doses_imgJ))
            for i in range(len(ten_doses_imgJ)):
                if (len(ten_doses_imgJ[i]) > 0):  # and i%5 == 0
                    plt.plot(x, ten_doses_imgJ[i][0], label=str(bea_arr[i]))

            plt.legend(loc='best')

            plt.subplot(2, 3, 6)
            plt.xlabel("Time(day)")
            plt.ylabel("Viability")
            # plt.xlim(0, x_imj.max())
            plt.ylim(0.0, 1.5)
            plt.title("Viability_ImJ_" + pt + "_" + drug)
            five_doses_imj = [[] for i in range(5)]
            for i in range(5):
                if (len(doses_imj[i]) == 0):
                    continue
                five_doses_imj[i].append(sum(doses_imj[i]) / len(doses_imj[i]))
                five_doses_imj[i][0] = five_doses_imj[i][0] / control_imj
                # x_imj = np.arange(0, len(five_doses_imj[i][0]), 1) / 48.0
                plt.plot(x, five_doses_imj[i][0], label=concentrations[i])
                # break
            plt.legend(loc='best')

            print(out_path)
            plt.savefig(out_path + pt + "_" + drug + "_individual_lines.png")


if __name__ == "__main__":
    # execute main
    main()