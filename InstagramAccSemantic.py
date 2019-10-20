from langdetect import detect
import requests
import json


class iAccount:
    '''
    `textList` - Список в котором хранятся все текстовые значения(если они имеются) ,
        которые пользователь оставил у себя под постами
        
    `ru_threshold` - Доля подписей под постами(хранятся в `textList`) на русском языке
        К примеру у пользователя 10 постов и текст под ними написан на следующих языках
        [en,en,ru,ru,ru,unknown,unknown,ru,en,ru]
        Доля русских подписей считается : Кол-во(ru) / (Общее Кол-во - Кол-во(unknown))
        Если это доля больше чем `ru_threshold` ,мы считаем что пользователь русский
        *Info: Значение Unknown бывает когда пользователь подписал пост не текстовым значением , например, emoji
        или вообще неичего не подписал
        
        `lang_bio` - Язык на котором написана биография пользователя у него в профиле, если она есть
        
        `is_ru` - Хранит значение русскоговорящий/нерусскоговорящий
    '''
    
    
    def __init__(self):
        
        self.textList = []
        self.ru_threshold = 0.25
        self.lang_bio = None
        self.is_ru = None
    
    def lang_verify(self,text):
        '''
        Определяет язык на котором написан текст
        
        Inputs: text (текст)
        Return: lang (язык на котором написан текст)
        
        '''
        try:
            lang = detect(text)
        except:
            lang='unknown'

        return lang
    
    def ru_share(self):
        '''
        Считает долю русскоязычных постов в медиа и отдает конечный результат, является ли владелец аккаунта
        русскоязычным или же нет
        
        Inputs:None
        Return: ru/ru_negative/unknown
        '''
    
        if len(self.textList) - self.textList.count('unknown') == 0:
            return 'unknown'
        else:
            if self.textList.count('ru')/(len(self.textList) - self.textList.count('unknown')) > 0.25:
                return 'ru'
            else:
                return 'ru_negative'
    
        
    def collect_media_lang(self,media):
        '''
        Собирает текст под постами и определяет язык на котором они написаны
        
        Inputs: media - JSON содержащий данные о всех медиа 
        Return: None
        '''
    
        for post in range(len(media)):  
            try:
                post_text = media[post]['node']['edge_media_to_caption']['edges'][0]['node']['text']
                self.textList.append(self.lang_verify(post_text))
            except Exception:
                pass
    
    def true_russian(self,r):       
        '''
        Определяет русскоговорящий пользователь или нет
        
        Inputs: r (r = requests.get("https://www.instagram.com/%username%/?__a=1"))
        Return:None
        '''
        
        if r.status_code == 200:
            user = r.json()
            bio = user['graphql']['user']['biography']
            
            # Если биография аккаунта заполнена и на русском языке , то аккаунт считается русскоязычным
            # Если биография пуста или не на русском языке ,то переходим к лингвистическому анализу медиа
            if (bio != '') and (self.lang_verify(bio)) == 'ru':
                    self.is_ru = 'ru'
                    
            else:
                media = user['graphql']['user']['edge_owner_to_timeline_media']['edges']
                if len(media) > 0:
                    self.collect_media_lang(media)
                    self.is_ru = self.ru_share()
                else:
                    self.is_ru = 'unknown'
        
        else:
            self.is_ru = 'request failed'
            
if __name__=='__main__':
    
    test_acc=["https://www.instagram.com/kevin/?__a=1",
              "https://www.instagram.com/keti_guchi/?__a=1",
              "https://www.instagram.com/eva.__init__/?__a=1"]
    
    for acc in test_acc:
        r=requests.get(acc)
        InstagramAcc = iAccount()
        InstagramAcc.true_russian(r)
        print("{} - {}".format(acc,InstagramAcc.is_ru))