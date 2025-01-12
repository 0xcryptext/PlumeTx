from web3 import Web3
import time
import random

# Blockchain node URL'si (Sepolia Testnet Infura örneği)
RPC_URL = "https://sepolia.drpc.org"

# Bağlantıyı oluştur
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Contract adresi ve ABI
CONTRACT_ADDRESS = "0x3E2e3F4F24eDdD9d6968B7b88F1Bf408FC9fEFd6"
CONTRACT_ABI = [
    {
        "inputs": [],
        "name": "depositEth",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    }
]
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

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

def tx_loop(wallets, eth_amount):
    """TX Kas işlemi için döngü."""
    print("TX işlemi başlatılıyor...")
    # İlk wallet'ı kullanıyoruz
    main_wallet, main_private_key = wallets[0]

    # Deposit işlemi yapmak için kontrata ETH gönderiyoruz
    for wallet_address, _ in wallets:
        try:
            # Transaction oluştur
            transaction = contract.functions.depositEth().build_transaction({
                'from': main_wallet,
                'value': eth_amount,  # Gönderilecek ETH
                'gas': 200000,        # Gas limiti (ayarlanabilir)
                'gasPrice': web3.to_wei(10, 'gwei'),  # Gas fiyatı
                'nonce': web3.eth.get_transaction_count(main_wallet),  # Nonce değeri
                'chainId': 11155111  # Sepolia Testnet için EIP-155 Chain ID
            })

            # İşlemi imzala
            signed_txn = web3.eth.account.sign_transaction(transaction, private_key=main_private_key)

            # İşlemi gönder
            tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
            print(f"Transaction gönderildi. Hash: {web3.to_hex(tx_hash)}")

            # İşlemi doğrula
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Transaction onaylandı. Hash: {web3.to_hex(tx_hash)}")
        except Exception as e:
            print(f"Contract'a ETH gönderirken hata oluştu: {e}")
        
        # Her işlemden sonra 5 ile 12 saniye arasında rastgele bekle
        wait_time = random.uniform(5, 12)
        print(f"Bir sonraki gönderim için {wait_time:.2f} saniye bekleniyor...\n")
        time.sleep(wait_time)  # Rastgele bekleme süresi

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
            print("Cüzdanlara ETH gönderme işlemi henüz yapılandırılmadı.")
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
