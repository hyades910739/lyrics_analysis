# Lyrics Analysis and Mojim Crawler
last update : Sep.27.2018  
now containing:  


### 1. *crawler.py* :  
爬取魔鏡歌詞網歌詞，只要輸入「專輯頁面」的網址，即可爬取頁面中專輯所有歌曲的歌詞。  

#### 使用方法  
於terminal 中執行:  
```
python crawler.py https://mojim.com/tw100951x23.htm
```
或者編輯多個url的文件(參考*url*檔案)並執行：  

```
python crawler.py $(cat filename)
```
隨便寫的應該有很大改進空間  


### 2. *data_preprocess.py* : 
本專案進行資料處理的部份，回傳vector space model 下wordcount的資料框(*vsm.csv*)  
資料清理大致進行了:  
* 清理歌詞中的雜訊，包括作詞作曲人標記、重複段落標記等  
* 清理小部分停用詞  
* 用googletrans API 進行英文轉中文翻譯  
* 刪去出現次數小於兩次的詞  
> 2018.09.27:  
> 由於目前googletrans 的API出了狀況，暫時直接刪去英文與其他語言  


### 3. *tfidf_classifier.py*
實作基於TFIDF的文字分類器，請參閱：
* MUSIC EMOTION CLASSIFICATION OF CHINESE SONGS BASED ON LYRICS USING TF*IDF AND RHYME
* AUTOMATIC MOOD CLASSIFICATIONUSING TF*IDF BASED ON LYRICS


### Other files:
* stop_cn.txt : 停用詞表
* url : crawler.py用的示範檔案
* label.csv : 情緒標注，使用thayer's model，一二維變數分別為arousal 與valence，以二維(正面與負面)的類別方式表達。兩個變數相結合， 可以四個象限表示，作為情緒分類之標籤。



