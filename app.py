import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Configurações do Chrome
options = Options()
options.headless = True  # Execute sem interface gráfica, se desejar

# Caminho para o chromedriver
driver_path = r"C:\Users\geova\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # Atualize se necessário
service = Service(driver_path)

# Inicializa o navegador com o serviço Chrome
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://steamdb.info/sales/")

# Aguarde até a tabela estar visível
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "table-sales"))
)

# Aguarde um pouco mais para garantir que a página está totalmente carregada
time.sleep(5)

# Obtenha o conteúdo HTML da página
soup = BeautifulSoup(driver.page_source, "html.parser")

# Feche o navegador
driver.quit()

# Encontre a tabela de vendas
sales_table = soup.find("table", {"class": "table-sales"})

# Lista para armazenar os dados extraídos
table_data = []

# Verifique se a tabela foi encontrada
if sales_table:
    # Extraia todas as linhas da tabela, ignorando o cabeçalho
    rows = sales_table.find_all("tr")[1:]  # Pula o cabeçalho
    for row in rows:
        # Cada linha contém várias células
        cells = row.find_all("td")
        if len(cells) >= 5:  # Verifique se a linha contém células suficientes
            game_name = cells[0].text.strip()  # Nome do jogo
            price = cells[1].text.strip()  # Preço original
            discount_price = cells[2].text.strip()  # Preço com desconto
            discount_percentage = cells[3].text.strip()  # Percentual de desconto
            remaining_time = cells[4].text.strip()  # Tempo restante

            # Adiciona os dados da linha à lista
            table_data.append([game_name, price, discount_price, discount_percentage, remaining_time])
else:
    print("Tabela de vendas não encontrada.")

# Salva os dados em um arquivo CSV
csv_filename = "steam_sales.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Escreve o cabeçalho do CSV
    writer.writerow(["Nome do Jogo", "Preço", "Preço com Desconto", "Desconto", "Tempo Restante"])
    # Escreve os dados extraídos
    writer.writerows(table_data)

print(f"Dados salvos em {csv_filename}")
