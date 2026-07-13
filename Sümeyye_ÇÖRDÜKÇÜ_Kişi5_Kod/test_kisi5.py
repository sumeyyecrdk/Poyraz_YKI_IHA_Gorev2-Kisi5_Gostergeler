"""
test_kisi5.py
==============
KİŞİ 5 — Kendi 4 widget'ımı (UcusGostergeleri, KontrolPaneli, DurumPaneli,
BaglantiPaneli) tek başına, sahte veriyle test etmek için yazdığım script.

Bu dosya sadece kendi modülümü doğrulamak için var.
main.py, merkezin gcs_pencere.py'sini açar; o dosyaya henüz entegrasyon
yapılmadığı için benim panellerim orada görünmez. Bu yüzden kendi test
penceremi kendim kuruyorum.

Bu dosya, panellerin sadece veri almadığını, aynı zamanda butonlara basıldığında
üretilen sinyallerin (ARM, DISARM, MOD DEĞİŞTİR vb.) durum modelini nasıl 
etkilediğini merkeze kanıtlamak için çift yönlü (Kapalı Çevrim) olarak tasarlanmıştır.
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
import time

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer

from core.veri_modeli import TelemetriVerisi
from arayuz.gostergeler import UcusGostergeleri, KontrolPaneli, DurumPaneli, BaglantiPaneli


class FonksiyonelTestPenceresi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KİŞİ 5 - Bağlantı ve Durum Testi")
        self.resize(700, 680)
        self.setStyleSheet("background-color: #0d1117;")

        self._baslangic = time.time()

        # İÇ DURUM DEĞİŞKENLERİ 
        self.mevcut_armed = False
        self.mevcut_mode = "MANUAL"
        self.mevcut_waypoint = 0
        
        # Bağlantı durumlarını hafızada tutuyoruz (Aç/Kapat mekanizması için)
        self.baglanti_durumlari = {
            "MAVLink": False,
            "Görev Bil.": False,
            "Sunucu": False
        }

        # Arayüz Düzeni
        layout = QVBoxLayout(self)

        self.gostergeler = UcusGostergeleri()
        self.durum = DurumPaneli()
        self.baglanti = BaglantiPaneli()
        self.kontrol = KontrolPaneli()
        
        self.log_label = QLabel("Test Başladı. 'BAĞLAN' ve 'KONTROL' butonlarını test edebilirsiniz...")
        self.log_label.setStyleSheet("color: #58a6ff; font-weight: bold; padding: 8px; border-top: 1px solid #21262d;")

        layout.addWidget(self.gostergeler)
        layout.addWidget(self.durum)
        layout.addWidget(self.baglanti)
        layout.addWidget(self.kontrol)
        layout.addWidget(self.log_label)

        
        # DİNAMİK BAĞLANTI BUTONU KÖPRÜSÜ
        # BaglantiPaneli içindeki QPushButton nesnelerini buluyoruz.
        baglan_butonlari = self.baglanti.findChildren(QPushButton)
        
        # Sırasıyla hangi butonun hangi hatta ait olduğunu eşleştiriyoruz
        hat_haritasi = ["MAVLink", "Görev Bil.", "Sunucu"]
        
        for i, btn in enumerate(baglan_butonlari):
            if i < len(hat_haritasi):
                hat_adi = hat_haritasi[i]
                # Butona her tıklandığında durumu tersine çevir (Toggle) ve paneli güncelle
                btn.clicked.connect(lambda checked, h=hat_adi, b=btn: self._slot_baglanti_tetikle(h, b))

        # ARAÇ KONTROL PANELİ SİNYAL BAĞLANTILARI 
        self.kontrol.arm_istendi.connect(self._slot_arm_yap)
        self.kontrol.disarm_istendi.connect(self._slot_disarm_yap)
        self.kontrol.mod_degistir_istendi.connect(self._slot_mod_degistir)
        
        self.kontrol.kalkis_istendi.connect(lambda: self._slot_navigasyon_tetikle("KALKIŞ", 1))
        self.kontrol.inis_istendi.connect(lambda: self._slot_navigasyon_tetikle("İNİŞ", 0))
        self.kontrol.serbest_rota_istendi.connect(lambda: self._slot_navigasyon_tetikle("SERBEST ROTA", 3))

        # Sahte Telemetri Döngüsü (~10 Hz)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._telemetri_dongusu)
        self.timer.start(100)

    # BAĞLANTI BUTONU REAKSİYONU 
    def _slot_baglanti_tetikle(self, hat_adi, buton_nesnesi):
        # Durumu tersine çevir (Bağlıysa kopar, kopuksa bağla)
        yeni_durum = not self.baglanti_durumlari[hat_adi]
        self.baglanti_durumlari[hat_adi] = yeni_durum
        
        # hat_durumu_guncelle fonksiyonunu çağırıyoruz
        self.baglanti.hat_durumu_guncelle(hat_adi, yeni_durum)
        
        # Görsel geri bildirimler
        if yeni_durum:
            buton_nesnesi.setText("KES")
            self.log_label.setText(f"{hat_adi} bağlantısı kuruldu.")
            self.baglanti.connection_status_log.setText(f"{hat_adi} Aktif")
        else:
            buton_nesnesi.setText("BAĞLAN")
            self.log_label.setText(f"{hat_adi} bağlantısı kesildi.")
            self.baglanti.connection_status_log.setText(f"{hat_adi} Bağlantısı Koptu")

    # KONTROL BUTONLARI REAKSİYONLARI 
    def _slot_arm_yap(self):
        self.mevcut_armed = True
        self.log_label.setText("Sinyal: ARM istendi.")

    def _slot_disarm_yap(self):
        self.mevcut_armed = False
        self.log_label.setText("Sinyal: DISARM istendi.")

    def _slot_mod_degistir(self, yeni_mod):
        self.mevcut_mode = yeni_mod
        self.log_label.setText(f"Sinyal: Mod {yeni_mod} olarak değiştirildi.")

    def _slot_navigasyon_tetikle(self, komut_adi, hedef_wp):
        self.mevcut_waypoint = hedef_wp
        self.log_label.setText(f"Sinyal: {komut_adi} tetiklendi. Hedef WP: {hedef_wp}")

    # TELEMETRİ GÜNCELLEME
    def _telemetri_dongusu(self):
        t_gecen = time.time() - self._baslangic

        t = TelemetriVerisi()
        
        # Göstergelerin hareket etmesi için dalgalı sahte veriler
        t.roll = math.radians(20 * math.sin(t_gecen))
        t.pitch = math.radians(10 * math.sin(t_gecen * 0.7))
        t.heading = (t_gecen * 10) % 360
        t.altitude = 100 + 10 * math.sin(t_gecen * 0.5)
        t.relative_altitude = t.altitude - 50
        t.airspeed = 20 + 3 * math.sin(t_gecen * 0.5)
        t.groundspeed = t.airspeed - 0.5
        t.climb_rate = 1.2 * math.cos(t_gecen * 0.5)

        t.battery_percentage = 98
        t.battery_voltage = 12.6
        t.battery_current = 8.4
        t.gps_fix = 3
        t.satellites = 11
        t.gps_saat, t.gps_dakika, t.gps_saniye = 14, 30, int(t_gecen) % 60
        t.mavlink_bagli = self.baglanti_durumlari["MAVLink"]

        # Butonlardan gelen kararlı durumlar modele işleniyor
        t.armed = self.mevcut_armed
        t.mode = self.mevcut_mode
        t.next_waypoint = self.mevcut_waypoint

        # Arayüzü besle
        self.gostergeler.guncelle(t)
        self.durum.guncelle(t)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FonksiyonelTestPenceresi()
    win.show()
    sys.exit(app.exec_())
