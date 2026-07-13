from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt , pyqtSlot

from core.veri_modeli import TelemetriVerisi

from arayuz.gostergeler.qfi.qfi_ADI import qfi_ADI
from arayuz.gostergeler.qfi.qfi_ALT import qfi_ALT
from arayuz.gostergeler.qfi.qfi_HSI import qfi_HSI
from arayuz.gostergeler.qfi.qfi_SI import qfi_SI

# Birim çevrimleri(1 m/s hız = 1.94384 knot)
_MS_TO_KNOT = 1.94384

#UcusGostergeleri sınıfı, QWidget'tan miras alıyor.Yani QWidget'ın tüm özelliklerini otomatik devralıyor.
class UcusGostergeleri(QWidget):

    #bir nesne üretildiğinde otomatik çalışan fonksiyon.
    def __init__(self, parent=None):

        #miras alınan QWidget sınıfının kendi içinde, bir widget'ın düzgün çalışması için gereken bir sürü gizli hazırlık var.
        #super ile bu miras alınan sınıfı çağırıyorum ki bu hazırlıklar yapılsın ve bizim UcusGostergeleri nesnemiz doğru şekilde oluşsun.
        super().__init__(parent)
        self._kur()

    def _kur(self) -> None:
        # arka plan siyah olsun , çerçeve çizgisi olmasın.
        self.setStyleSheet("background-color: #000000; border: none;")

        #QVBoxLayout sınıfından bir nesne üretildi(dikey sıralayıcı), dış kenar boşluğu ve elemanlar arası iç boşluk ayarlandı.
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # yatay sıralayıcı üretildi. bu nesne doğrudan widget'a değil layout'un içine eklenecek.
        # bu yatay sıralayıcının içine konacak 4 gösterge elemanı arasındaki boşluk ayarlandı.
        qfi_lay = QHBoxLayout()
        qfi_lay.setSpacing(5)

        # her satır ilgili gösterge sınıfından bir nesne üretiyor.
        self.adi = qfi_ADI(self)
        self.alt = qfi_ALT(self)
        self.hsi = qfi_HSI(self)
        self.si = qfi_SI(self)

        # bu döngü ile yatay sıralayıcının içine sırasıyla ADI,ALT,HSI,SI widgetları eklendi.
        for w in (self.adi, self.alt, self.hsi, self.si):
            w.setFixedSize(130, 130)
            qfi_lay.addWidget(w)
        
        #döngü sonucu oluşan yatay sıralayıcı layout (ana dikey sıralayıcı) içine eklendi.
        #layout içine layout eklendiği için Qt de yer alan hazır addLayout fonksiyonu kullanıldı.
        layout.addLayout(qfi_lay)

        # Dijital telemetri metni 
        self.telemetriL = QLabel("Telemetri Verileri Yükleniyor...")
        self.telemetriL.setWordWrap(True)
        #arka planı şeffaf yap,kenarlık yok,yazı rengi beyaz,yazı boyutu 14 piksel
        self.telemetriL.setStyleSheet(
            "background-color: transparent; border: none; color: #ffffff; font-size: 14px;"
        )

        #etiketin içindeki yazının hizalanmasını ayarlayan fonksiyon."|" ile hem üste hem sola yazı hizalandı.
        self.telemetriL.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        #oluşturulan bu etiket ana dikey layout'a eklendi. pencerede fazla boşluk kalırsa elemanlarda anormal bir değişiklik yaşanmaması için addStretch(1) ifadesi yazıldı.
        layout.addWidget(self.telemetriL)
        layout.addStretch(1)
        
    
    @pyqtSlot(object)
    def guncelle(self, t: TelemetriVerisi) -> None:

        # ADI göstergesine , gelen telemetrinin yatış açısını(derece cinsinden) ve burun açısını bildiren ifade yazıldı. ekran değişen değerlere göre yeniden düzenlendi.
        self.adi.setRoll(t.roll_deg)
        self.adi.setPitch(t.pitch_deg)
        self.adi.update()

        # ALT göstergesine telemetri paketindeki ham,çevrilmemiş metre değeri verildi.çünkü qfi_ALT kendi içinde çevrimi yapıyor.
        self.alt.setAltitude(t.altitude)   
        self.alt.update()
        
        # HSI göstergesine telemetrideki heading değeri(yön;zaten derece cinsinden,çevrim gerektirmiyor) verildi ve ekran güncellendi.
        self.hsi.setHeading(t.heading)
        self.hsi.update()

        # SI göstergesine telemetrideki hız m/s cinsinden giriliyor. bunu direkt fonksiyon içinde sabit ile çarpıp knot'a çevrildi,ekran güncellendi.
        self.si.setSpeed(t.airspeed * _MS_TO_KNOT)
        self.si.update()

        # ekrana bilgilerin yazdırılmasında kullanılacak yerel değişkenler tanımlandı.
        irtifa_ft = t.altitude * 3.28084
        hiz_knot = t.airspeed * _MS_TO_KNOT
        pitch_deg = t.pitch_deg
        roll_deg = t.roll_deg
        heading_deg = t.heading

        gps_saat = f"{t.gps_saat:02d}:{t.gps_dakika:02d}:{t.gps_saniye:02d}"

        # veriler ekrana yazdırıldı.
        self.telemetriL.setText(
            f"İrtifa (AGL): {t.relative_altitude:.1f} m   |   İrtifa (MSL): {t.altitude:.1f} m ({irtifa_ft:.0f} ft)\n"
            f"Yer Hızı: {t.groundspeed:.1f} m/s   |   Hava Hızı: {t.airspeed:.1f} m/s ({hiz_knot:.1f} kt)\n"
            f"Heading: {t.heading:.0f}°   Roll: {t.roll_deg:.1f}°   Pitch: {t.pitch_deg:.1f}°\n"
            f"Tırmanma: {t.climb_rate:+.1f} m/s   |   GPS: {t.gps_fix} fix, {t.satellites} uydu   |   Saat: {gps_saat}\n"
            f"Batarya: %{t.battery_percentage}  ({t.battery_voltage:.1f} V / {t.battery_current:.1f} A)   |   "
            f"MAVLink: {'Bağlı' if t.mavlink_bagli else 'Kopuk'}"
        )
