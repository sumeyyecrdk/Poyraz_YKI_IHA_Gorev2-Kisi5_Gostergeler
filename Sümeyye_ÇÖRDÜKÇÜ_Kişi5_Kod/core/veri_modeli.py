"""
core/veri_modeli.py
===================
BTU-Poyraz YKİ — Modüller Arası Ortak Veri Sözleşmesi

Bu dosyayı YALNIZCA Kişi 6 düzenler.
Diğer herkes sadece import eder:
    from core.veri_modeli import TelemetriVerisi, RakipIha
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


# ---------------------------------------------------------------------------
# Rakip renk paleti — takim_no % len(PALET) ile renk seçilir
# Haritada her rakip farklı renkte gösterilir
# ---------------------------------------------------------------------------
RAKIP_RENK_PALETI = [
    "#e74c3c",  # kırmızı
    "#3498db",  # mavi
    "#2ecc71",  # yeşil
    "#f39c12",  # turuncu
    "#9b59b6",  # mor
    "#1abc9c",  # turkuaz
    "#e67e22",  # koyu turuncu
    "#e91e63",  # pembe
]

def rakip_rengi(takim_no: int) -> str:
    """Takım numarasına göre tekrarlamalı renk döndürür."""
    return RAKIP_RENK_PALETI[takim_no % len(RAKIP_RENK_PALETI)]


# ---------------------------------------------------------------------------
# Rakip İHA Verisi (Kişi 3 — SunucuThread doldurur, Kişi 4 gösterir)
# ---------------------------------------------------------------------------
@dataclass
class RakipIha:
    """
    Yarışma sunucusundan gelen rakip İHA bilgisi.

    Haritada gösterilecek 3 zorunlu bilgi (şartname teknik kontrol):
        takim_no  → balon/popup başlığı
        irtifa    → metre cinsinden (sunucudan int gelir)
        hiz       → m/s cinsinden (sunucudan int gelir)

    Kullanım (harita_paneli.py içinde):
        for rakip in rakip_listesi:
            renk = rakip_rengi(rakip.takim_no)
            # haritaya işaretle: ikon rengi=renk
            # popup içeriği: f"#{rakip.takim_no}  {rakip.irtifa}m  {rakip.hiz}m/s"
    """
    takim_no:  int   = 0
    enlem:     float = 0.0
    boylam:    float = 0.0
    irtifa:    int   = 0     # metre
    hiz:       int   = 0     # m/s
    yonelme:   float = 0.0   # derece (ok yönü için)

    @property
    def renk(self) -> str:
        return rakip_rengi(self.takim_no)

    @staticmethod
    def sunucu_yaniti_parse(ham_liste: list) -> "List[RakipIha]":
        """
        Sunucudan gelen ham JSON listesini RakipIha listesine çevirir.
        Kişi 3'ün sunucu_thread.py'si bunu çağırır.

        Beklenen ham format (haberleşme dokümanına göre):
            [
              {"takim_numarasi": 5, "iha_enlem": 40.1, "iha_boylam": 29.2,
               "iha_irtifa": 150, "iha_hiz": 25, "iha_yonelme": 180},
              ...
            ]
        """
        # TODO: Kişi 3 burayı dolduracak
        pass


# ---------------------------------------------------------------------------
# HSS / Sinyal Karıştırma Bölgesi (şartname zorunlu — haritada kırmızı daire)
# ---------------------------------------------------------------------------
@dataclass
class HssBolgesi:
    """
    Hava Savunma Sistemi veya sinyal karıştırma bölgesi.
    Aktif olduğunda haritada kırmızı yarı-saydam daire olarak gösterilir.

    Şartname: HSS aktifken bu bölgede her tam saniye -5 ceza puanı.
    30 saniye geçilirse iniş zorunlu.
    """
    enlem:  float = 0.0
    boylam: float = 0.0
    yaricap: int  = 0    # metre
    aktif:  bool  = False


# ---------------------------------------------------------------------------
# Ana İHA Telemetri Verisi (Kişi 1 — MavlinkThread doldurur)
# ---------------------------------------------------------------------------
@dataclass
class TelemetriVerisi:
    """
    Tüm modüller arası ortak veri nesnesi.

    Doldurma sorumluluğu:
        Modül A (mavlink_thread)           → MAVLink alanları
        Modül B (gorev_bilgisayari_thread) → Görev bilgisayarı alanları
        Modül C (sunucu_thread)            → sadece OKUR + to_sunucu_paketi() çağırır
        Modül D (harita_paneli)            → sadece OKUR
        Modül E (gostergeler)              → sadece OKUR

    Sinyal tipi: pyqtSignal(object)  — TelemetriVerisi nesnesi taşır
    """

    # ── MAVLink / SITL (Kişi 1 doldurur) ────────────────────────────────────
    latitude:           float = 0.0    # derece
    longitude:          float = 0.0    # derece
    altitude:           float = 0.0    # metre MSL
    relative_altitude:  float = 0.0    # metre AGL
    groundspeed:        float = 0.0    # m/s
    airspeed:           float = 0.0    # m/s
    heading:            float = 0.0    # derece 0-360
    pitch:              float = 0.0    # radyan
    roll:               float = 0.0    # radyan
    yaw:                float = 0.0    # radyan
    climb_rate:         float = 0.0    # m/s

    battery_voltage:    float = 0.0    # Volt
    battery_current:    float = 0.0    # Amper
    battery_percentage: int   = 0      # %

    gps_fix:            int   = 0      # 0=yok 2=2D 3=3D
    satellites:         int   = 0

    armed:              bool  = False
    mode:               str   = "UNKNOWN"
    next_waypoint:      int   = 0

    gps_saat:           int   = 0
    gps_dakika:         int   = 0
    gps_saniye:         int   = 0
    gps_milisaniye:     int   = 0

    mavlink_bagli:      bool  = False

    # ── Görev Bilgisayarı / Raspberry Pi (Kişi 2 doldurur) ──────────────────
    kamera_aktif:       bool  = False
    hedef_x:            int   = 0      # piksel — kilitlenme dörtgeni sol üst X
    hedef_y:            int   = 0      # piksel — kilitlenme dörtgeni sol üst Y
    hedef_genislik:     int   = 0      # piksel
    hedef_yukseklik:    int   = 0      # piksel
    kilitlenme_aktif:   bool  = False  # True → hedef 4 sn kilitli (şartname vuruş)

    gb_cpu_yuzde:       float = 0.0
    gb_ram_yuzde:       float = 0.0
    gb_sicaklik:        float = 0.0
    gb_baglanti:        bool  = False

    # ── Yardımcı ─────────────────────────────────────────────────────────────
    @property
    def pitch_deg(self) -> float:
        import math; return math.degrees(self.pitch)

    @property
    def roll_deg(self) -> float:
        import math; return math.degrees(self.roll)

    @property
    def yaw_deg(self) -> float:
        import math; return math.degrees(self.yaw) % 360

    @property
    def otonom_mu(self) -> bool:
        return self.mode.upper() in {"AUTO", "GUIDED", "RTL", "TAKEOFF"}

    def to_sunucu_paketi(self, takim_no: int) -> dict:
        """
        Yarışma sunucusunun beklediği paketi oluşturur.
        Kişi 3'ün sunucu_thread.py'si bunu çağırır.
        """
        return {
            "takim_numarasi": int(takim_no),
            "iha_enlem":      round(self.latitude,  7),
            "iha_boylam":     round(self.longitude, 7),
            "iha_irtifa":     int(round(self.altitude)),
            "iha_dikilme":    int(round(self.pitch_deg)),
            "iha_yonelme":    int(round(self.yaw_deg)) % 360,
            "iha_yatis":      int(round(self.roll_deg)),
            "iha_hiz":        int(round(self.groundspeed)),
            "iha_batarya":    int(self.battery_percentage),
            "iha_otonom":     self.otonom_mu,
            "iha_kilitlenme": self.kilitlenme_aktif,
            "hedef_merkez_X":  int(self.hedef_x),
            "hedef_merkez_Y":  int(self.hedef_y),
            "hedef_genislik":  int(self.hedef_genislik),
            "hedef_yukseklik": int(self.hedef_yukseklik),
            "gps_saati": {
                "saat":       int(self.gps_saat),
                "dakika":     int(self.gps_dakika),
                "saniye":     int(self.gps_saniye),
                "milisaniye": int(self.gps_milisaniye),
            },
        }
