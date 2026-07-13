from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QFrame,
)
from PyQt5.QtCore import Qt, pyqtSignal

# Şartname/KTR'e göre desteklenen uçuş modları (otonom algoritmalara dokunulmuyor,
# mod isimleri sadece MAVLink'e gönderilecek string'ler)
UCUS_MODLARI = ["MANUAL", "STABILIZE", "FBWA", "AUTO", "GUIDED", "RTL", "TAKEOFF"]

#QWidget'tan miras alan KontrolPaneli sınıfı üretildi.
class KontrolPaneli(QWidget):
    # ── Dışa açık sinyaller ──

    #bu zil çalarken hiçbir ek bilgi göndermiyor sadece "bir şey oldu diyor". mesela burada "ARM butonun basıldı" bilgisi yeterlidir.
    arm_istendi = pyqtSignal()
    disarm_istendi = pyqtSignal()
    kalkis_istendi = pyqtSignal()
    inis_istendi = pyqtSignal()
    serbest_rota_istendi = pyqtSignal()

    #bu zil çalarken beraberinde bir string de gönderiyor. çünkü "mod değiştir" butonu tetiklendiğinde hangi moda geçileceği bilgisi de lazım.
    mod_degistir_istendi = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._kur()

    def _kur(self) -> None:
        self.setStyleSheet("background-color: #000000; border: none;")

        #satır ve sütunlardan oluşan bir tablo oluşturuldu. kenar boşlukları ayarlandı.griddek hücreler arasındaki boşluk ayarlandı.
        grid = QGridLayout(self)
        grid.setContentsMargins(8, 4, 8, 4)
        grid.setSpacing(6)

        # etiketlerdeki yazılar için kullanılacak ortak stil
        label_style = (
            "color: #58a6ff; font-weight: bold; font-size: 13px; border: none; "
            "border-left: 3px solid #58a6ff; "
            "background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #111d2e, stop:1 transparent); "
            "padding: 2px 8px; border-radius: 3px;"
        )
        # tüm butonlar için kullanılacak ortak stil
        btn_style = (
            "QPushButton { min-height: 28px; font-size: 13px; font-weight: 600; "
            "background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #21262d, stop:1 #161b22);} "
            "QPushButton:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #30363d, stop:1 #21262d); border-color: #58a6ff; color: #ffffff; } "
            "QPushButton:pressed { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #161b22, stop:1 #0d1117); border-color: #1f6feb; color: #58a6ff; }"
        )

        # Navigasyon Butonları
        # hazır yazı stili ayarlandı ve yazılar dikeyde ortalandı.
        nav_label = QLabel("  ►  NAVİGASYON")
        nav_label.setStyleSheet(label_style)
        nav_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # üzerinde "KALKIŞ" yazan bir buton nesnesi üretildi.yukarıda tutulan buton stili uygulandı
        btn_kalkis = QPushButton("KALKIŞ")
        btn_kalkis.setStyleSheet(btn_style)
        #emit fonksiyonu bir referans olarak connect'e verildi henüz çalışmadı, sadece ileride clicked sinyali tetiklenirse o zaman bu fonskiyon çağırılsın diye kayıt bırakıldı.
        btn_kalkis.clicked.connect(self.kalkis_istendi.emit)

        #aynı işlemler "İNİŞ" ve "SERBEST ROTA" için tekrarlandı.
        btn_inis = QPushButton("İNİŞ")
        btn_inis.setStyleSheet(btn_style)
        btn_inis.clicked.connect(self.inis_istendi.emit)

        btn_rota = QPushButton("SERBEST ROTA")
        btn_rota.setStyleSheet(btn_style)
        btn_rota.clicked.connect(self.serbest_rota_istendi.emit)

        #soldan sağa: [başlık][KALKIŞ][İNİŞ][SERBEST ROTA] şeklinde 4 kutu yan yana eklendi.
        grid.addWidget(nav_label, 0, 0)
        grid.addWidget(btn_kalkis, 0, 1)
        grid.addWidget(btn_inis, 0, 2)
        grid.addWidget(btn_rota, 0, 3)

        # Ayırıcı Çizgi
        separator = QFrame()
        #HLine, QFrame sınıfının içinde tanımlı hazır bir sabit. Yatay çizgi şeklinde çerçevenin çizilmesini sağlar.
        separator.setFrameShape(QFrame.HLine)
        #bu çizginin hangi satır ve sütundan başlayıp kaç satır ve sütun kaplayacağı belirlenerek widget'a eklendi.
        #bu şekilde navigasyon bölümü ile araç kontrol bölümü arası görsel olarak bölümlere ayrıldı.
        separator.setStyleSheet("background-color: #30363d; border: none; max-height: 1px;")
        grid.addWidget(separator, 1, 0, 1, 4)

        # Araç Kontrol Butonları
        # hazır yazı stili ayarlandı ve yazılar dikeyde ortalandı.
        ctrl_label = QLabel("  ►  ARAÇ KONTROL")
        ctrl_label.setStyleSheet(label_style)
        ctrl_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # üzerinde "ARM" yazan bir buton nesnesi üretildi.yukarıda tutulan buton stili uygulandı ve buton tetiklendiğinde çağrılacak fonksiyon kayıt edildi.
        btn_arm = QPushButton("ARM")
        btn_arm.setObjectName("armButton")   # global STYLE_SHEET (gcs_pencere) rengini devralır
        btn_arm.setStyleSheet(btn_style)
        btn_arm.clicked.connect(self.arm_istendi.emit)
  
        # aynı işlemler "DISARM" butonu için tekrarlandı.
        btn_disarm = QPushButton("DİSARM")
        btn_disarm.setObjectName("disarmButton")
        btn_disarm.setStyleSheet(btn_style)
        btn_disarm.clicked.connect(self.disarm_istendi.emit)

        # Mod seçimi + SET butonu
        #boş sade bir konteyner widget'ı üretildi.
        mod_widget = QWidget()
        mod_widget.setStyleSheet("border: none;")
        #yeni bir düzen üretildi ve bu düzenin mod_widget'a ait olduğu belirtildi.
        mod_lay = QHBoxLayout(mod_widget)
        mod_lay.setContentsMargins(0, 0, 0, 0)
        #ComboBox ile SET butonu arasındaki mesafe ayarlandı.
        mod_lay.setSpacing(4)

        # UCUS_MODLARI listesindeki elemanları içeren bir liste widget'ı üretildi.
        self.comboBox = QComboBox()
        self.comboBox.addItems(UCUS_MODLARI)
        #bu liste widget'ının stili ayarlandı.
        self.comboBox.setStyleSheet(
            "QComboBox { background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #21262d, stop:1 #161b22); "
            "color: #f0f6fc; border: 1px solid #30363d; border-radius: 8px; padding: 4px 12px; "
            "font-size: 13px; font-weight: 600; min-height: 28px; } "
            "QComboBox:hover { border-color: #58a6ff; } "
            #drop-down:liste widget'ının tıklanınca listeyi açan ok bölümü.ComboBox gibi birden fazla iç parçası olan widgetların her bir parçasını ayrı ayrı stillendirmesi için :: kullanıldı
            "QComboBox::drop-down { border: none; width: 20px; } "
            "QComboBox::down-arrow { image: none; border-left: 4px solid transparent; "
            "border-right: 4px solid transparent; border-top: 6px solid #58a6ff; margin-right: 6px; } "
            "QComboBox QAbstractItemView { background-color: #161b22; color: #f0f6fc; "
            "border: 1px solid #30363d; selection-background-color: #21262d; } "
        )

        # SET butonu diğer butonlardan farklı bir stil kullanıyor çünkü bu buton görse olarak daha belirgin/vurgulu olması gerekn bir "onayla/uygula" butonu.
        btn_set_mod = QPushButton("SET")
        btn_set_mod.setStyleSheet(
            "QPushButton { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #388bfd, stop:1 #58a6ff); "
            "color: #fff; border: none; border-radius: 10px; font-size: 13px; font-weight: bold; "
            "padding: 5px 10px; min-width: 40px; min-height: 24px; letter-spacing: 1px; } "
            "QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #79c0ff, stop:1 #388bfd); color: #fff; } "
            "QPushButton:pressed { background: #1f6feb; color: #fff; }"
        )
        #lambda isme gerek kalmadan bir fonksiyon üretmemize yardımcı oldu. direkt emit diye çağıramazdık burada çünkü emiti parametresiz çağırmamız gerekirdi.
        #ancak mod değiştirme işleminde mod parametre olarak girilmeli.bu yüzden buna uygun bir fonksiyon gövdesi lambda ile yazıldı.
        btn_set_mod.clicked.connect(
            lambda: self.mod_degistir_istendi.emit(self.comboBox.currentText())
        )

        # ComboBox ve SET butonu iç mod_lay layout'una eklendi.
        mod_lay.addWidget(self.comboBox)
        mod_lay.addWidget(btn_set_mod)

        #ikinci satır gride'e yerleştirildi. (çünkü 0=navigasyon,1=ayırıcı çizgi)
        grid.addWidget(ctrl_label, 2, 0)
        grid.addWidget(btn_arm, 2, 1)
        grid.addWidget(btn_disarm, 2, 2)
        #burada grid'in bakış açısından hücreye tek bir widget yerleştirildi ancak o widget'ın içinde 2 ayrı eleman(ComboBox + SET butonu) saklı
        grid.addWidget(mod_widget, 2, 3)

        #pencere kullanıcı tarafından yeniden boyutlandırılabilir.bu satırlarda genişlik değiştiğinde bu fazla veya eksik alanın grid'in hangi sütunlarına ve ne oranla dağıtılacağı belirlendi.
        grid.setColumnStretch(0, 15)
        grid.setColumnStretch(1, 28)
        grid.setColumnStretch(2, 28)
        grid.setColumnStretch(3, 28)

        #aynı mantık ancak bu sefer satırlar için yapıldı.0. ve 2. satır eşit oranda genişlesin ancak 1.satır değişmesin şeklinde ayarlandı.
        #çünkü 1.satır ayırıcı çizgidir. bu çizginin her zaman aynı incelikle kalması istenir.
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 0)
        grid.setRowStretch(2, 1)