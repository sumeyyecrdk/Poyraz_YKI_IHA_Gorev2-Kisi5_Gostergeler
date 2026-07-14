# Poyraz_YKI_IHA_Gorev2-Kisi5_Gostergeler

 Bu depo, Poyraz Yer Kontrol İstasyonu (YKI) projesinin 2. görevi kapsamında hazırladığım **Kişi 5 (Uçuş Göstergeleri)** modülünün kodlarını içermektedir. 

Bu projede amacım, bir İHA'nın havada süzülürken ihtiyaç duyduğu temel uçuş verilerini ekranda dinamik ve anlaşılır bir şekilde görselleştirmekti.

## Neler Yaptım? (Özellikler)

Arayüz üzerinde İHA'nın anlık durumunu takip edebilmek için şu temel göstergeleri hazırladım:

*   **Yapay Ufuk:** İHA'nın sağa-sola yatış (roll) ve yukarı-aşağı yönelim (pitch) hareketlerini gösteriyor.
*   **Hız ve Yükseklik Barları:** İHA'nın o anki hızını ve ne kadar yüksekte olduğunu canlı olarak takip etmeyi sağlıyor.
*   **Pusula:** İHA'nın hangi yöne (açıya) doğru gittiğini gösteriyor.

## Klasör Yapısı 
Projeyi daha düzenli tutabilmek için dosyaları şu şekilde ayırdım:
*  **`arayuz/`**: Göstergelerin çizimlerini ve ekran tasarımlarını yazdığım asıl kod dosyalarım burada yer alıyor.
*  **`assets/`**: Kod içerisindeki görsel kaynakların import yollarında (`ModuleNotFoundError: No module named 'assets'`) hata alınmaması ve kütüphane kaynaklarının (`qfi_rc.py`) sorunsuz import edilebilmesi için yapılandırdığım teknik klasördür.
*  **`test_kisi5.py`**: Projeyi çalıştırmak ve göstergelerin nasıl çalıştığını test etmek için kullandığım ana Python dosyası.
*   **`core.py`**: Test kodunu çalıştırabilmek için dosyaya dahil edildi.

---
**Hazırlayan:** Sümeyye Çördükçü (Kişi 5 - Göstergeler Modülü)
