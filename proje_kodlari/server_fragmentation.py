import socket

# Sunucu IP ve PORT ayarları
HOST = '0.0.0.0'    # Tüm arayüzlerden bağlantı kabul et
PORT = 5001         # Dinleme yapılacak port

# TCP socket oluştur ve bağlantıya hazırla
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))  # IP ve portu ata
server_socket.listen(1)           # Maksimum 1 istemciyi bekle

print("[Sunucu] Bağlantı bekleniyor...")

# İstemciden gelen bağlantıyı kabul et
conn, addr = server_socket.accept()
print(f"[Sunucu] Bağlantı geldi: {addr}")

# Gelen verileri kaydetmek için dosya aç
with open("alinan_dosya.bin", "wb") as f:
    while True:
        # İstemciden 4096 baytlık veri oku (4 KB)
        data = conn.recv(4096)
        if not data:            # Veri yoksa (bağlantı kapandıysa) döngüden çık
            break
        f.write(data)           # Alınan veriyi dosyaya ekle

print("[Sunucu] Dosya başarıyla alındı.")

# Bağlantı ve socket'i kapat
conn.close()
server_socket.close()
