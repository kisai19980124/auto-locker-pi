import binascii
import nfc

class reader(object):
    def __init__(self, id_list):
        self.id_list = id_list

    def on_connect(self, tag):
        #タッチ時の処理 
        print("【 Touched 】")
 
        #タグ情報を全て表示 
        print(tag)
 
        #IDmのみ取得して表示 
        self.idm = str(binascii.hexlify(tag._nfcid))
        print("IDm : " + self.idm)
 
        #特定のIDmだった場合のアクション 
        if self.idm in self.id_list:
            print("【 登録されたIDです 】")
 
        return True
 
    def read_id(self):
        self.clf = nfc.ContactlessFrontend('usb')
        try:
            self.clf.connect(rdwr={'on-connect': self.on_connect})
        finally:
            self.clf.close()

    def close(self):
        self.clf.close()