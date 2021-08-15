def start(initialize=1):

    import threading, subprocess
    from . import favorites, foundry, furaffinity, twitter

    # process = subprocess.Popen([
    #     r'Webscraping\PixivUtil\PixivUtil2.exe',
    #     '-s', '6', 'y', '-x'
    #     #         start end  stop
    #     ])
    
    threads = [
        # threading.Thread(target=process.wait),
        threading.Thread(target=twitter.start, args=(initialize,)),
        threading.Thread(target=foundry.start, args=(initialize,)),
        threading.Thread(target=furaffinity.start, args=(initialize,)),
        ]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    favorites.start(initialize)