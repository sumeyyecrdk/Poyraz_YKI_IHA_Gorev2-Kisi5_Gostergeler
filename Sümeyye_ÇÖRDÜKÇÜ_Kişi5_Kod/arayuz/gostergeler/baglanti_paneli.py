from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSlot

# (görüntü adı, hat_durumu_guncelle çağrılarında kullanılan anahtar) — anahtarlar
# docstring'deki kullanım örneğiyle (gcs_pencere.py) birebir aynı olmalı.
# burada 2 ayrı isim gerekiyor. ekranda görünecek isim / programın arka planda kullanacağı kısa isim şeklinde
_HATLAR = [
    ("Uçak (MAVLink)", "MAVLink"),
    ("Görev Bilgisayarı", "Görev Bil."),
    ("Sunucu", "Sunucu"),
]

# bağlı ve kopuk durumlarından hareketle oluşacak renk ayarı yapıldı.
_RENK_BAGLI = "#2ea043"
_RENK_KOPUK = "#da3633"


class BaglantiPaneli(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._hat_satirlari = {}  # {hat_adi: status_line widget}
        self._kur()

    def _kur(self) -> None:
        #panelin arka planını siyah yapıyoruz,kenarlık yok
        self.setStyleSheet("background-color: #000000; border: none;")

        # layout isimli dikey sıralama yapan bir düzenleyici oluşturuldu. panel buna bağlandı.
        # panelin kenarları ile içindeki elemanlar arasındaki boşluklar ayarlandı.
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        # üzerinde SİSTEM BAĞLANTILARI yazan bir metin kutusu(QLabel) oluşturuldu. Bu metin kutusunun stili ayarlandı ve layout' a eklendi.
        baglanti_label = QLabel("  ►  SİSTEM BAĞLANTILARI")
        baglanti_label.setStyleSheet(
            "color: #58a6ff; font-weight: bold; font-size: 14px; border: none; "
            "border-left: 5px solid #58a6ff; background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #111d2e, stop:1 transparent); padding: 10px 15px; border-radius: 3px;"
        )
        layout.addWidget(baglanti_label)

        # çevrimdışı bir değişkende BAĞLAN butonunun nasıl görüneceği ayarlandı.
        btn_style = (
            "QPushButton { background: transparent; border: 1px solid #30363d; border-radius: 4px; color: #f0f6fc; font-weight: bold; padding: 8px; font-size: 13px; } "
            "QPushButton:hover { background: #30363d; border-color: #58a6ff; } "
            "QPushButton:pressed { background: #161b22; color: #58a6ff; }"
        )

        # boş bir kutu oluşturuldu. bu kutu döngüde dönerkenki tek bir veriyi temsil edecek. bunları yatay sıralayan bir düzenleyici oluşturuldu ve boş kutuya bağlandı. 
        for name, hat_adi in _HATLAR:
            row_widget = QWidget()
            row_lay = QHBoxLayout(row_widget)
            row_lay.setContentsMargins(5, 5, 5, 5)
 
            # üzerinde dönüşteki name değeri yazan bir metin kutusu oluşturuldu. bu metin kutusunun genişliği ayarlandı
            lbl = QLabel(name)
            lbl.setFixedWidth(90)
            lbl.setStyleSheet("font-weight: bold; color: #8b949e; border: none; font-size: 14px;")

            # bir çerçeve nesnesi oluşturuldu, bu o satırın durum çizgisi olacaktır. bu çerçevenin yatay bir çizgi olarak görülmesi sağlandı.
            # çizginin başlangıç rengi kopuk olduğu zamanki yani kırmızı rengine ayarlandı. program yeni açıldığında henüz bir bağlantı kurulmadığı için default olarak böyle ayarlandı.
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFixedHeight(3)
            line.setStyleSheet(f"background-color: {_RENK_KOPUK}; border: none;")
            # çizginin pencere genişledikçe genişlemesi, yükseklik yönünde uzadıkca sabit kalması ayarlandı.
            line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            # üzerinde BAĞLAN yazan bir buton yaratıldı, genişliği ayarlandı. düğme tıklanınca basılı durumda kalması sağlandı ve btn_style bu butona bağlandı.
            btn_status = QPushButton("BAĞLAN")
            btn_status.setFixedWidth(110)
            btn_status.setCheckable(True)
            btn_status.setStyleSheet(btn_style)

            # üretilen bu elemanlar yukarıda yaratılan boş kutuya eklendi.
            row_lay.addWidget(lbl)
            row_lay.addWidget(line)
            row_lay.addWidget(btn_status)

            # mini kutu, panelin ana dikey düzenleyicisine(layout) eklendi.
            layout.addWidget(row_widget)
            
            # listedeki hat_adi değişkenleri line değerine bağlandı.
            self._hat_satirlari[hat_adi] = line

        # üzerinde Sistem Hazır yazan bir metin kutusu oluşturuldu. rengi, stili ayarlandı ve panele eklendi.
        self.connection_status_log = QLabel("Sistem Hazır")
        self.connection_status_log.setStyleSheet("color: #58a6ff; font-size: 12px; border: none; padding-top: 5px;")
        self.connection_status_log.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.connection_status_log)

    @pyqtSlot(str, bool)

    # bağlantı bilgisi geldiğinde çalışan fonksiyon.
    def hat_durumu_guncelle(self, hat_adi: str, bagli: bool) -> None:

        #listeden gelen ürünlerin hat_adi karşılığında gelen çizgi nesnesi çekilip line değişkenine atandı.
        line = self._hat_satirlari.get(hat_adi)
        # eğer line, sözlükte tanımlı 3 elemandan biri değilse program durduruldu.
        if line is None:
            return
        
        # eğer bagli doğruysa renk değişkenine _RENK_BAGLI yani yeşil rengi atandı. Değilse _RENK_KOPUK yani kırmızı rengi atandı.
        renk = _RENK_BAGLI if bagli else _RENK_KOPUK
        # söz konusu olan line değişkeninin rengi yeni hesaplanan renk değişkenine göre güncellendi.
        line.setStyleSheet(f"background-color: {renk}; border: none;")
