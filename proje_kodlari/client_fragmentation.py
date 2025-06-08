import socket

# Sunucu IP ve PORT ayarları
HOST = '127.0.0.1'  # Sunucu IP (localhost)
PORT = 5001         # Sunucu portu

# Socket oluştur ve sunucuya bağlan
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Gönderilecek dosya
file_path = "gonderilecek_dosya.bin"  # Örnek test dosyası
with open(file_path, "rb") as f:
    while True:
        chunk = f.read(4096)          # 4 KB'lık parça oku
        if not chunk:                 # Dosya bitince çık
            break
        client_socket.sendall(chunk)  # Parçayı gönder

print("[İstemci] Dosya gönderimi tamamlandı.")
client_socket.close()
