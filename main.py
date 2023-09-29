import os
import zipfile
import shutil
import tkinter as tk
from tkinter import messagebox, ttk
import requests
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# URLs dos temas e plugins padrão
DEFAULT_THEME = "astra"
SITE_PLUGINS = {
    "Elementor": "https://downloads.wordpress.org/plugin/elementor.latest-stable.zip",
    "Elementor Header Footer": "https://downloads.wordpress.org/plugin/header-footer-elementor.latest-stable.zip",
    "Admin Menu Editor": "https://downloads.wordpress.org/plugin/admin-menu-editor.latest-stable.zip",
    "Contact Form 7": "https://downloads.wordpress.org/plugin/contact-form-7.latest-stable.zip",
    "Hide Admin Notice": "https://downloads.wordpress.org/plugin/hide-admin-notices.latest-stable.zip",
    "Hide My WP Ghost": "https://downloads.wordpress.org/plugin/hide-my-wp.latest-stable.zip",
    "My WP Translate": "https://downloads.wordpress.org/plugin/my-wp-translate.latest-stable.zip",
    "QuadMenu": "https://downloads.wordpress.org/plugin/quadmenu.latest-stable.zip",
    "QuadMenu Astra": "https://downloads.wordpress.org/plugin/quadmenu-astra.latest-stable.zip",
    "WP Fastest Cache": "https://downloads.wordpress.org/plugin/wp-fastest-cache.latest-stable.zip",
    "SEO By Yoast": "https://downloads.wordpress.org/plugin/wordpress-seo.latest-stable.zip",
}

ECOMMERCE_PLUGINS = {
    "Elementor": "https://downloads.wordpress.org/plugin/elementor.latest-stable.zip",
    "Elementor Header Footer": "https://downloads.wordpress.org/plugin/header-footer-elementor.latest-stable.zip",
    "Admin Menu Editor": "https://downloads.wordpress.org/plugin/admin-menu-editor.latest-stable.zip",
    "Contact Form 7": "https://downloads.wordpress.org/plugin/contact-form-7.latest-stable.zip",
    "Hide Admin Notice": "https://downloads.wordpress.org/plugin/hide-admin-notices.latest-stable.zip",
    "Hide My WP Ghost": "https://downloads.wordpress.org/plugin/hide-my-wp.latest-stable.zip",
    "My WP Translate": "https://downloads.wordpress.org/plugin/my-wp-translate.latest-stable.zip",
    "QuadMenu": "https://downloads.wordpress.org/plugin/quadmenu.latest-stable.zip",
    "QuadMenu Astra": "https://downloads.wordpress.org/plugin/quadmenu-astra.latest-stable.zip",
    "WP Fastest Cache": "https://downloads.wordpress.org/plugin/wp-fastest-cache.latest-stable.zip",
    "SEO By Yoast": "https://downloads.wordpress.org/plugin/wordpress-seo.latest-stable.zip",
    # PLGUNS ECOMMERCE
    "Woocommerce": "https://downloads.wordpress.org/plugin/woocommerce.latest-stable.zip",
}

themes = {
    #"Astra": "https://downloads.wordpress.org/theme/astra.latest-stable.zip",
    "Astra Child": "http://localhost/startwp/astra-child.zip",
}

def create_database_with_selenium(db_name, db_user, db_password, db_user_value, db_password_value):
    # Configurar as opções do Chrome para o modo headless
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Ativa o modo headless
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://localhost/phpmyadmin")  # Abra o phpMyAdmin
    time.sleep(5)

    # Preencha as informações de login do phpMyAdmin usando XPath
    username_field = driver.find_element(By.XPATH, "//*[@id='input_username']")
    username_field.send_keys(db_user_value)

    password_field = driver.find_element(By.XPATH, "//*[@id='input_password']")
    password_field.send_keys(db_password_value)
    password_field.send_keys(Keys.ENTER)

    time.sleep(3)

    # Crie um novo banco de dados
    driver.get("http://localhost/phpmyadmin/index.php?route=/server/databases")
    time.sleep(2)
    new_db_name_field = driver.find_element(By.XPATH, "//*[@id='text_create_db']")
    time.sleep(2)
    new_db_name_field.send_keys(db_name)
    time.sleep(1)
    collation_select = driver.find_element(By.XPATH, "//*[@id='text_create_db']")
    time.sleep(1)
    collation_select.send_keys(Keys.ENTER)
    time.sleep(1)
    driver.quit()


def login_to_wordpress_with_selenium(site_url, project_name, wordpress_language, wordpress_username, wordpress_email, wordpress_password):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Ativa o modo headless
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(site_url)

    time.sleep(4)
    select_element = driver.find_element(By.XPATH, "//*[@id='language']")
    select_element.send_keys(wordpress_language)
    select_element.send_keys(Keys.RETURN)

    time.sleep(3)
    sitename_field = driver.find_element(By.XPATH, "//*[@id='weblog_title']")
    sitename_field.send_keys(project_name)

    time.sleep(1)
    username_field = driver.find_element(By.XPATH, "//*[@id='user_login']")
    username_field.send_keys(wordpress_username)

    time.sleep(1)
    password_field = driver.find_element(By.XPATH, "//*[@id='pass1']")
    password_field.send_keys(Keys.CONTROL + 'a')
    password_field.send_keys(Keys.DELETE)
    password_field.send_keys(wordpress_password)

    time.sleep(1)
    username_field = driver.find_element(By.XPATH, "//*[@id='admin_email']")
    username_field.send_keys(wordpress_email)
    password_field.send_keys(Keys.RETURN)

    driver.quit()
def download_wordpress():
    wordpress_url = "https://wordpress.org/latest.zip"
    response = requests.get(wordpress_url)
    with open("wordpress.zip", "wb") as file:
        file.write(response.content)

def extract_wordpress():
    with zipfile.ZipFile("wordpress.zip", "r") as zip_ref:
        zip_ref.extractall()
    os.remove("wordpress.zip")

def configure_wp_config(db_name, db_user, db_password, project_name):
    wp_config_path = os.path.join(".", "wp-config.php")

    if not os.path.exists(wp_config_path):
        # Se o arquivo wp-config.php não existir, crie-o
        with open(wp_config_path, "w") as file:
            file.write(f"<?php\n")
            file.write(f"define('DB_NAME', '{db_name}');\n")
            file.write(f"define('DB_USER', '{db_user}');\n")
            file.write(f"define('DB_PASSWORD', '{db_password}');\n")
            file.write(f"define('DB_HOST', 'localhost');\n")
            file.write(f"define('DB_CHARSET', 'utf8mb4');\n")
            file.write(f"define('DB_COLLATE', '');\n")
            file.write(f"$table_prefix = 'wp_';\n")
            file.write(f"define('WP_DEBUG', false);\n")
            file.write(f"if ( ! defined('ABSPATH') )\n")
            file.write(f"  define('ABSPATH', __DIR__ . '/');\n")
            file.write(f"require_once ABSPATH . 'wp-settings.php';\n")
            file.write(f"define('WP_HOME', 'http://localhost/{project_name}');\n")
            file.write(f"define('WP_SITEURL', 'http://localhost/{project_name}');\n")

    else:
        # Se o arquivo wp-config.php já existe, atualize-o com as informações do banco de dados
        with open(wp_config_path, "r") as file:
            wp_config = file.read()
        wp_config = wp_config.replace("database_name_here", db_name)
        wp_config = wp_config.replace("username_here", db_user)
        wp_config = wp_config.replace("password_here", db_password)
        wp_config = wp_config.replace("http://localhost", f"http://localhost/{project_name}")
        with open(wp_config_path, "w") as file:
            file.write(wp_config)

def remove_all_themes_and_plugins():
    themes_dir = os.path.join(".", "wp-content", "themes")
    plugins_dir = os.path.join(".", "wp-content", "plugins")
    shutil.rmtree(themes_dir, ignore_errors=True)
    shutil.rmtree(plugins_dir, ignore_errors=True)

def install_theme(theme_slug, theme_url):
    #os.system(f"wp theme install {theme_slug} --activate")
    pass

def download_theme(theme_slug, theme_url):
    response = requests.get(theme_url)
    with open(f"{theme_slug}.zip", "wb") as file:
        file.write(response.content)

def install_plugins(plugin_urls):
    for plugin_name, plugin_url in plugin_urls.items():
        download_plugin(plugin_name, plugin_url)
        unzip_plugin(plugin_name)

def download_plugin(plugin_name, plugin_url):
    response = requests.get(plugin_url)
    with open(f"{plugin_name}.zip", "wb") as file:
        file.write(response.content)

def unzip_plugin(plugin_name):
    with zipfile.ZipFile(f"{plugin_name}.zip", "r") as zip_ref:
        zip_ref.extractall(os.path.join(".", "wp-content", "plugins"))

def move_wordpress_files_one_level_up():
    wordpress_dir = os.path.join(".", "wordpress")
    for item in os.listdir(wordpress_dir):
        source = os.path.join(wordpress_dir, item)
        destination = os.path.join(".", item)
        shutil.move(source, destination)
    shutil.rmtree(wordpress_dir)

def install_themes_in_wp_content_themes(themes_to_install):
    themes_dir = os.path.join(".", "wp-content", "themes")
    os.makedirs(themes_dir, exist_ok=True)
    for theme_name, theme_url in themes_to_install.items():
        download_theme(theme_name, theme_url)
        unzip_theme(theme_name, themes_dir)

def unzip_theme(theme_name, themes_dir):
    theme_zip_file = f"{theme_name}.zip"
    with zipfile.ZipFile(theme_zip_file, "r") as zip_ref:
        zip_ref.extractall(os.path.join(themes_dir, theme_name))
    os.remove(theme_zip_file)

def create_database(db_name, db_user, db_password):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'localhost' IDENTIFIED BY '{db_password}'")
    cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost'")
    conn.close()

def create_wp_config_file(db_name, db_user, db_password, project_name):
    wp_config_path = os.path.join(".", "wp-config.php")
    if not os.path.exists(wp_config_path):
        with open(wp_config_path, "w") as file:
            file.write(f"<?php\n")
            file.write(f"define('DB_NAME', '{db_name}');\n")
            file.write(f"define('DB_USER', '{db_user}');\n")
            file.write(f"define('DB_PASSWORD', '{db_password}');\n")
            file.write(f"define('DB_HOST', 'localhost');\n")
            file.write(f"define('DB_CHARSET', 'utf8mb4');\n")
            file.write(f"define('DB_COLLATE', '');\n")
            file.write(f"$table_prefix = 'wp_';\n")
            file.write(f"define('WP_DEBUG', false);\n")
            file.write(f"if ( ! defined('ABSPATH') )\n")
            file.write(f"  define('ABSPATH', __DIR__ . '/');\n")
            file.write(f"require_once ABSPATH . 'wp-settings.php';\n")
            file.write(f"define('WP_HOME', 'http://localhost/{project_name}');\n")
            file.write(f"define('WP_SITEURL', 'http://localhost/{project_name}');\n")

def install_wordpress(project_name, db_name, db_user, db_password, language, theme_slug, theme_url, plugin_slugs):
    # Calculate the path one level above the current directory
    parent_directory = os.path.abspath(os.path.join(os.getcwd(), '..'))
    project_dir = os.path.join(parent_directory, project_name)

    os.makedirs(project_dir, exist_ok=True)
    os.chdir(project_dir)

    download_wordpress()
    extract_wordpress()

    move_wordpress_files_one_level_up()  # Move WordPress files one level up

    create_database(db_name, db_user, db_password)
    create_wp_config_file(db_name, db_user, db_password, project_name)
    remove_all_themes_and_plugins()

    install_themes_in_wp_content_themes(themes)  # Install themes in the wp-content/themes folder

    install_theme(theme_slug, theme_url)
    install_plugins(plugin_slugs)

def createwp():
    def start_installation():
        project_name = project_name_entry.get()
        db_name = db_name_entry.get()
        db_user = db_user_entry.get()
        db_password = db_password_entry.get()
        language = language_combobox.get()
        theme_slug = theme_combobox.get()
        plugin_option = plugin_option_combobox.get()
        plugins = SITE_PLUGINS if plugin_option == "site" else ECOMMERCE_PLUGINS

        if not db_exists_checkbox.get():
            create_database_with_selenium(db_name, db_user, db_password, db_user_entry.get(), db_password_entry.get())

        # Obtenha a URL correta do tema Astra do dicionário 'themes'
        theme_url = themes.get(theme_slug)

        install_wordpress(project_name, db_name, db_user, db_password, language, theme_slug, theme_url, plugins)

        # Obtém as credenciais inseridas pelo usuário
        wordpress_username = wordpress_username_entry.get()
        wordpress_password = wordpress_password_entry.get()
        wordpress_language = language_combobox.get()
        wordpress_email = wordpress_email_entry.get()

        # Faz login no WordPress com as credenciais fornecidas
        login_to_wordpress_with_selenium(f"http://localhost/{project_name}", project_name, wordpress_language, wordpress_username, wordpress_email, wordpress_password)

        messagebox.showinfo("Instalação Concluída", "O WordPress foi instalado com sucesso!")

        # Captura de tela com mensagem de sucesso
        root.update_idletasks()
        root.withdraw()  # Ocultar a janela principal temporariamente
        time.sleep(2)  # Esperar para garantir que a janela de mensagem seja exibida

    root = tk.Tk()
    root.title("Instalador WordPress")
    root.geometry("250x800")  # Aumentar o tamanho em 150%
    root.configure()  # Defina o fundo da janela como preto

    padding = 6

    project_name_label = tk.Label(root, text="Nome do Projeto:")
    project_name_label.pack(pady=padding)
    project_name_entry = tk.Entry(root)
    project_name_entry.pack(pady=padding)

    db_exists_checkbox = tk.BooleanVar()
    db_exists_checkbox.set(False)
    db_exists_checkbox_widget = tk.Checkbutton(root, text="Eu tenho um banco de dados", variable=db_exists_checkbox)
    db_exists_checkbox_widget.pack(pady=padding)

    db_name_label = tk.Label(root, text="Nome do Banco de Dados:")
    db_name_label.pack(pady=padding)
    db_name_entry = tk.Entry(root)
    db_name_entry.pack(pady=padding)

    db_user_label = tk.Label(root, text="Usuário do Banco de Dados:")
    db_user_label.pack(pady=padding)
    db_user_entry = tk.Entry(root)
    db_user_entry.insert(0, "root")  # Defina o nome do banco de dados como "root"
    db_user_entry.pack(pady=padding)

    db_password_label = tk.Label(root, text="Senha do Banco de Dados:")
    db_password_label.pack(pady=padding)
    db_password_entry = tk.Entry(root, show="*")
    db_password_entry.pack(pady=padding)

    wordpress_username_label = tk.Label(root, text="Nome de Usuário WordPress:")
    wordpress_username_label.pack(pady=padding)
    wordpress_username_entry = tk.Entry(root)
    wordpress_username_entry.pack(pady=padding)

    wordpress_password_label = tk.Label(root, text="Senha WordPress:")
    wordpress_password_label.pack(pady=padding)
    wordpress_password_entry = tk.Entry(root, show="*")
    wordpress_password_entry.pack(pady=padding)

    wordpress_email_label = tk.Label(root, text="Email admin WordPress:")
    wordpress_email_label.pack(pady=padding)
    wordpress_email_entry = tk.Entry(root)
    wordpress_email_entry.pack(pady=padding)

    language_label = tk.Label(root, text="Idioma:")
    language_label.pack(pady=padding)
    language_combobox = ttk.Combobox(root, values=["pt-br", "it-it", "en-us", "en-uk", "fr-fr", "es-es"])
    language_combobox.set("it-it")  # Defina o idioma padrão como "it-it"
    language_combobox.pack(pady=padding)

    theme_label = tk.Label(root, text="Escolha um Tema:")
    theme_label.pack(pady=padding)
    theme_combobox = ttk.Combobox(root, values=["Astra"])
    theme_combobox.set("Astra")
    theme_combobox.pack(pady=padding)

    plugin_option_label = tk.Label(root, text="Escolha a opção de Plugins:")
    plugin_option_label.pack(pady=padding)
    plugin_option_combobox = ttk.Combobox(root, values=["site", "e-commerce"])
    plugin_option_combobox.set("e-commerce")  # Defina o idioma padrão como "it-it"
    plugin_option_combobox.pack(pady=padding)

    install_button = tk.Button(root, text="Iniciar Instalação", command=start_installation)
    install_button.pack(pady=padding)
    root.mainloop()

createwp()
