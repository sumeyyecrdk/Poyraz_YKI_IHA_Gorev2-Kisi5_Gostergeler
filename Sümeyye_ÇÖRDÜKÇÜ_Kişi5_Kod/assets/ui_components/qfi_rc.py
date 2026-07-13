"""
arayuz/gostergeler/qfi/*.py dosyalarının hepsi şu satırla bu modülü arıyor:
    from assets.ui_components import qfi_rc

Görev tanımı "qfi/ klasörü dokunulmaz" dediği için o dosyalara hiç
dokunulmadı. Ancak proje zip'inde bu dosyanın/klasörün kendisi eksikti
— bu yüzden qfi widget'ları hiç import edilemiyor, program açılmıyordu.

Gerçek Qt kaynak verisi (SVG grafikleri) zaten projede,
arayuz/gostergeler/qfi/qfi_rc.py içinde duruyor. Bu dosya sadece o
gerçek modüle yönlendirme yapıyor, hiçbir veriyi değiştirmiyor/
kopyalamıyor.
"""
from arayuz.gostergeler.qfi.qfi_rc import *  # noqa: F401,F403
