import socket
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Şifreleme parametreleri (AES anahtarı ve IV)
key = b"1234567890abcdef"  # 16 byte'lık AES anahtarı
iv = b"abcdef1234567890"   # 16 byte'lık IV

# AES CBC modunda veriyi çözen fonksiyon
def decrypt_data(encrypted_data):
    # AES CBC modunda şifre çözme objesi
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Şifrelenmiş veriyi çöz (padding dahil)
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

    # PKCS7 padding'i kaldır
    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    return decrypted

# Sunucu IP ve PORT ayarları
HOST = '0.0.0.0'  # Tüm ağ arayüzlerinden bağlantı kabul et
PORT = 5001       # Dinleme portu

# TCP socket oluştur ve dinleme moduna geç
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("[Sunucu] Bağlantı bekleniyor...")

# İstemciden gelen bağlantıyı kabul et
conn, addr = server_socket.accept()
print(f"[Sunucu] Bağlantı geldi: {addr}")

#  Kimlik doğrulama aşaması
auth_data = conn.recv(1024).decode()  # İstemciden parolayı al
if auth_data == "password123":
    conn.sendall(b"OK")  # Doğru parola ise "OK" gönder
    print("[Sunucu] Kimlik doğrulama başarılı!")
else:
    conn.sendall(b"NO")  # Yanlışsa "NO" gönder ve bağlantıyı kapat
    print("[Sunucu] Kimlik doğrulama hatalı. Bağlantı kapatılıyor.")
    conn.close()
    server_socket.close()
    exit()

#  Şifreli veriyi al ve buffer'a topla
encrypted_data = b""
while True:
    data = conn.recv(4096)  # 4 KB'lık parçalarla veri al
    if not data:
        break
    encrypted_data += data  # Gelen veriyi birleştir

# Son 64 byte, SHA-256 hash değeri (hex string)
client_hash = encrypted_data[-64:]     # İstemcinin gönderdiği hash
encrypted_data = encrypted_data[:-64]  # Asıl şifreli dosya verisi

#  Şifreyi çöz ve dosya olarak kaydet
decrypted_data = decrypt_data(encrypted_data)
with open("alinan_dosya.bin", "wb") as f:
    f.write(decrypted_data)

print("[Sunucu] Dosya başarıyla alındı ve çözüldü.")

#  SHA-256 bütünlük doğrulaması
sha256 = hashlib.sha256()
with open("alinan_dosya.bin", "rb") as f:
    while True:
        data = f.read(4096)  # Dosyayı 4 KB'lık parçalara bölerek oku
        if not data:
            break
        sha256.update(data)
server_hash = sha256.hexdigest().encode()  # Hesaplanan hash'i hex olarak al

# İstemciden gelen hash ile karşılaştır
if client_hash == server_hash:
    print("[Sunucu] SHA-256 bütünlük doğrulaması BAŞARILI!")
else:
    print("[Sunucu] SHA-256 bütünlük doğrulaması BAŞARISIZ!")

# Bağlantı ve socket'i kapat
conn.close()
server_socket.close()
