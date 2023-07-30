class Download:
    url:str
    filename:str
    _opened = False

    def __init__(self, url, filename):
        self.url = url
        self.filename = filename

    def start_download(self) -> bytes:
        
        """Start the download process"""
        
        return download_file(self.url)
        

    def save_file(self, content:bytes):
        
        """Save the download content to the specified filename"""
        
        if content == -1:
            return

        with open(self.filename, 'wb') as file:
            file.write(content)
            self._opened = True

    def download_complete(self):

        """Signals that the download is complete"""

        if self._opened:
            return "file loaded"
        else:
            return "The file did not load or there are problems with it"


class ThreadingDownloader(Download):
    def __init__(self, url, filename):
        super().__init__(url, filename)

    def start_download(self):
        import threading

        thread = threading.Thread(target=self._download)
        thread.start()
        thread.join()

    def _download(self):
        content = download_file(self.url)
        self.save_file(content)


class MultiprocessingDownloader(Download):
    def __init__(self, url, filename):
        super().__init__(url, filename)

    def start_download(self):
        import multiprocessing

        thread = multiprocessing.Process(target=self._download)
        thread.start()
        thread.join()

    def _download(self):
        content = download_file(self.url)
        self.save_file(content)

class DownloadManager():
    _max_threads:int
    _max_processes:int
    _download:list
    
    def __init__(self, max_threads, max_processes):
        print('init')
        self._max_threads = max_threads
        self._max_processes = max_processes
        self._download = []

    def download(self, url:str, filename:str):
        
        """starts a new download for the given URL and saves it with the specified filename"""
        print(self.__dict__)

        if len(self._download) < self._max_threads:
            thread = ThreadingDownloader(url, filename)
            thread.start_download()
        else:
            thread = MultiprocessingDownloader(url, filename)
            thread.start_download()


#Helper Functions

def download_file(url:str) -> bytes:
     
    """Download the content for the given URL and returns it as bytes"""
    
    import requests

    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"File '{url}' downloaded and saved successfully.")
            return response.content
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
            return -1
    except Exception as e:
        with open('error_log.txt', 'a') as error_file:
            error_file.write(f"An error occurred while downloading '{url}':\n")
        print(f"An error occurred while downloading '{url}'. Details logged in 'error_log.txt'.")
        return -1


if __name__ == "__main__":
    d = DownloadManager(5, 5)
    d.download('https://in.all.biz/img/in/service_catalog/1774.jpeg', 'image.jpeg')
    d.download('https://thumbs.dreamstime.com/b/bi%C3%B3logo-molecular-joven-27183453.jpg', 'image.jpg')
    d.download('https://ideas.tribalyte.com/wp-content/uploads/2015/08/Biotechnology.jpg', 'image1.jpg')
    


