# 📡 Ağ Performans ve Güvenlik Analizi Projesi

Bu proje, bilgisayar ağlarının temel yapıtaşlarını (TCP/IP iletişimi, veri aktarımı, güvenlik önlemleri) test etmek ve analiz etmek için hazırlanmıştır. Python dilinde geliştirilen istemci-sunucu uygulaması, veri şifreleme, kimlik doğrulama ve dosya bütünlüğü sağlama işlevlerini desteklerken; Wireshark ve iperf3 gibi araçlarla ağ performansı detaylı şekilde ölçülmüştür.

## 🚀 Projede Yapılanlar

 **İstemci-Sunucu Dosya Transferi:**  
- TCP tabanlı bağlantı (127.0.0.1:5001) üzerinden dosya gönderimi ve alımı.  
- İstemci, dosyayı 4096 byte’lık parçalara bölerek gönderir.  
- Sunucu, gelen parçaları sırayla yazar ve dosyayı yeniden birleştirir.

 **Veri Şifreleme ve Kimlik Doğrulama:**  
- AES-CBC şifreleme (16 byte key ve IV) ile veri güvenliği sağlanır.  
- SHA-256 ile dosya bütünlük kontrolü yapılır.  
- Parola tabanlı kimlik doğrulama.

 **Düşük Seviyeli IP Başlık İşleme:**  
- `ip_raw_test.py` ile IP ve TCP başlıkları manuel oluşturulur.  
- Checksum manuel hesaplanır ve veri Wireshark ile gözlemlenir.

 **Saldırı Simülasyonu:**  
- `fake_packet_injection.py` ile sahte TCP SYN paketleri enjekte edilir.  
- Wireshark üzerinde sahte paketlerin algılanması sağlanır.

 **Ağ Performans Testleri:**  
- RTT (Round Trip Time) ölçümü: `ping` komutları (Wi-Fi ve VPN testleri).  
- Bant genişliği analizi: `iperf3` ile TCP/UDP testleri.  
- Paket kaybı yönetimi: `tc` komutu ile %10 paket kaybı simülasyonu ve iperf3 testleri.

## 🛠️ Gereksinimler

- Python 3.x  
- `cryptography`, `scapy` modülleri  
- Wireshark  
- iperf3  
- Linux (Ubuntu VM önerilir, raw socket için root yetkisi gerekir!)

## 🔧 Kurulum ve Kullanım

Proje ortamını hazırlamak için aşağıdaki adımları takip edebilirsiniz:

### 1️⃣ Bağımlılıkları Yükleyin

Python modülleri ve ağ test araçlarını kurmak için:

```bash 
pip install cryptography scapy
```

```bash 
sudo apt install iperf3 wireshark
```

### 2️⃣ Sunucuyu Başlatın

Veri alımını sağlayacak sunucu tarafını çalıştırın:

```bash
python server_fragmentation.py
```

### 3️⃣ İstemciyi Çalıştırın

Veriyi şifreleyip gönderecek istemciyi başlatın:

```bash
python client_fragmentation.py
```

### 4️⃣ Düşük Seviyeli IP Başlık Testi

Manuel IP başlık oluşturmayı test edin:

```bash
sudo python ip_raw_test.py
```
### 5️⃣ Sahte Paket Enjeksiyonu

Sahte paket gönderimiyle saldırı simülasyonunu deneyin:

```bash
sudo python fake_packet_injection.py
```

### 6️⃣ Ağ Performans Testleri

Wi-Fi, VPN gibi farklı ağlar için ping ve iperf3 ile gecikme ve bant genişliği analizleri yapın:

**RTT testi için:**

```bash
ping <hedef_ip>
```


**Bant genişliği testi için:**

```bash
iperf3 -s               # Sunucu
iperf3 -c <server_ip>   # İstemci
```



### 7️⃣ Paket Kaybı Simülasyonu

tc komutuyla ağ üzerinde paket kaybını simüle edebilirsiniz:

```bash
 # %10 paket kaybı oluştur

sudo tc qdisc add dev <arayüz> root netem loss 10%
```

```bash
 # Simülasyonu kaldır

sudo tc qdisc del dev <arayüz> root netem
```

## 📈 Sonuç ve Öneriler
Wi-Fi, VPN gibi farklı ağ türleri için performans testleri başarıyla yapılmıştır.

Şifreleme ve bütünlük kontrolleri, ağ üzerinden verinin gizli kalmasını sağlamıştır.

Gelecekte TLS/SSL gibi protokoller ve gelişmiş saldırı simülasyonları eklenerek proje geliştirilebilir.

## Proje Videosu
➡️ https://www.youtube.com/watch?v=Jpg6musObVI&t=2s

## 📚 Kaynakça
Kurose, J. F., & Ross, K. W. (2017). Computer Networking: A Top-Down Approach (7th ed.). Pearson.

Scapy. (n.d.). Scapy documentation. Retrieved from https://scapy.net

Iperf. (n.d.). iperf3 documentation. Retrieved from https://iperf.fr

Wireshark Foundation. (n.d.). Wireshark documentation. Retrieved from https://www.wireshark.org/docs/

Linux Foundation. (n.d.). tc(8) – Linux man page. Retrieved from https://linux.die.net/man/8/tc

OpenAI ChatGPT. (2025). OpenAI ChatGPT.
