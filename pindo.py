from requests import Session
from threading import Thread, Lock

mainU = 'https://api.pindo.ir/v1/?page={}'
getInfoU = 'https://api.pindo.ir/v2/advertisement/details/{}/'

mainH = {
    "Accept": "application/json, text/plain, /",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "no-cache",
    "Client": "desktop",
    "ClientId": "10fd90c1-e008-4cef-ab0b-9b6286ae6fec", #if script didnt work place your ClientId here
    "Connection": "keep-alive",
    "Host": "api.pindo.ir",
    "Origin": "https://www.pindo.ir",
    "Referer": "https://www.pindo.ir/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "X-Requested-With": "XMLHttpRequest",
    "supernova-optimize-response": "1"
}

phones = []
lock = Lock()

def getNum(id, session):
    try:
        response = session.get(getInfoU.format(id), headers=mainH)
        response.raise_for_status()
        data = response.json()['data']['advertisement']
        phone = data.get('phone')
        if phone:
            with lock:
                if phone not in phones:
                    phones.append(phone)
                    print(phone)
                    
                    with open("phones.txt", "a") as f:
                        f.write(f"{phone}\n")
    except Exception as e:
        print(f"Error fetching phone for ID {id}: {e}")

def fetch_ads():
    with Session() as session:
        page = 1
        while True:
            try:
                response = session.get(mainU.format(page), headers=mainH)
                if response.status_code != 200:
                    break

                data = response.json()
                if data.get('status') == 200:
                    advertisements = data['data']['advertisements']

                    threads = []
                    for ad in advertisements:
                        thread = Thread(target=getNum, args=(ad['id'], session))
                        thread.start()
                        threads.append(thread)

                    
                    for thread in threads:
                        thread.join()

                page += 1
            except KeyError:
                print("KeyError encountered, skipping page.")
                page += 1
            except Exception as e:
                print(f"Error on page {page}: {e}")
                break

    print('NUMBERS SAVED IN [ "phones.txt" ]')

fetch_ads()
