import argparse, json
from . import CONNECT, INSERT, SELECT, DELETE, WEBDRIVER
from .utils import bs4, requests, re, IncrementalBar, USER, ARTIST, save_image, get_hash, get_name, get_tags, generate_tags

SITE = 'nhentai'

def get_artist(text):

    targets = re.findall(r'[^[]*\[([^]]*)\]', text)
    targets = sum([i.split() for i in targets], [])
    targets = [i for i in targets if i not in ['decensored', 'digital']]
    targets = '_'.join([i.replace(',', '') for i in targets])

    return targets.replace('_)', ')')

def initialize(page='/favorites/?page=1', query=0):
    
    def next_page(pages):

        try: return pages.find(class_='next').get('href')
        except AttributeError: return False

    if not query:
        query = set(MYSQL.execute(SELECT[0], (SITE,), fetch=1))
        
    DRIVER.get(f'https://{SITE}.net{page}')
    html = bs4.BeautifulSoup(DRIVER.page_source(), 'lxml')
    hrefs = [
        (href, SITE) for target in 
        html.findAll('a', class_='cover', href=True)
        if (href:=target.get('href'),) not in query
        ]
        
    next = next_page(html.find(class_='pagination'))
    if hrefs and next: return hrefs + initialize(next, query)
    else: return hrefs
    
def page_handler(hrefs):

    if not hrefs: return
    comic_records = json.load(open(r'Webscraping\comic_data.json'))
    progress = IncrementalBar(SITE, max=MYSQL.rowcount)

    for href, in hrefs:
        
        progress.next()
        page_source = requests.get(f'https://{SITE}.net{href}')
        html = bs4.BeautifulSoup(page_source.content, 'lxml')
        
        cover = None
        target = html.findAll(href=re.compile('/artist/.+'))
        if target is None: target = html.findAll(href=re.compile('/group/.+'))
        artists = [
            artist.get('href').split('/')[-2].replace('-', '_')
            for artist in target
            ]
        artists = [
            ARTIST.get(artist, [artist])[0] for artist in artists
            ]

        for image in html.findAll('a', class_='gallerythumb'):
            
            try:
                page_source = requests.get(f'https://{SITE}.net{image.get("href")}')
                image = bs4.BeautifulSoup(page_source.content, 'lxml')
                src = image.find(src=re.compile('.+galleries.+')).get('src')
                name = get_name(src)

                if cover is None:
                    cover = name
                    comic_records[cover.name] = comic_records.get(
                        cover.name, {'imagedata': [], 'comics': []}
                        )
                if name.name in [i[0] for i in comic_records[cover.name]['comics']]: continue
                if not save_image(name, src):
                    MYSQL.rollback()
                    break
            
                tags, rating, exif = generate_tags(
                    general=get_tags(DRIVER, name, True), 
                    custom=True, rating=True, exif=True
                    )
                
                save_image(name, src, exif)
                hash_ = get_hash(name)

                comic_records[cover.name]['imagedata'].append(
                    (name.name, ' '.join(artists), tags,
                    rating, 3, hash_, src, SITE, href)
                    )
                comic_records[cover.name]['comics'].append(
                    (name.name, cover.name)
                    )
        
            except Exception as error:
                print('\n', error, href, src)
                break
            
        else:
            imagedata = comic_records[cover.name]['imagedata']
            comics = comic_records[cover.name]['comics']

            if (
                MYSQL.execute(INSERT[3], imagedata, many=1) and
                MYSQL.execute(INSERT[4], comics, many=1)
                ):
                
                del comic_records[cover.name]
                MYSQL.execute(DELETE[0], (href,), commit=1)
                
            else:
                MYSQL.rollback()
                break
            
        json.dump(
            comic_records, 
            open(r'Webscraping\comic_data.json', 'w'),
            indent=4
            )

    print()

def start(initial=1, headless=True, mode=1):
    
    global MYSQL, DRIVER

    if mode:
        
        MYSQL = CONNECT()
        DRIVER = WEBDRIVER(headless)

        if initial: 
            
            hrefs = initialize()
            MYSQL.execute(INSERT[0], hrefs, many=1, commit=1)

        page_handler(MYSQL.execute(SELECT[2], (SITE,), fetch=1))
        DRIVER.close()
        return

    import send2trash

    MYSQL = CONNECT()
    DRIVER = WEBDRIVER(headless, None)

    path = USER / r'Downloads\Images\Comics'
    folders = list(path.iterdir())
    if not (length := len(folders)): return
    progress = IncrementalBar('Comic', max=length)

    for folder in folders:
        
        progress.next()
        artist = ' '.join(
            ARTIST.get(artist, [artist])[0] for artist in 
            [get_artist(folder.stem.lower())]
            )
        images = [
            (
                num, get_hash(file), name:=get_name(file),
                name.write_bytes(file.read_bytes())
                )
            for num, file in enumerate(folder.iterdir())
            ]
        cover = images[0][2]
        
        for num, hash_, image, _ in images:

            tags, rating = generate_tags(
                general=get_tags(DRIVER, image), 
                custom=True, rating=True, exif=False
                )
            imagedata = MYSQL.execute(INSERT[3], (
                    image.name, artist, tags, rating, 
                    3, hash_, None, None, None
                    )
                )
            comics = MYSQL.execute(INSERT[4], (
                    image.name, cover.name
                    )
                )
            if not (imagedata and comics): break; continue

        MYSQL.commit()
        send2trash.send2trash(str(folder))
        
    print()

    DRIVER.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='comics', 
        )
    parser.add_argument(
        '-i', '--init', type=int,
        help='Initial argument (default 1)',
        default=1
        )
    parser.add_argument(
        '-he', '--head', type=bool,
        help='Headless argument (default True)',
        default=True
        )
    parser.add_argument(
        '-m', '--mode', type=int,
        help='Mode argument (default 1)',
        default=1
        )
    
    args = parser.parse_args()

    start(args.init, args.head, args.mode)