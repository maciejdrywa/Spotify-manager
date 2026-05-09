from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon, QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify downloader")
        self.setWindowIcon(QIcon("assets/app_icon.png"))
        self.setFixedSize(1150, 700)

        # Create menu bar
        menu = self.menuBar()
        # File menu
        file_menu = menu.addMenu("File")
        setting_action = QAction("Settings", self)
        open_downloads_action = QAction("Open downloads folder", self)
        exit_action = QAction("Exit", self)

        file_menu.addAction(setting_action)
        file_menu.addAction(open_downloads_action)
        file_menu.addAction(exit_action)
        
        # Account menu
        account_menu = menu.addMenu("&Account")
        login_action = QAction("Login with Spotify", self)
        logout_action = QAction("Logout", self)
        profile_action = QAction("Profile", self)
        refresh_action = QAction("Refresh session", self)

        account_menu.addAction(login_action)
        account_menu.addAction(logout_action)
        account_menu.addAction(profile_action)
        account_menu.addAction(refresh_action)

        # Spotify menu
        spotify_menu = menu.addMenu("Spotify")
        playlists_action = QAction("My playlists", self)
        liked_action = QAction("Liked Songs", self)
        search_playlist_url_action = QAction("Search playlist by URL", self)
        load_playlists_action = QAction("Load playlist", self)

        spotify_menu.addAction(playlists_action)
        spotify_menu.addAction(liked_action)
        spotify_menu.addAction(search_playlist_url_action)
        spotify_menu.addAction(load_playlists_action)

        # Download menu
        download_menu = menu.addMenu("Download")
        download_selceted_action = QAction("Download selected", self)
        download_playlist_action = QAction("Download playlist", self)
        stop_download_action = QAction("Stop download", self)

        download_menu.addAction(download_selceted_action)
        download_menu.addAction(download_playlist_action)
        download_menu.addAction(stop_download_action)

        # Help menu
        help_menu = menu.addMenu("Help")
        about_action = QAction("About", self)
        github_action = QAction("GitHub / Documentation", self)

        help_menu.addAction(about_action)
        help_menu.addAction(github_action)



        
        

