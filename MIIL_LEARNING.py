# -*- coding: utf-8 -*-

import subprocess #OS関連処理用モジュールの読込
import os #OS関連処理用モジュールの読込
import sys #システム関連処理用モジュールの読込
import time #時間関連処理用モジュールの読込
import numpy as np #行列処理用モジュールの読込
import math as mt #各種計算用モジュールの読込
import glob #ファイルパス一括取得用モジュールの読込
from PySide2 import QtCore, QtGui, QtWidgets #GUI関連処理用モジュールの読込
from MIIL_LEARNING_GUI import Ui_MainWindow #QT Designerで作成し変換したファイルの読込

from make_cfg_resnet152_trident import cfg_resnet152_trident
from make_cfg_yolov3 import cfg_yolov3
from make_cfg_yolov3_5l import cfg_yolov3_5l
from make_cfg_yolov3_spp import cfg_yolov3_spp
from make_cfg_yolo_v3_tiny_pan3 import cfg_yolo_v3_tiny_pan3
from make_cfg_yolov4 import cfg_yolov4

#####グローバル変数########################################
capLoop = 0 #動画を表示中か判定するフラグ
LabelNum = 0 #ラベル数を代入する変数
CheckNum = 1 #チェックボックスの選択状況を記憶する変数
cfgNum = 1 #コンフィグの選択状況を記憶する変数
#####Pysideのウィンドウ処理クラス########################################
class MainWindow1(QtWidgets.QMainWindow): #QtWidgets.QMainWindowを継承
#=====GUI用クラス継承の定型文========================================
    def __init__(self, parent = None): #クラス初期化時にのみ実行される関数（コンストラクタと呼ばれる）
        super(MainWindow1, self).__init__(parent) #親クラスのコンストラクタを呼び出す（親クラスのコンストラクタを再利用したい場合）　指定する引数は、親クラスのコンストラクタの引数からselfを除いた引数
        self.ui = Ui_MainWindow() #uiクラスの作成。Ui_MainWindowのMainWindowは、QT DesignerのobjectNameで設定した名前
        self.ui.setupUi(self) #uiクラスの設定
        self.ui.comboBox1.addItems(["1", "2", "3", "4", "5", "6", "7", "8"]) #####コンボボックスにアイテムを追加
        self.ui.comboBox1.setCurrentIndex(0) #####コンボボックスのアイテムを選択
        self.ui.comboBox2.addItems(["1", "2", "4", "8", "16", "32", "64", "128", "256"]) #####コンボボックスにアイテムを追加
        self.ui.comboBox2.setCurrentIndex(5) #####コンボボックスのアイテムを選択
        self.ui.comboBox3.addItems(["1", "2", "4", "8", "16", "32", "64", "128", "256"]) #####コンボボックスにアイテムを追加
        self.ui.comboBox3.setCurrentIndex(3) #####コンボボックスのアイテムを選択
        #self.ui.comboBox4.addItems(["10", "20", "30", "40", "50"]) #####コンボボックスにアイテムを追加
        #self.ui.comboBox4.setCurrentIndex(0) #####コンボボックスのアイテムを選択
        self.ui.comboBox5.addItems(["32", "64", "96", "128", "160", "192", "224", "256", "288", "320", "352", "384", "416", "448", "480", "512", "544", "576", "608", "640", "672", "704", "736", "768", "800","832","864", "896","928","960", "992", "1024", "1056", "1088", "1120"]) #####コンボボックスにアイテムを追加
        self.ui.comboBox5.setCurrentIndex(18) #####コンボボックスのアイテムを選択
        self.ui.comboBox6.addItems(["32", "64", "96", "128", "160", "192", "224", "256", "288", "320", "352", "384", "416", "448", "480", "512", "544", "576", "608", "640", "672", "704", "736", "768", "800","832","864", "896","928","960", "992", "1024", "1056", "1088", "1120"]) #####コンボボックスにアイテムを追加
        self.ui.comboBox6.setCurrentIndex(18) #####コンボボックスのアイテムを選択
        self.ui.comboBox7.addItems(["32", "64", "96", "128", "160", "192", "224", "256", "288", "320", "352", "384", "416", "448", "480", "512", "544", "576", "608", "640", "672", "704", "736", "768", "800","832","864", "896","928","960", "992", "1024", "1056", "1088", "1120"]) #####コンボボックスにアイテムを追加
        self.ui.comboBox7.setCurrentIndex(18) #####コンボボックスのアイテムを選択
        self.ui.comboBox8.addItems(["32", "64", "96", "128", "160", "192", "224", "256", "288", "320", "352", "384", "416", "448", "480", "512", "544", "576", "608", "640", "672", "704", "736", "768", "800","832","864", "896","928","960", "992", "1024", "1056", "1088", "1120"]) #####コンボボックスにアイテムを追加
        self.ui.comboBox8.setCurrentIndex(18) #####コンボボックスのアイテムを選択
        self.ui.comboBox9.addItems(["yolov3", "spp", "5l", "trident", "pan3", "yolov4"]) #####コンボボックスにアイテムを追加
        self.ui.comboBox9.setCurrentIndex(0) #####コンボボックスのアイテムを選択
        #-----シグナルにメッソドを関連付け----------------------------------------
        self.ui.radioButton1.clicked.connect(self.radioButton1_clicked) #radioButton1_clickedは任意
        self.ui.radioButton2.clicked.connect(self.radioButton2_clicked) #radioButton2_clickedは任意
        self.ui.radioButton3.clicked.connect(self.radioButton3_clicked) #radioButton3_clickedは任意
        self.ui.radioButton4.clicked.connect(self.radioButton4_clicked) #radioButton4_clickedは任意
        self.ui.radioButton5.clicked.connect(self.radioButton5_clicked) #radioButton5_clickedは任意
        self.ui.comboBox1.currentIndexChanged.connect(self.comboBox1_currentIndexChanged) #comboBox1_currentIndexChangedは任意
        self.ui.comboBox9.currentIndexChanged.connect(self.comboBox9_currentIndexChanged) #comboBox9_currentIndexChangedは任意
        self.ui.pushButton1.clicked.connect(self.pushButton1_clicked) #pushButton1_clickedは任意
        self.ui.pushButton2.clicked.connect(self.pushButton2_clicked) #pushButton2_clickedは任意
        self.ui.pushButton3.clicked.connect(self.pushButton3_clicked) #pushButton3_clickedは任意
        self.ui.pushButton4.clicked.connect(self.pushButton4_clicked) #pushButton4_clickedは任意
        #self.ui.pushButton5.clicked.connect(self.pushButton5_clicked) #pushButton5_clickedは任意
        self.ui.pushButton6.clicked.connect(self.pushButton6_clicked) #pushButton6_clickedは任意
        self.ui.pushButton7.clicked.connect(self.pushButton7_clicked) #pushButton7_clickedは任意
        self.ui.pushButton8.clicked.connect(self.pushButton8_clicked) #pushButton8_clickedは任意
        self.ui.pushButton9.clicked.connect(self.pushButton9_clicked) #pushButton9_clickedは任意
        #self.ui.pushButton10.clicked.connect(self.pushButton10_clicked) #pushButton10_clickedは任意
        self.ui.pushButton11.clicked.connect(self.pushButton11_clicked) #pushButton11_clickedは任意
        #self.ui.pushButton12.clicked.connect(self.pushButton12_clicked) #pushButton12_clickedは任意
        self.ui.pushButton13.clicked.connect(self.pushButton13_clicked) #pushButton13_clickedは任意
        #self.ui.pushButton14.clicked.connect(self.pushButton14_clicked) #pushButton14_clickedは任意
        #self.ui.pushButton15.clicked.connect(self.pushButton15_clicked) #pushButton15_clickedは任意
        #self.ui.pushButton16.clicked.connect(self.pushButton16_clicked) #pushButton16_clickedは任意
        self.ui.pushButton17.clicked.connect(self.pushButton17_clicked) #pushButton17_clickedは任意
        #self.ui.pushButton18.clicked.connect(self.pushButton18_clicked) #pushButton18_clickedは任意
        self.ui.pushButton19.clicked.connect(self.pushButton19_clicked) #pushButton19_clickedは任意
        self.ui.pushButton20.clicked.connect(self.pushButton20_clicked) #pushButton20_clickedは任意
        #self.ui.pushButton21.clicked.connect(self.pushButton21_clicked) #pushButton21_clickedは任意
        #self.ui.pushButton22.clicked.connect(self.pushButton22_clicked) #pushButton22_clickedは任意
        self.ui.pushButton23.clicked.connect(self.pushButton23_clicked) #pushButton23_clickedは任意
        self.ui.pushButton24.clicked.connect(self.pushButton24_clicked) #pushButton24_clickedは任意
        self.ui.pushButton25.clicked.connect(self.pushButton25_clicked) #pushButton25_clickedは任意
        #self.ui.pushButton26.clicked.connect(self.pushButton26_clicked) #pushButton26_clickedは任意

#=====ウィジットのシグナル処理用メッソド========================================

    #-----radioButton1用イベント処理----------------------------------------
    ##########
    #学習済みネットワークから継続して学習
    ##########
    def radioButton1_clicked(self):
        global CheckNum
        CheckNum = 1

    #-----radioButton2用イベント処理----------------------------------------
    ##########
    #新規に学習
    ##########
    def radioButton2_clicked(self):
        global CheckNum
        CheckNum = 2

    #-----radioButton3用イベント処理----------------------------------------
    ##########
    #学習済みネットワークを取得
    ##########
    def radioButton3_clicked(self):
        global CheckNum
        CheckNum = 3

    #-----radioButton4用イベント処理----------------------------------------
    ##########
    #アンカーを算出
    ##########
    def radioButton4_clicked(self):
        global CheckNum
        CheckNum = 4

    #-----radioButton5用イベント処理----------------------------------------
    ##########
    #検出テスト
    ##########
    def radioButton5_clicked(self):
        global CheckNum
        CheckNum = 5






















    #-----comboBox9用イベント処理----------------------------------------
    def comboBox9_currentIndexChanged(self):
        global cfgNum
        index = self.ui.comboBox9.currentIndex()
        if index == 0: #yolov3
            cfgNum = 1
            self.ui.lineEdit12.setText('anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326')
            self.ui.checkBox1.setEnabled(True)
            self.ui.checkBox3.setEnabled(True)
            self.ui.checkBox7.setEnabled(True)
            self.ui.checkBox7.setChecked(True)
            self.ui.lineEdit11.setText("9")
        elif index ==1: #spp
            cfgNum = 2
            self.ui.lineEdit12.setText('anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326')
            self.ui.checkBox1.setEnabled(True)
            self.ui.checkBox3.setEnabled(True)
            self.ui.checkBox7.setEnabled(True)
            self.ui.checkBox7.setChecked(True)
            self.ui.lineEdit11.setText("9")
        elif index ==2: #5l
            cfgNum = 3
            self.ui.lineEdit12.setText('anchors = 4,4,  5,5,  6,6, 7,7,  8,8,  9,9, 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326')
            self.ui.checkBox1.setEnabled(False)
            self.ui.checkBox1.setChecked(False)
            self.ui.checkBox3.setEnabled(False)
            self.ui.checkBox3.setChecked(False)
            self.ui.checkBox7.setEnabled(True)
            self.ui.checkBox7.setChecked(True)
            self.ui.lineEdit11.setText("15")
        elif index ==3: #trident
            cfgNum = 4
            #self.ui.lineEdit12.setText('anchors = 8,8, 10,13, 16,30, 33,23,  32,32, 30,61, 62,45, 59,119,   80,80, 116,90, 156,198, 373,326')
            self.ui.lineEdit12.setText('')
            self.ui.checkBox1.setEnabled(False)
            self.ui.checkBox1.setChecked(False)
            self.ui.checkBox3.setEnabled(False)
            self.ui.checkBox3.setChecked(False)
            self.ui.checkBox7.setEnabled(False)
            self.ui.checkBox7.setChecked(False)
            self.ui.lineEdit11.setText("12")
        elif index ==4: #pan3
            cfgNum = 5
            self.ui.lineEdit12.setText('anchors = 8,8, 10,13, 16,30, 33,23,  32,32, 30,61, 62,45, 59,119,   80,80, 116,90, 156,198, 373,326')
            self.ui.checkBox1.setEnabled(False)
            self.ui.checkBox1.setChecked(False)
            self.ui.checkBox3.setEnabled(False)
            self.ui.checkBox3.setChecked(False)
            self.ui.checkBox7.setEnabled(False)
            self.ui.checkBox7.setChecked(False)
            self.ui.lineEdit11.setText("12")
        elif index ==5: #yolov4
            cfgNum = 6
            self.ui.lineEdit12.setText('anchors = 12,16, 19,36, 40,28, 36,75, 76,55, 72,146, 142,110, 192,243, 459,401')
            self.ui.checkBox1.setEnabled(True)
            self.ui.checkBox3.setEnabled(True)
            self.ui.checkBox7.setEnabled(True)
            self.ui.checkBox7.setChecked(True)
            self.ui.lineEdit11.setText("9")






















    #-----comboBox1用イベント処理----------------------------------------
    ##########
    #使用ＧＰＵ数が変更された時の処理
    ##########
    def comboBox1_currentIndexChanged(self):
        msgbox = QtWidgets.QMessageBox(self) #メッセージボックスを準備
        msgbox.setWindowTitle("MLFYV3")
        msgbox.setText('PLEASE CHANGE THE VALUE AS BELOW AND SAVE MODEL FILE.\n\nLEARNING RATE = LEARNING RATE FOR 1 GPU / NUMBER OF GPU\n\nMAX BATCHES = MAX BATCHES FOR 1 GPU * NUMBER OF GPU\n\nBURN IN = BURN IN FOR 1 GPU * NUMBER OF GPU') #メッセージボックスのテキストを設定
        ret = msgbox.exec_() #メッセージボックスを表示

    #-----pushButton1用イベント処理----------------------------------------
    ##########
    #各種処理実行
    ##########
    def pushButton1_clicked(self):
        global capLoop
        if self.ui.lineEdit3.text() == '':
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET DARKNET FOLDER.")
            ret = msgbox.exec_()
        elif self.ui.lineEdit6.text() == '':
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET MODEL FILE.")
            ret = msgbox.exec_()
        elif self.ui.lineEdit7.text() == '' and self.ui.radioButton1.isChecked() == True:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET WEIGHT FILE.")
            ret = msgbox.exec_()
        elif self.ui.lineEdit7.text() == '' and self.ui.radioButton3.isChecked() == True:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET WEIGHT FILE.")
            ret = msgbox.exec_()
        elif self.ui.lineEdit7.text() == '' and self.ui.radioButton5.isChecked() == True:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET WEIGHT FILE.")
            ret = msgbox.exec_()
        elif self.ui.lineEdit9.text() == '' and self.ui.radioButton1.isChecked() == True:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET PARAMETER FILE.")
            ret = msgbox.exec_()
        elif self.ui.lineEdit9.text() == '' and self.ui.radioButton2.isChecked() == True:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET PARAMETER FILE.")
            ret = msgbox.exec_()
        elif self.ui.lineEdit9.text() == '' and self.ui.radioButton4.isChecked() == True:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET PARAMETER FILE.")
            ret = msgbox.exec_()
        elif self.ui.lineEdit9.text() == '' and self.ui.radioButton5.isChecked() == True:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET PARAMETER FILE.")
            ret = msgbox.exec_()
        else:
            if self.ui.radioButton1.isChecked() == True:
                cmd = self.ui.lineEdit3.text() + ' detector train ' + \
                self.ui.lineEdit9.text() + ' ' + self.ui.lineEdit6.text() + ' ' + self.ui.lineEdit7.text()
                if self.ui.checkBox4.isChecked() == True:
                    cmd = cmd + ' -map'
                if self.ui.checkBox5.isChecked() == True:
                    cmd = cmd + ' -show_imgs'
            elif self.ui.radioButton2.isChecked() == True:
                cmd = self.ui.lineEdit3.text() + ' detector train ' + \
                self.ui.lineEdit9.text() + ' ' + self.ui.lineEdit6.text()
                if self.ui.checkBox4.isChecked() == True:
                    cmd = cmd + ' -map'
                if self.ui.checkBox5.isChecked() == True:
                    cmd = cmd + ' -show_imgs'
            elif self.ui.radioButton3.isChecked() == True:
                cmd = self.ui.lineEdit3.text() + ' partial ' + \
                self.ui.lineEdit6.text() + ' ' + self.ui.lineEdit7.text() + \
                ' ' + self.ui.lineEdit7.text() + '.conv.' + self.ui.lineEdit10.text() + '.weights ' + self.ui.lineEdit10.text()
            elif self.ui.radioButton4.isChecked() == True:
                cmd = self.ui.lineEdit3.text() + ' detector calc_anchors ' + \
                self.ui.lineEdit9.text() + ' -num_of_clusters ' + self.ui.lineEdit11.text() + \
                ' -width ' + self.ui.comboBox7.currentText() + ' -height ' + self.ui.comboBox8.currentText() + ' -show'
            elif self.ui.radioButton5.isChecked() == True:
                cmd = self.ui.lineEdit3.text() + ' detector demo ' + \
                self.ui.lineEdit9.text() + ' ' + self.ui.lineEdit6.text() + ' ' + self.ui.lineEdit7.text() + \
                ' -c 0 -thresh 0.5'
            if self.ui.comboBox1.currentIndex() > 0:
                GPU = ' -gpus 0'
                for GNum in range(1, self.ui.comboBox1.currentIndex() + 1):
                    GPU = GPU + ',' + str(GNum)
                cmd = cmd + GPU
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText(cmd)
            ret = msgbox.exec_()
            capLoop = 1
            if self.ui.radioButton4.isChecked() == True:
                #ret = str(subprocess.check_output(cmd))
                proc = subprocess.run(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
                ret = str(proc.stdout)
                print(ret)
                ret = ret.replace('\\r\\n', "")
                ret = ret.replace("'", "")
                ret = ret.replace(".0000", "")

                #ret = ret.rsplit("anchors.txt ")
                #self.ui.lineEdit12.setText(ret[1])
                #print(ret[1])
                print(ret)
                ret = ret.rsplit("anchors = ")
                print(ret)
                ancVal = ret[1].split(',')
                ancText = 'anchors = '
                for item in ancVal:
                    item = item.replace(" ", "")
                    item = item.replace('"', "")
                    ancText = ancText + item + ', '
                ancText = ancText.rsplit(',', 1)
                self.ui.lineEdit12.setText(ancText[0])
                print(ancText[0])

            else:
                ret = os.system(cmd)
            capLoop = 0

    #-----pushButton2用イベント処理----------------------------------------
    ##########
    #設定読み込み
    ##########
    def pushButton2_clicked(self):
        global LabelNum
        global CheckNum
        global cfgNum
    #####ファイル読込
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",'mly File (*.mly)')
        if filepath:
            #####ファイル名のみの取得
            filename1 = filepath.rsplit(".", 1) #ファイルパスの文字列右側から指定文字列で分割
            filename2 = filename1[0].rsplit("/", 1) #ファイルパスの文字列右側から指定文字列で分割
            #os.chdir(filename2[0] + "/") #カレントディレクトリをファイルパスへ変更
            f = open(filepath, "r")
            text = ''
            text = f.readlines() #改行コードも含む
            f.close()
            self.ui.comboBox1.setCurrentIndex(int(text[0].replace("\n", ""))) #改行コードを削除してデータを読込む
            self.ui.comboBox2.setCurrentIndex(int(text[1].replace("\n", ""))) #改行コードを削除してデータを読込む
            self.ui.comboBox3.setCurrentIndex(int(text[2].replace("\n", ""))) #改行コードを削除してデータを読込む

            self.ui.comboBox5.setCurrentIndex(int(text[3].replace("\n", ""))) #改行コードを削除してデータを読込む
            self.ui.comboBox6.setCurrentIndex(int(text[4].replace("\n", ""))) #改行コードを削除してデータを読込む
            self.ui.comboBox7.setCurrentIndex(int(text[5].replace("\n", ""))) #改行コードを削除してデータを読込む
            self.ui.comboBox8.setCurrentIndex(int(text[6].replace("\n", ""))) #改行コードを削除してデータを読込む
            self.ui.lineEdit1.setText(text[7].replace("\n", "")) #改行コードを削除してデータを読込む
            self.ui.lineEdit2.setText(text[8].replace("\n", "")) #改行コードを削除してデータを読込む
            self.ui.lineEdit3.setText(text[9].replace("\n", "")) #改行コードを削除してデータを読込む

            self.ui.lineEdit5.setText(text[10].replace("\n", "")) #改行コードを削除してデータを読込む
            self.ui.lineEdit6.setText(text[11].replace("\n", "")) #改行コードを削除してデータを読込む
            self.ui.lineEdit7.setText(text[12].replace("\n", "")) #改行コードを削除してデータを読込む

            self.ui.lineEdit9.setText(text[13].replace("\n", "")) #改行コードを削除してデータを読込む
            self.ui.lineEdit10.setText(text[14].replace("\n", "")) #改行コードを削除してデータを読込む
            self.ui.lineEdit11.setText(text[15].replace("\n", "")) #改行コードを削除してデータを読込む

            self.ui.lineEdit13.setText(text[17].replace("\n", "")) #改行コードを削除してデータを読込む
            if self.ui.lineEdit5.text() != '':
                f = open(self.ui.lineEdit5.text(), "r")
                tr = f.readlines() #改行コードも含む
                f.close()
                if len(tr) > 0:
                    LabelNum = 0
                    for Label in tr:
                        LabelNum += 1
                else:
                    msgbox = QtWidgets.QMessageBox(self) #####メッセージボックスを準備
                    msgbox.setWindowTitle("MLFYV3")
                    msgbox.setText("No label found in the file.") #####メッセージボックスのテキストを設定
            CheckNum = int(text[18])
            if CheckNum == 1:
                self.ui.radioButton1.setChecked(True)
            elif CheckNum == 2:
                self.ui.radioButton2.setChecked(True)
            elif CheckNum == 3:
                self.ui.radioButton3.setChecked(True)
            elif CheckNum == 4:
                self.ui.radioButton4.setChecked(True)
            elif CheckNum == 5:
                self.ui.radioButton5.setChecked(True)
            if int(text[19]) == 1:
                self.ui.checkBox1.setChecked(True)
            else:
                self.ui.checkBox1.setChecked(False)
            if int(text[20]) == 1:
                self.ui.checkBox2.setChecked(True)
            else:
                self.ui.checkBox2.setChecked(False)
            if int(text[21]) == 1:
                self.ui.checkBox3.setChecked(True)
            else:
                self.ui.checkBox3.setChecked(False)
            cfgNum = int(text[22])
            if cfgNum == 1:
                self.ui.comboBox9.setCurrentIndex(0) #####コンボボックスのアイテムを選択
                self.ui.checkBox1.setEnabled(True)
                self.ui.checkBox3.setEnabled(True)
                self.ui.checkBox7.setEnabled(True)
                self.ui.lineEdit11.setText("9")
            elif cfgNum == 2:
                self.ui.comboBox9.setCurrentIndex(1) #####コンボボックスのアイテムを選択
                self.ui.checkBox1.setEnabled(True)
                self.ui.checkBox3.setEnabled(True)
                self.ui.checkBox7.setEnabled(True)
                self.ui.lineEdit11.setText("9")
            elif cfgNum == 3:
                self.ui.comboBox9.setCurrentIndex(2) #####コンボボックスのアイテムを選択
                self.ui.checkBox1.setEnabled(False)
                self.ui.checkBox3.setEnabled(False)
                self.ui.checkBox7.setEnabled(False)
                self.ui.lineEdit11.setText("15")
            elif cfgNum == 4:
                self.ui.comboBox9.setCurrentIndex(3) #####コンボボックスのアイテムを選択
                self.ui.checkBox1.setEnabled(False)
                self.ui.checkBox3.setEnabled(False)
                self.ui.checkBox7.setEnabled(False)
                self.ui.lineEdit11.setText("12")
            elif cfgNum == 5:
                self.ui.comboBox9.setCurrentIndex(4) #####コンボボックスのアイテムを選択
                self.ui.checkBox1.setEnabled(False)
                self.ui.checkBox3.setEnabled(False)
                self.ui.checkBox7.setEnabled(False)
                self.ui.lineEdit11.setText("12")
            if cfgNum == 6:
                self.ui.comboBox9.setCurrentIndex(5) #####コンボボックスのアイテムを選択
                self.ui.checkBox1.setEnabled(True)
                self.ui.checkBox3.setEnabled(True)
                self.ui.checkBox7.setEnabled(True)
                self.ui.lineEdit11.setText("9")
            if int(text[23]) == 1:
                self.ui.checkBox4.setChecked(True)
            else:
                self.ui.checkBox4.setChecked(False)
            if int(text[24]) == 1:
                self.ui.checkBox5.setChecked(True)
            else:
                self.ui.checkBox5.setChecked(False)
            if int(text[25]) == 1:
                self.ui.checkBox6.setChecked(True)
            else:
                self.ui.checkBox6.setChecked(False)
            if int(text[26]) == 1:
                self.ui.checkBox7.setChecked(True)
            else:
                self.ui.checkBox7.setChecked(False)

            self.ui.lineEdit12.setText(text[16].replace("\n", "")) #改行コードを削除してデータを読込む

            msgbox = QtWidgets.QMessageBox(self) #####メッセージボックスを準備
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("FILE : Loded.") #####メッセージボックスのテキストを設定
            ret = msgbox.exec_() #####メッセージボックスを表示
            #####
    #####

    #-----pushButton3用イベント処理----------------------------------------
    ##########
    #設定書き込み
    ##########
    def pushButton3_clicked(self):
    #####ファイル書込み
        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "",'mly File (*.mly)')
        if filepath:
            #####ファイル名のみの取得
            filename1 = filepath.rsplit(".", 1) #ファイルパスの文字列右側から指定文字列で分割
            filename2 = filename1[0].rsplit("/", 1) #ファイルパスの文字列右側から指定文字列で分割
            #os.chdir(filename2[0] + "/") #カレントディレクトリをファイルパスへ変更
            f = open(filepath, "w")
            text = ''
            text = str(self.ui.comboBox1.currentIndex()) + "\n" + \
            str(self.ui.comboBox2.currentIndex()) + "\n" + \
            str(self.ui.comboBox3.currentIndex()) + "\n" + \
            str(self.ui.comboBox5.currentIndex()) + "\n" + \
            str(self.ui.comboBox6.currentIndex()) + "\n" + \
            str(self.ui.comboBox7.currentIndex()) + "\n" + \
            str(self.ui.comboBox8.currentIndex()) + "\n" + \
            self.ui.lineEdit1.text() + "\n" + \
            self.ui.lineEdit2.text() + "\n" + \
            self.ui.lineEdit3.text() + "\n" + \
            self.ui.lineEdit5.text() + "\n" + \
            self.ui.lineEdit6.text() + "\n" + \
            self.ui.lineEdit7.text() + "\n" + \
            self.ui.lineEdit9.text() + "\n" + \
            self.ui.lineEdit10.text() + "\n" + \
            self.ui.lineEdit11.text() + "\n" + \
            self.ui.lineEdit12.text() + "\n" + \
            self.ui.lineEdit13.text() + "\n" + \
            str(CheckNum) + "\n"
            if self.ui.checkBox1.isChecked() == True:
                text = text + '1\n'
            else:
                text = text + '0\n'
            if self.ui.checkBox2.isChecked() == True:
                text = text + '1\n'
            else:
                text = text + '0\n'
            if self.ui.checkBox3.isChecked() == True:
                text = text + '1\n'
            else:
                text = text + '0\n'
            text = text + str(cfgNum) + "\n"
            if self.ui.checkBox4.isChecked() == True:
                text = text + '1\n'
            else:
                text = text + '0\n'
            if self.ui.checkBox5.isChecked() == True:
                text = text + '1\n'
            else:
                text = text + '0\n'
            if self.ui.checkBox6.isChecked() == True:
                text = text + '1\n'
            else:
                text = text + '0\n'
            if self.ui.checkBox7.isChecked() == True:
                text = text + '1\n'
            else:
                text = text + '0\n'
            f.writelines(text)
            f.close()
            msgbox = QtWidgets.QMessageBox(self) #####メッセージボックスを準備
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("FILE : Saved.") #####メッセージボックスのテキストを設定
            ret = msgbox.exec_() #####メッセージボックスを表示
            #####
    #####

    #-----pushButton4用イベント処理----------------------------------------
    ##########
    #darknet.exeが存在するフォルダを選択
    ##########
    def pushButton4_clicked(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "exe File", "",'exe File (*.exe)')
        if filepath:
            self.ui.lineEdit3.setText(filepath)

    #-----pushButton6用イベント処理----------------------------------------
    ##########
    #ラベルファイルが存在するフォルダを選択
    ##########
    def pushButton6_clicked(self):
        global LabelNum
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",'lab File (*.lab)')
        if filepath:
            f = open(filepath, "r")
            text = f.readlines() #改行コードも含む
            f.close()
            if len(text) > 0:
                LabelNum = 0
                for Label in text:
                    LabelNum += 1
                self.ui.lineEdit5.setText(filepath)
            else:
                msgbox = QtWidgets.QMessageBox(self) #####メッセージボックスを準備
                msgbox.setWindowTitle("MLFYV3")
                msgbox.setText("No label found in the file.") #####メッセージボックスのテキストを設定

    #-----pushButton7用イベント処理----------------------------------------
    ##########
    #モデルファイルを選択
    ##########
    def pushButton7_clicked(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",'cfg File (*.cfg)')
        if filepath:
            self.ui.lineEdit6.setText(filepath)































    #-----pushButton8用イベント処理----------------------------------------
    ##########
    #モデルファイルを保存
    ##########
    def pushButton8_clicked(self):
        global N_TEXT3
        eNum = self.ui.lineEdit2.text()
        try:
            lNum = self.ui.lineEdit1.text()
            lNum = float(lNum)
        except:
            lNum = 'NG'

        if self.ui.lineEdit1.text() == '':
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET LEARNING RATE.")
            ret = msgbox.exec_()
        elif lNum == 'NG':
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET PROPER VALUE TO LEARNING RATE.")
            ret = msgbox.exec_()
        elif self.ui.lineEdit2.text() == '':
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET MAX BATCHES.")
            ret = msgbox.exec_()
        elif eNum.isdigit() == False:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET PROPER VALUE TO MAX BATCHES.")
            ret = msgbox.exec_()
        elif self.ui.lineEdit5.text() == '':
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("PLEASE SET LABEL FILE.")
            ret = msgbox.exec_()
        elif LabelNum <= 0:
            msgbox = QtWidgets.QMessageBox(self) #####メッセージボックスを準備
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText("NO LABEL FOUND IN THE FILE.") #####メッセージボックスのテキストを設定
            ret = msgbox.exec_()
        else:
            filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", 'cfg File (*.cfg)')
            if filepath:
                cfg_batch=self.ui.comboBox2.currentText()
                cfg_subdivisions=self.ui.comboBox3.currentText()
                cfg_width=self.ui.comboBox5.currentText()
                cfg_height=self.ui.comboBox6.currentText()
                cfg_learning_rate = self.ui.lineEdit1.text()
                cfg_burn_in = self.ui.lineEdit13.text()
                cfg_max_batches =self.ui.lineEdit2.text()
                cfg_classes = str(LabelNum)
                cfg_anchors = self.ui.lineEdit12.text()
                if self.ui.checkBox1.isEnabled() == True:
                    cfg_small = '1'
                else:
                    cfg_small = '0'
                if self.ui.checkBox2.isChecked() == True:
                    cfg_flip = '1'
                else:
                    cfg_flip = '0'
                if self.ui.checkBox3.isChecked() == True:
                    cfg_conv = '1'
                else:
                    cfg_conv = '0'
                if self.ui.checkBox6.isChecked() == True:
                    cfg_jitter = '1'
                else:
                    cfg_jitter = '0'
                if self.ui.checkBox7.isChecked() == True:
                    cfg_random = '1'
                else:
                    cfg_random = '0'
                if self.ui.comboBox9.currentIndex() == 0: #####コンボボックスのアイテムを選択
                    CFG = cfg_yolov3(cfg_batch,cfg_subdivisions,cfg_width,cfg_height,cfg_learning_rate,cfg_burn_in,cfg_max_batches,cfg_classes,cfg_anchors,cfg_flip,cfg_small,cfg_conv,cfg_jitter,cfg_random)
                elif self.ui.comboBox9.currentIndex() == 1: #####コンボボックスのアイテムを選択
                    CFG = cfg_yolov3_spp(cfg_batch,cfg_subdivisions,cfg_width,cfg_height,cfg_learning_rate,cfg_burn_in,cfg_max_batches,cfg_classes,cfg_anchors,cfg_flip,cfg_small,cfg_conv,cfg_jitter,cfg_random)
                elif self.ui.comboBox9.currentIndex() ==2: #####コンボボックスのアイテムを選択
                    CFG = cfg_yolov3_5l(cfg_batch,cfg_subdivisions,cfg_width,cfg_height,cfg_learning_rate,cfg_burn_in,cfg_max_batches,cfg_classes,cfg_anchors,cfg_flip,cfg_jitter,cfg_random)
                elif self.ui.comboBox9.currentIndex() ==3: #####コンボボックスのアイテムを選択
                    CFG = cfg_resnet152_trident(cfg_batch,cfg_subdivisions,cfg_width,cfg_height,cfg_learning_rate,cfg_burn_in,cfg_max_batches,cfg_classes,cfg_flip,cfg_jitter)
                elif self.ui.comboBox9.currentIndex() ==4: #####コンボボックスのアイテムを選択
                    CFG = cfg_yolo_v3_tiny_pan3(cfg_batch,cfg_subdivisions,cfg_width,cfg_height,cfg_learning_rate,cfg_burn_in,cfg_max_batches,cfg_classes,cfg_anchors,cfg_flip,cfg_jitter)
                elif self.ui.comboBox9.currentIndex() == 5: #####コンボボックスのアイテムを選択
                    CFG = cfg_yolov4(cfg_batch,cfg_subdivisions,cfg_width,cfg_height,cfg_learning_rate,cfg_burn_in,cfg_max_batches,cfg_classes,cfg_anchors,cfg_flip,cfg_small,cfg_conv,cfg_jitter,cfg_random)
                f = open(filepath, "w")
                f.writelines(CFG)
                f.close()
                self.ui.lineEdit6.setText(filepath)




















    #-----pushButton9用イベント処理----------------------------------------
    ##########
    #学習済みファイルを選択
    ##########
    def pushButton9_clicked(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",'weights File (*.*)')
        if filepath:
            self.ui.lineEdit7.setText(filepath)

    #-----pushButton11用イベント処理----------------------------------------
    ##########
    #パラメータファイルをを選択
    ##########
    def pushButton11_clicked(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",'parameter File (*.prm)')
        if filepath:
            self.ui.lineEdit9.setText(filepath)

    #-----pushButton13用イベント処理----------------------------------------
    ##########
    #モデルファイルを表示
    ##########
    def pushButton13_clicked(self):
        if self.ui.lineEdit6.text() != '':
            ret = os.system(self.ui.lineEdit6.text())

    #-----pushButton17用イベント処理----------------------------------------
    ##########
    #学習済みファイルを検証
    ##########
    def pushButton17_clicked(self):
        if self.ui.lineEdit3.text() != '' and self.ui.lineEdit6.text() != '' and self.ui.lineEdit7.text() != '' and self.ui.lineEdit9.text() != '':
            ret = os.system(self.ui.lineEdit3.text() + ' detector map ' + self.ui.lineEdit9.text() + ' ' + self.ui.lineEdit6.text() + ' ' + self.ui.lineEdit7.text())
        else:
            msgbox = QtWidgets.QMessageBox(self) #メッセージボックスを準備
            msgbox.setWindowTitle("MLFYV3")
            msgbox.setText('PLEASE SET VALUE TO [DARKNET FOLDE]R OR [WEIGHT FILE] OR [PARAMETER FILE] OR [MODEL FILE].') #メッセージボックスのテキストを設定
            ret = msgbox.exec_()

    #-----pushButton18用イベント処理----------------------------------------
    ##########
    #アンカーをリセット
    ##########
    #def pushButton18_clicked(self):
        #self.ui.lineEdit12.setText('anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326')

    #-----pushButton19用イベント処理----------------------------------------
    ##########
    #ラベルファイルををリセット
    ##########
    def pushButton19_clicked(self):
        self.ui.lineEdit5.setText('')

    #-----pushButton20用イベント処理----------------------------------------
    ##########
    #モデルファイルをリセット
    ##########
    def pushButton20_clicked(self):
        self.ui.lineEdit6.setText('')

    #-----pushButton23用イベント処理----------------------------------------
    ##########
    #パラメータファイルをリセット
    ##########
    def pushButton23_clicked(self):
        self.ui.lineEdit9.setText('')

    #-----pushButton24用イベント処理----------------------------------------
    ##########
    #学習済みファイルをリセット
    ##########
    def pushButton24_clicked(self):
        self.ui.lineEdit7.setText('')

    #-----pushButton25用イベント処理----------------------------------------
    ##########
    #darknet.exeが存在するフォルダをリセット
    ##########
    def pushButton25_clicked(self):
        self.ui.lineEdit3.setText('')

#=====メインウィンドウのイベント処理========================================
    #-----ウィンドウ終了イベントのフック----------------------------------------
    def closeEvent(self, event): #event.accept() event.ignore()で処理を選択可能
        global capLoop
        if capLoop == 1: #ループ実行中の場合
            event.ignore() #メインウィンドウの終了イベントをキャンセル
        else: #ループが実行中でない場合
            event.accept() #メインウィンドウの終了イベントを実行

#####メイン処理（グローバル）########################################
#=====メイン処理定型文========================================
if __name__ == '__main__': #C言語のmain()に相当。このファイルが実行された場合、以下の行が実行される（モジュールとして読込まれた場合は、実行されない）
    app = QtWidgets.QApplication(sys.argv) #アプリケーションオブジェクト作成（sys.argvはコマンドライン引数のリスト）
    win = MainWindow1() #MainWindow1クラスのインスタンスを作成
    win.show() #ウィンドウを表示　win.showFullScreen()やwin.showEvent()を指定する事でウィンドウの状態を変える事が出来る
    sys.exit(app.exec_()) #引数が関数の場合は、関数が終了するまで待ち、その関数の返値を上位プロセスに返す
