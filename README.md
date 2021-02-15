# Best Universities to Study Abroad in 2021

Data Scraped from:
- Times Higher Education - World University Rankings: https://www.timeshighereducation.com/world-university-rankings/2020/world-ranking#!/page/0/length/25/sort_by/rank/sort_order/asc/cols/stats
- GDP Data 2020: https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)
## Demo:
Link: https://bestuniversitiesanalysis.herokuapp.com/
![Alt Text](https://github.com/kadatatlukishore/Best-Universities-to-Study-Abroad-2021/blob/main/captured.gif)
## Steps involved :
1. [Data collection](https://github.com/kadatatlukishore/Best-Universities-to-Study-Abroad-2021/tree/main/Data%20Collection)      
2. [Data Preparation](https://github.com/kadatatlukishore/Best-Universities-to-Study-Abroad-2021/tree/main/Data%20Preparation)
3. WebApp for visualization - [app.py](https://github.com/kadatatlukishore/Best-Universities-to-Study-Abroad-2021/blob/main/app.py)

### Directory Tree
```
├── Data Collection 
|     ├── UniversityDataExtraction(filename:tableextractor.py) - Web Scraping
|     ├── GDPData2020(filename:GDPdata2020.py) - Web Scraping
├── Data preparation 
├── Data
|     ├── UniversityData
|     ├── Data related to countries
├── app.py
├── requirements.txt
├── setup.sh
|__ Procfile

```
## Setup Instructions:
The Code is written in Python 3.8. If you don't have Python installed you can find it [here](https://www.python.org/downloads/). 
```bash
git clone https://github.com/kadatatlukishore/Best-Universities-to-Study-Abroad-2021.git
cd Best-Universities-to-Study-Abroad-2021
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 app.py
```
## Technologies Used:
[<img target="_blank" src="https://ih1.redbubble.net/image.411682602.8572/st,small,845x845-pad,1000x1000,f8f8f8.u2.jpg" width=50>](https://www.python.org) [<img target="_blank" src="https://blog.eduonix.com/wp-content/uploads/2018/12/Linear-Discriminant-Analysis.jpg" width=100>](https://scikit-learn.org/stable/) [<img target="_blank" src="https://pbs.twimg.com/profile_images/1187765724451868673/uVw1PWA7.png" width=50>](https://pandas.pydata.org/)[<img target="_blank" src="https://discoversdkcdn.azureedge.net/runtimecontent/companyfiles/6617/2328/thumbnail.png?v131141820642441697" width=50>](https://scrapy.org/)
[<img target="_blank" src="https://assets.website-files.com/5dc3b47ddc6c0c2a1af74ad0/5e18182db827fa0659541754_RGB_Logo_Vertical_Color_Light_Bg.png" width=80>](https://www.streamlit.io/) [<img target="_blank" src="https://images.prismic.io/plotly-marketing-website/bd1f702a-b623-48ab-a459-3ee92a7499b4_logo-plotly.svg?auto=compress,format" width=80>](https://plotly.com/) [<img target="_blank" src="https://miro.medium.com/max/3600/1*fIjRtO5P8zc3pjs0E5hYkw.png" width=100>](https://www.heroku.com/)

-  If you find any problems in the site, kindly [reach us](https://www.linkedin.com/in/kishorekadatatlu/)
