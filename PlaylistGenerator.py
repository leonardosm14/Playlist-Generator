#Projeto Playlist Generator - Trabalho Final
#Criado por Leonardo de Sousa Marques
#Disciplina: Programação Orientada a Objetos I

#Bibliotecas: tkinter (interface gráfica), spotipy (verificação e validação do Spotify), random e webbrowser (Web)
import tkinter as tk
from tkinter import *
from tkinter import font
import spotipy
from spotipy import *
import webbrowser
import random

#Classe do Aplicativo/Programa:
class Aplicativo:

    #Configurações de tela e variáveis self. do programa:
    def __init__(self, root):
        self.window = root
        self.window.title('Playlist Generator')
        self.window.geometry("400x550")
        self.window.resizable(False, False)
        self.artists = None
        self.num_songs = None
        self.playlist_name = None
        self.validate_token = None
        self.playlist_url = None
        self.initial_frame()

     #Página Inicial
    def initial_frame(self):
        #Configurações de Background
        self.background = tk.PhotoImage(file="images/bg1.png")
        self.background_label = tk.Label(self.window, image=self.background)
        self.background_label.place(relwidth=1, relheight=1)
        self.initial_frame = tk.Frame(self.window)

        #Tipografia
        self.Poppins = font.Font(family="Poppins", size=12)

        #Botão de "Continue"
        continue_button = Button(text="Continue", font=self.Poppins, bg="#1ED760", fg="white", command=self.second_frame)
        continue_button.place(relx=0.60, rely=0.90, anchor="se")

    #Segunda Página
    def second_frame(self):
        #Lógica para fechar a primeira página e abrir a segunda
        self.initial_frame.pack_forget()
        self.page2_frame = Frame(self.window, bg="#222222", width=400, height=550)
        self.page2_frame.pack_propagate(False)
        self.Poppins = font.Font(family="Poppins", size=12)

        #Título
        title_label = Label(self.page2_frame, text="CREATE YOUR \n PLAYLIST", font=("Poppins", 25, "bold"), bg="#222222", fg="#1ED760")
        title_label.pack(pady=50)

        #Configuração dos Campos de Entrada de Dados
        entry_frame = Frame(self.page2_frame, bg="#222222")
        entry_frame.pack()

        #Campo - Artists
        self.artists_label = Label(entry_frame, text="Artists/Bands (max. 50):", font=self.Poppins, bg="#222222", fg="white")
        self.artists_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.artists_entry = Entry(entry_frame, font=self.Poppins, bg="#4E4E4E")
        self.artists_entry.grid(row=2, column=0, padx=5, pady=12, sticky="ew")

        #Campo - Num of Songs
        self.num_songs_label = Label(entry_frame, text="Number of Songs (max. 100):", font=self.Poppins, bg="#222222", fg="white")
        self.num_songs_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.num_songs_entry = Entry(entry_frame, font=self.Poppins, bg="#4E4E4E")
        self.num_songs_entry.grid(row=4, column=0, padx=5, pady=12, sticky="ew")

        #Campo - Playlist Name
        self.playlist_name_label = Label(entry_frame, text="Playlist Name:", font=self.Poppins, bg="#222222", fg="white")
        self.playlist_name_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.playlist_name_entry = Entry(entry_frame, font=self.Poppins, bg="#4E4E4E", width=30)
        self.playlist_name_entry.grid(row=6, column=0, padx=5, pady=12, sticky="ew")

        #Botão "Generate" que ativa a função de geração de playlist
        generate_button = Button(self.page2_frame, text="Generate", font=self.Poppins, bg="#1ED760", fg="white", command=self.generate_playlist)
        generate_button.pack(pady=40)

        self.page2_frame.pack()

    #Geração da Playlist
    def generate_playlist(self):
        #Lógica para conseguir o Token de Acesso do Spotify

        #Caso altere o projeto, é necessário preencher seus próprios dados de client_id, secret e uri:
        #Estes dados podem ser criados no site Spotify Developer
        client_id = 'SEU-CLIENT-ID'
        client_secret = 'SEU-CLIENT-SECRET'
        redirect_uri = 'SEU-LOCAL-HOST'

        credentials = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri)

        #Sistema de autenticação para permissão do programa
        sp = spotipy.Spotify(auth_manager=credentials)

        #Coleta dos dados preenchidos nas caixas da página 2
        artists = self.artists_entry.get().split(',')
        num_songs = int(self.num_songs_entry.get())
        playlist_name = self.playlist_name_entry.get()

        songs_per_artist = num_songs // len(artists)

        #Cálculo do resto da divisão para caso a quantidade de artistas não seja divisível pelo num de músicas
        remainder = num_songs % len(artists)

        #Restrições da quantidade e artistas e número de músicas (é possível alterar):
        if len(artists) <= 50 and num_songs <= 100:

            #Criação da Playlist
            #OBS: É necessário preencher com seu próprio usuário do Spotify.
            playlist = sp.user_playlist_create(user='SEU-USUÁRIO-SPOTIFY', name=playlist_name)

            #Lógica de busca pelos artistas no Spotify (seleciona o primeiro compatível com o nome digitado)
            for artist_name in artists:
                results = sp.search(q=artist_name, limit=1, type='artist')
                artist_uri = results['artists']['items'][0]['uri']

                #Vetor com todas as músicas do artista
                all_tracks = []

                #Todos os albums do artista:
                albums = sp.artist_albums(artist_uri, album_type='album')

                #Adiciona-se cada faixa de cada album na lista all_trakcs:
                for album in albums['items']:
                    album_tracks = sp.album_tracks(album['id'])
                    all_tracks.extend(track['uri'] for track in album_tracks['items'])

                #Embaralhamento para que a ordem seja aleatória
                random.shuffle(all_tracks)

                #Caso o resto seja diferente de 0, serão adicionadas mais músicas aos primeiros artistas
                additional = 0
                if remainder > 0:
                    additional = 1
                    remainder -= 1

                if additional > 0:
                    sp.playlist_add_items(playlist['id'], all_tracks[:songs_per_artist + additional])
                else:
                    sp.playlist_add_items(playlist['id'], all_tracks[:songs_per_artist])

            #Link da Playlist:
            self.playlist_url = f"https://open.spotify.com/playlist/{playlist['id']}"
            print("Open the Playlist:", self.playlist_url)

        #Caso as restrições não sejam atendidas:
        else:
            if len(artists) > 50:
                print("Adicione uma quantidade de artistas menor ou igual que 50.")
            if num_songs > 100:
                print("Adicione uma quantidade de artistas menor ou igual que 100.")

        #Depois de gerada, abre-se a terceira página
        self.third_frame()

    #Terceira Página
    def third_frame(self):
        # Lógica para fechar a segunda página e abrir a terceira
        self.page2_frame.pack_forget()
        self.page3_frame = Frame(self.window, bg="#222222", width=400, height=550)
        self.page3_frame.pack_propagate(False)
        self.page3_frame.pack(fill="both")
        self.Poppins = font.Font(family="Poppins", size=12)

        #Título
        title = Label(self.page3_frame, text="PLAYLIST \n GENERATED!", font=("Poppins", 25, "bold"),bg="#222222", fg="#1ED760")
        title.pack(pady=50)

        #Botão para abrir a playlist (Ativa a def open_playlist)
        open_button = Button(self.page3_frame, text="Open the Playlist", font=self.Poppins, bg="#1ED760", fg="white",
                             command=self.open_playlist)
        open_button.pack(pady=80)

        #Mensagem de créditos
        message_label = Label(self.page3_frame,
                              text="© Programa criado por \n Leonardo de Sousa Marques para a \n Disciplina INE5401, com auxílio de \n Spotify Developer",
                              font=("Poppins", 12), bg="#222222", fg="white")
        message_label.pack(pady=40)

        self.page3_frame.pack()

    #Função para abrir a playlist no navegador padrão:
    def open_playlist(self):
        webbrowser.open(self.playlist_url)

#Roda o aplicativo com interface gráfica - Tkinter
if __name__ == "__main__":
    window = tk.Tk()
    app = Aplicativo(window)
    window.mainloop()
