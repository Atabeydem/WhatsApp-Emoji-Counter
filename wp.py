from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# ChromeDriver başlatma ayarları
options = Options()
options.add_argument("--headless")  # Tarayıcıyı başlıksız çalıştırır
options.add_argument("--disable-gpu")  # GPU hızlandırmasını devre dışı bırak
options.add_argument("--window-size=1920,1080")  # Tarayıcı penceresini standart boyutta aç
options.add_argument("--no-sandbox")  # Kök izinlerine sahip olmayan ortamlarda kullanılmak üzere
options.add_argument("--disable-dev-shm-usage")  # /dev/shm kullanmadan geçici bellek oluşturma

# WebDriver'ı başlat
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# WhatsApp Web'e bağlan
driver.get('https://web.whatsapp.com')

# Kullanıcının QR kodu tarayıp oturum açmasını bekle
print("Lütfen QR kodu tarayarak oturum açın.")
time.sleep(30)  # Oturum açma süresi için bekleyin (bu süreyi ihtiyaca göre arttırabilirsiniz)

try:
    # Sohbetin yüklendiğini doğrulama
    chat_name = 'Hopdeneme123'  # Grubunuzun adı
    chat = WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.XPATH, f'//span[@title="{chat_name}"]')))
    chat.click()
except Exception as e:
    print(f"Error locating chat: {e}")
    driver.quit()
    exit()

time.sleep(5)  # Sohbetin yüklenmesi için bekleyin

# Duyuru mesajlarını ve emoji reaksiyonlarını çekin
messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
data = []

for message in messages:
    try:
        msg_text = message.find_element(By.XPATH, './/span[contains(@class, "selectable-text")]').text
        reactions = message.find_elements(By.XPATH, './/span[contains(@class, "reaction-emoji")]')
        for reaction in reactions:
            emoji = reaction.find_element(By.XPATH, './/span[@data-plain-text]').get_attribute('data-plain-text')
            count = reaction.find_element(By.XPATH, './/span[contains(@class, "reaction-count")]').text
            data.append([msg_text, emoji, count])
    except Exception as e:
        print(f"Error processing message: {e}")

# WebDriver'ı kapat
driver.quit()

# Verileri pandas DataFrame'e çevirin
df = pd.DataFrame(data, columns=['Mesaj', 'Emoji', 'Kullanıcı Sayısı'])

# Verileri Excel dosyasına yazın
output_file = 'whatsapp_emoji_reactions.xlsx'
df.to_excel(output_file, index=False)

print(f"Veriler '{output_file}' dosyasına kaydedildi.")
