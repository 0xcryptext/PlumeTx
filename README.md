## Kullanım

Botu çalıştırmadan önce aşağıdaki adımları takip edin:

### 1. `wallet.txt` ve `mainwallet.txt` Dosyalarını Hazırlama

- **wallet.txt**: Cüzdan adreslerini ve private key'lerini içermelidir. Cüzdanları aşağıdaki formata uygun şekilde ekleyin:
  ```
  adres1, privateKey1
  adres2, privateKey2
  ```

- **mainwallet.txt**: Ana cüzdan adresini ve private key'ini ekleyin (sadece 1 cüzdan).
  ```
  mainWalletAdres, mainWalletPrivateKey
  ```

### 2. Sanal Ortamı Kurma

1. **Sanal ortam kurma**:

   Windows:
   ```bash
   python -m venv venv
   ```

   Linux/MacOS:
   ```bash
   python3 -m venv venv
   ```

2. **Sanal ortamı aktif hale getirme**:

   Windows:
   ```bash
   .\venv\Scripts\activate
   ```

   Linux/MacOS:
   ```bash
   source venv/bin/activate
   ```

### 3. Web3 ve Diğer Bağımlılıkları Yükleme

Web3 kütüphanesini yüklemek için terminalde aşağıdaki komutu çalıştırın:

```bash
pip install web3
```

### 4. Botu Çalıştırma

Botu çalıştırmak için şu komutu yazın:

```bash
python main.py
```

Botu başlattığınızda aşağıdaki seçenekler sunulacaktır:

1. **Cüzdanlara ETH Gönder**: Ana cüzdandan `wallet.txt` dosyasındaki her bir cüzdana ETH gönderir.
2. **TX Kas**: ETH miktarını belirleyerek, belirtilen adreslere işlem gönderimi yapar.
3. **Çıkış**: Botu kapatır.

### 5. İşlem Seçimi

Bot çalıştıktan sonra, menüdeki işlemleri seçebilirsiniz. Her işlem için ETH miktarlarını girmeniz gerekecek.

### 6. ETH Gönderme İşlemi

**Cüzdanlara ETH Gönder** seçeneğini seçtiğinizde:

- Bot, **mainwallet.txt** dosyasındaki ana cüzdandan, **wallet.txt** dosyasındaki her bir cüzdana belirli bir miktar ETH gönderecektir.
- Gönderim işlemleri arasında 5-12 saniye beklenir.

### 7. TX Kasma İşlemi

**TX Kas** seçeneğini seçtiğinizde:

- Belirtilen ETH miktarı ile işlem (TX) yapılacaktır.
