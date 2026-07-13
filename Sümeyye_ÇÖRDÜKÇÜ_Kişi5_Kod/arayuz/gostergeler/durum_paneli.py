from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSlot
from core.veri_modeli import TelemetriVerisi


class DurumPaneli(QWidget):
    
    #nesne üretildiğinde otomatik çalışan fonksiyon
    def __init__(self, parent=None):
        super().__init__(parent)
        self._kur()

    def _kur(self) -> None:
        
        self.setStyleSheet("background: transparent; border: none;")
        
        #bir grid nesnesi üretildi. kenar boşlukları ayarlandı.satırlar ve sütunlar arası boşluklar ayarlandı.
        layout = QGridLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setVerticalSpacing(10)
        layout.setHorizontalSpacing(15)

        # üzerinde "ARAÇ DURUM" yazan bir etiket nesnesi üretildi. yazı merkezde olacak şekilde ayarlandı.yazının stili,rengi belirlendi.
        durum_label = QLabel("ARAÇ DURUM")
        durum_label.setAlignment(Qt.AlignCenter)
        durum_label.setStyleSheet("color:#58a6ff; font-size: 13px; font-weight: bold; background: transparent; border: none;")
        
        # aynı şeyler "ARAÇ MODU" ve "WAYPOINT" etiketleri içinde yazıldı.
        mod_label = QLabel("ARAÇ MODU")
        mod_label.setAlignment(Qt.AlignCenter)
        mod_label.setStyleSheet("color:#58a6ff; font-size: 13px; font-weight: bold; background: transparent; border: none;")

        wp_label = QLabel("WAYPOINT")
        wp_label.setAlignment(Qt.AlignCenter)
        wp_label.setStyleSheet("color:#58a6ff; font-size: 13px; font-weight: bold; background: transparent; border: none;")

        # programın yeni açıldığı, henüz telemetri gelmediği durumda defalut olarak DISARM ile başlandı.
        # bununla paralel olarak "henüz aktif değil" mesajı için kırmızı yazı kullanıldı.(bu kontrol_paneli.py'deki ARM/DISARM buton renklendirmesiyle ilgili bir kural)
        self.ucakarm = QLabel("DISARM")
        self.ucakarm.setAlignment(Qt.AlignCenter)
        self.ucakarm.setStyleSheet("color:red; font-size: 16px; font-weight: bold; background: transparent; border: none;")

        # mod bilgisi henüz gelmediği için yanıltıcı bir şey göstermek yerine bilinmiyor anlamına gelen "UNKNOWN" ifadesi yazıldı.
        # nötr bir bilgiyle paralel olarak bu yazının rengi de gri tonlu bir şekilde ayarlandı.
        self.ucakmod = QLabel("UNKNOWN")
        self.ucakmod.setAlignment(Qt.AlignCenter)
        self.ucakmod.setStyleSheet("color:#f0f6fc; font-size: 16px; font-weight: bold; background: transparent; border: none;")

        # henüz bir yol noktası bilgisi gelmedi. bu yüzden default olarak 0 şeklinde yazıldı. yine nötr ifadeye bununla paralel gri tonlu bir renk ayarlandı.
        self.next_wp = QLabel("WP: 0")
        self.next_wp.setAlignment(Qt.AlignCenter)
        self.next_wp.setStyleSheet("color:#f0f6fc; font-size: 16px; font-weight: bold; background: transparent; border: none;")

        # Grid'e ekleme
        layout.addWidget(durum_label, 0, 0)
        layout.addWidget(self.ucakarm, 1, 0)

        layout.addWidget(mod_label, 0, 1)
        layout.addWidget(self.ucakmod, 1, 1)

        layout.addWidget(wp_label, 0, 2)
        layout.addWidget(self.next_wp, 1, 2)

    @pyqtSlot(object)
    def guncelle(self, t: TelemetriVerisi) -> None:
        
        # arm durumu "ARM" ise etiket yazısı ARM şeklinde ayrlanıyor ve istendiği gibi bu ayarlamada yeşil renk kullanılıyor.
        if t.armed:
            self.ucakarm.setText("ARM")
            self.ucakarm.setStyleSheet("color:#2ea043; font-size: 16px; font-weight: bold; background: transparent; border: none;")
        # arm durumu "DISARM" ise etiket yazısı DISARM şeklinde ayarlanıyor ve istenediği gibi bu ayarlamada kırmızı renk kullanılıyor.
        else:
            self.ucakarm.setText("DISARM")
            self.ucakarm.setStyleSheet("color:red; font-size: 16px; font-weight: bold; background: transparent; border: none;")
        
        # telemetri paketindeki mod bilgisi (bu zaten bir string) doğrudan self.ucakmod etikteine yazdırıldı.
        self.ucakmod.setText(t.mode)
        # telemetri paketindeki next_waypoint alanı fstring formatıyla yazdırıldı.
        self.next_wp.setText(f"WP: {t.next_waypoint}")