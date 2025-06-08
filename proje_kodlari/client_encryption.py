import socket
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Şifreleme parametreleri (AES anahtarı ve IV)
key = b"1234567890abcdef"  # 16 byte'lık AES anahtarı
iv = b"abcdef1234567890"   # 16 byte'lık IV

# Veriyi AES CBC modunda şifreleyen fonksiyon
def encrypt_data(data):
    # AES CBC için PKCS7 padding uygulanır
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # AES CBC modunda şifreleme objesi oluştur
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Veriyi şifrele ve döndür
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted

# Sunucu IP ve PORT ayarları
HOST = '127.0.0.1'  # Sunucu IP (localhost)
PORT = 5001         # Sunucu portu

# TCP bağlantısı oluştur ve sunucuya bağlan
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

#  Kimlik doğrulama süreci
client_socket.sendall(b"password123")  # Sunucuya parolayı gönder
auth_response = client_socket.recv(1024)  # Sunucudan yanıt al
if auth_response != b"OK":  # Yanıt "OK" değilse bağlantıyı kapat
    print("[İstemci] Kimlik doğrulama başarısız! Çıkılıyor...")
    client_socket.close()
    exit()
print("[İstemci] Kimlik doğrulama başarılı, dosya gönderimine başlanıyor.")

#  Dosya okuma ve şifreleme
file_path = "gonderilecek_dosya.bin"  # Gönderilecek dosya adı
with open(file_path, "rb") as f:
    file_data = f.read()  # Dosyanın tamamını oku

# Dosya verisini şifrele
encrypted_data = encrypt_data(file_data)

# Şifreli veriyi sunucuya gönder
client_socket.sendall(encrypted_data)
print("[İstemci] Şifreli dosya gönderimi tamamlandı.")

#  SHA-256 bütünlük kontrolü için dosya hash'i hesapla
sha256 = hashlib.sha256()
with open(file_path, "rb") as f:
    while True:
        data = f.read(4096)  # 4 KB'lık parçalarla oku
        if not data:
            break
        sha256.update(data)
hash_digest = sha256.hexdigest().encode()  # Hash'i hex formatına çevir

# Hesaplanan SHA-256 hash'i sunucuya gönder
client_socket.sendall(hash_digest)
print("[İstemci] SHA-256 gönderildi, işlem tamamlandı.")

# Bağlantıyı kapat
client_socket.close()
