from web3 import Web3
import time
import random

# Blockchain node URL'si (Sepolia Testnet Infura örneği)
RPC_URL = "https://sepolia.drpc.org"

# Bağlantıyı oluştur
web3 = Web3(Web3.HTTPProvider(RPC_URL))

def load_wallets(file_path):
    """Cüzdan adreslerini ve private key'leri bir dosyadan yükler."""
    wallets = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                wallet, private_key = line.strip().split(",")
                wallets.append((wallet, private_key))
    except FileNotFoundError:
        print(f"Dosya bulunamadı: {file_path}")
    return wallets

def load_main_wallet(file_path):
    """Ana cüzdan bilgilerini yükler."""
    try:
        with open(file_path, "r") as file:
            main_wallet, main_private_key = file.readline().strip().split(",")
            return main_wallet, main_private_key
    except FileNotFoundError:
        print(f"Dosya bulunamadı: {file_path}")
        return None, None

def get_amount_from_user(prompt):
    """Kullanıcıdan gönderilecek ETH miktarını alır ve Wei'ye çevirir."""
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("Miktar 0'dan büyük olmalıdır.")
                continue
            return web3.to_wei(amount, 'ether')
        except ValueError:
            print("Geçersiz değer. Lütfen geçerli bir ETH miktarı girin.")

def send_eth_to_wallets(main_wallet, main_private_key, wallets, amount_in_wei):
    """Ana cüzdandan diğer cüzdanlara ETH gönderir."""
    for wallet_address, _ in wallets:
        try:
            # Transaction oluştur
            transaction = {
                'from': main_wallet,
                'to': wallet_address,
                'value': amount_in_wei,
                'gas': 21000,
                'gasPrice': web3.to_wei(10, 'gwei'),
                'nonce': web3.eth.get_transaction_count(main_wallet),
                'chainId': 11155111  # Sepolia Testnet için EIP-155 Chain ID
            }

            # İşlemi imzala
            signed_txn = web3.eth.account.sign_transaction(transaction, private_key=main_private_key)

            # İşlemi gönder
            tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
            print(f"[{main_wallet}] {wallet_address} adresine ETH gönderildi. Hash: {web3.to_hex(tx_hash)}")

            # İşlemi doğrula
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"[{wallet_address}] Transaction onaylandı. Hash: {web3.to_hex(tx_hash)}")
        except Exception as e:
            print(f"[{main_wallet}] {wallet_address} adresine ETH gönderirken hata oluştu: {e}")
        
        # Her işlemden sonra 5 ile 12 saniye arasında rastgele bekle
        wait_time = random.uniform(5, 12)
        print(f"Bir sonraki gönderim için {wait_time:.2f} saniye bekleniyor...\n")
        time.sleep(wait_time)  # Rastgele bekleme süresi

def tx_loop(wallets, eth_amount):
    """TX Kas işlemi için döngü."""
    print("TX işlemi başlatılıyor...")
    send_eth_to_wallets(wallets[0][0], wallets[0][1], wallets, eth_amount)  # İlk wallet'ı kullanıyoruz

def main_menu():
    """Ana menü arayüzü."""
    wallets = load_wallets("wallet.txt")
    main_wallet, main_private_key = load_main_wallet("mainwallet.txt")

    if not wallets:
        print("Hiçbir cüzdan yüklenmedi.")
        return
    if not main_wallet or not main_private_key:
        print("Ana cüzdan yüklenemedi.")
        return

    while True:
        print("\n--- Bot Menüsü ---")
        print("1. Cüzdanlara ETH Gönder")
        print("2. TX Kas")
        print("3. Çıkış")

        choice = input("Bir seçim yapın (1-3): ")
        if choice == "1":
            if web3.is_connected():
                print("Cüzdanlara ETH gönderme işlemi başlatılıyor...")
                eth_amount = get_amount_from_user("Cüzdanlara göndereceğiniz ETH miktarını girin: ")
                send_eth_to_wallets(main_wallet, main_private_key, wallets, eth_amount)
            else:
                print("Blockchain'e bağlanılamadı.")
        elif choice == "2":
            if web3.is_connected():
                print("TX Kas işlemi başlatılıyor...")
                eth_amount = get_amount_from_user("TX kas işlemi için kullanılacak ETH miktarını girin: ")
                tx_loop(wallets, eth_amount)
            else:
                print("Blockchain'e bağlanılamadı.")
        elif choice == "3":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim, lütfen 1-3 arasında bir değer girin.")

if __name__ == "__main__":
    main_menu()
