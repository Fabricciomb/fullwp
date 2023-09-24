import os
import requests
from zipfile import ZipFile
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedTk
from PIL import Image, ImageTk  # Importe as bibliotecas do Pillow

# Função para baixar o WordPress
def install_wordpress(project_folder):
    wordpress_url = "https://wordpress.org/latest.zip"

    try:
        response = requests.get(wordpress_url)
        response.raise_for_status()

        with open("wordpress.zip", "wb") as f:
            f.write(response.content)

        with ZipFile("wordpress.zip", "r") as zip_ref:
            zip_ref.extractall()

        os.remove("wordpress.zip")

        print("WordPress baixado e descompactado com sucesso!")

        # Remover todos os temas e plugins existentes
        remove_all_themes_and_plugins(project_folder)

        # Renomear a pasta "wordpress" para o nome do projeto
        os.rename("wordpress", project_folder)

        print(f"Pasta renomeada para '{project_folder}'")
    except Exception as e:
        print(f"Falha ao baixar e configurar o WordPress: {e}")

# Função para remover todos os temas e plugins existentes
def remove_all_themes_and_plugins(project_folder):
    theme_path = os.path.join(project_folder, "wp-content", "themes")
    plugin_path = os.path.join(project_folder, "wp-content", "plugins")

    # Remover todos os temas existentes
    if os.path.exists(theme_path):
        for theme in os.listdir(theme_path):
            theme_folder = os.path.join(theme_path, theme)
            if os.path.isdir(theme_folder):
                shutil.rmtree(theme_folder)
                print(f"Removido tema: {theme}")

    # Remover todos os plugins existentes
    if os.path.exists(plugin_path):
        for plugin in os.listdir(plugin_path):
            plugin_folder = os.path.join(plugin_path, plugin)
            if os.path.isdir(plugin_folder):
                shutil.rmtree(plugin_folder)
                print(f"Removido plugin: {plugin}")

# Função para baixar e instalar temas
def download_and_install_themes(theme_urls, project_folder):
    for theme_name, theme_url in theme_urls.items():
        try:
            response = requests.get(theme_url)
            response.raise_for_status()

            theme_folder_path = os.path.join(project_folder, "wp-content", "themes", theme_name)
            os.makedirs(theme_folder_path, exist_ok=True)

            temp_zip_path = os.path.join(os.getcwd(), f"{theme_name}.zip")

            with open(temp_zip_path, "wb") as f:
                f.write(response.content)

            with ZipFile(temp_zip_path, "r") as zip_ref:
                zip_ref.extractall(theme_folder_path)

            os.remove(temp_zip_path)
            print(f"Tema '{theme_name}' baixado e instalado com sucesso.")
        except Exception as e:
            print(f"Falha ao baixar e instalar o tema '{theme_name}': {e}")

# Função para baixar e instalar plugins
def download_and_install_plugins(plugin_urls, project_folder):
    try:
        plugin_folder = os.path.join(project_folder, "wp-content", "plugins")
        os.makedirs(plugin_folder, exist_ok=True)

        for plugin_name, plugin_url in plugin_urls.items():
            try:
                response = requests.get(plugin_url)
                response.raise_for_status()

                temp_zip_path = os.path.join(os.getcwd(), f"{plugin_name}.zip")

                with open(temp_zip_path, "wb") as f:
                    f.write(response.content)

                with ZipFile(temp_zip_path, "r") as zip_ref:
                    zip_ref.extractall(plugin_folder)

                os.remove(temp_zip_path)
                print(f"Plugin '{plugin_name}' baixado e instalado com sucesso.")
            except Exception as e:
                print(f"Falha ao baixar e instalar o plugin '{plugin_name}': {e}")
    except Exception as e:
        print(f"Falha ao criar a pasta 'wp-content/plugins': {e}")

# Função principal
def main():
    def start_installation():
        project_folder = project_folder_entry.get()
        plugin_option = plugin_option_combobox.get()

        if project_folder and plugin_option:
            install_wordpress(project_folder)
            remove_all_themes_and_plugins(project_folder)
            download_and_install_themes(themes, project_folder)

            if plugin_option == "site":
                download_and_install_plugins(site_plugins, project_folder)
            elif plugin_option == "ecommerce":
                download_and_install_plugins(ecommerce_plugins, project_folder)
            else:
                print("Opção de plugins inválida. Escolha 'site' ou 'ecommerce'.")

        # Fechar a janela após a execução
        root.destroy()

    root = ThemedTk(theme="equilux")
    root.title("Core WordPress")

    # Defina o fundo da janela para preto (#000)
    root.configure(background="#000")

    main_frame = ttk.Frame(root)
    main_frame.grid(column=0, row=0, padx=0, pady=0)

    # Carregue a imagem
    logo_image = Image.open("logo.png")
    logo_photo = ImageTk.PhotoImage(logo_image)

    project_folder_logo = ttk.Label(main_frame, image=logo_photo)
    project_folder_logo.image = logo_photo  # Evitar que a imagem seja coletada pelo garbage collector
    project_folder_logo.grid(column=0, row=0, pady=10, padx=20, sticky=tk.W)

    project_folder_label = ttk.Label(main_frame, text="Nome do site:", font=("Arial", 16))
    project_folder_label.grid(column=0, row=1, pady=10, padx=20, sticky=tk.W)

    project_folder_entry = ttk.Entry(main_frame, font=("Arial", 16))
    project_folder_entry.grid(column=0, row=2, pady=10, padx=20, sticky=(tk.W, tk.E))


    plugin_option_label = ttk.Label(main_frame, text="Tipo do site:", font=("Arial", 16))
    plugin_option_label.grid(column=0, row=3, pady=10, padx=20, sticky=tk.W)

    plugin_option_combobox = ttk.Combobox(main_frame, values=["site", "ecommerce"], font=("Arial", 16), state="readonly")
    plugin_option_combobox.grid(column=0, row=4, pady=10, padx=20, sticky=(tk.W, tk.E))

    start_button = ttk.Button(main_frame, text="Iniciar Instalação", command=start_installation)
    start_button.grid(column=0, row=5, pady=20, padx=20, sticky=(tk.W, tk.E))

    root.mainloop()

if __name__ == "__main__":
    # Lista de temas e plugins para instalar
    themes = {
        #"Astra": "https://downloads.wordpress.org/theme/astra.latest-stable.zip",
        "Astra Child": "http://localhost/astra-child.zip",
    }

    site_plugins = {
        "Elementor": "https://downloads.wordpress.org/plugin/elementor.latest-stable.zip",
        "Admin Menu Editor": "https://downloads.wordpress.org/plugin/admin-menu-editor.latest-stable.zip",
        "Contact Form 7": "https://downloads.wordpress.org/plugin/contact-form-7.latest-stable.zip",
        "Hide Admin Notice": "https://downloads.wordpress.org/plugin/hide-admin-notices.latest-stable.zip",
        "Hide My WP Ghost": "https://downloads.wordpress.org/plugin/hide-my-wp.latest-stable.zip",
        "My WP Translate": "https://downloads.wordpress.org/plugin/my-wp-translate.latest-stable.zip",
        "QuadMenu": "https://downloads.wordpress.org/plugin/quadmenu.latest-stable.zip",
        "Astra": "https://downloads.wordpress.org/plugin/quadmenu-astra.latest-stable.zip",
        "WP Fastest Cache": "https://downloads.wordpress.org/plugin/wp-fastest-cache.latest-stable.zip",
        "SEO By Yoast": "https://downloads.wordpress.org/plugin/wordpress-seo.latest-stable.zip",
    }

    ecommerce_plugins = {
        "Elementor": "https://downloads.wordpress.org/plugin/elementor.latest-stable.zip",
        "Admin Menu Editor": "https://downloads.wordpress.org/plugin/admin-menu-editor.latest-stable.zip",
        "Contact Form 7": "https://downloads.wordpress.org/plugin/contact-form-7.latest-stable.zip",
        "Hide Admin Notice": "https://downloads.wordpress.org/plugin/hide-admin-notices.latest-stable.zip",
        "Hide My WP Ghost": "https://downloads.wordpress.org/plugin/hide-my-wp.latest-stable.zip",
        "My WP Translate": "https://downloads.wordpress.org/plugin/my-wp-translate.latest-stable.zip",
        "QuadMenu": "https://downloads.wordpress.org/plugin/quadmenu.latest-stable.zip",
        "Astra": "https://downloads.wordpress.org/plugin/quadmenu-astra.latest-stable.zip",
        "WP Fastest Cache": "https://downloads.wordpress.org/plugin/wp-fastest-cache.latest-stable.zip",
        "SEO By Yoast": "https://downloads.wordpress.org/plugin/wordpress-seo.latest-stable.zip",
        "Woocommerce": "https://downloads.wordpress.org/plugin/woocommerce.latest-stable.zip",
    }

    main()