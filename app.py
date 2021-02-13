import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

st.set_page_config(layout="wide")
st.markdown("""
<style>
body {
    color: black;
    background-color: white ;
}
</style>
    """, unsafe_allow_html=True)

html_temp = f"""
        <body style="background-color:red;">
        <div style="background-color:#212F3D ;padding:10px">
        <h1 style="color:white;text-align:center;">Best Universities to Study Abroad(2021)</h1>
        </div>
        </body>
        """
st.markdown(html_temp, unsafe_allow_html=True)

# st.markdown("<h1 style='text-align: center; color: black;'>Welcome to our project!!!!</h1>", unsafe_allow_html=True)
with st.beta_expander("How it works:"):
    text = '''Selecting any subject/course will give you the results of number of best universities around the world. Then after 
    selecting any country that provide the selected subject will result in the dashboard of that particular country
    and it also provides the best universities in that country and by selecting any university will give the dashboard of University key stats.
    '''
    st.write(text)


@st.cache
def load_data():
    data = pd.read_csv('Data/UniversityData.csv')
    gdpdata = pd.read_csv('Data/finalgdpdata.csv')
    unemployment = pd.read_csv('Data/Unemploymentdata.csv')
    investment = pd.read_csv('Data/Investmentoneducation.csv')
    gdp_20 = pd.read_csv('Data/2020GDP.csv')
    return data, gdpdata, unemployment, investment, gdp_20


def plots(Universities_of_country):
    html_temp1 = """
        <body style="background-color:red;">
        <div style="background-color:#DB7093 ;padding:6px">
        <h2 style="color:white;text-align:center;">University Key_stats:</h2>
        </div>
        </body>
        """
    st.markdown(html_temp1, unsafe_allow_html=True)
    st.subheader('Select the University:point_down: :-')
    selected_university = st.selectbox(label='Universities',
                                       options=Universities_of_country['UniversityName'].values)
    University_data = Universities_of_country[Universities_of_country['UniversityName'] == selected_university]
    subjects = list(University_data['subjects_offered'].values)
    col11, col22 = st.beta_columns([1.2, 1])
    with col11:
        st.subheader(f"List of Subjects offered in {selected_university}:")
        length = len(subjects[0])
        rowEvenColor = 'lightgrey'
        rowOddColor = 'white'
        fig = go.FigureWidget(data=[go.Table(
            header=dict(values=['Subjects_offered'], fill_color='paleturquoise', align='left',
                        font=dict(color='black', size=15)),
            cells=dict(values=[subjects[0].split(',')],
                       fill_color=[[rowOddColor, rowEvenColor] * (length // 2)], align='left',
                       font=dict(color='black', size=13)))])

        st.plotly_chart(fig)

    # st.dataframe({'Subjects_Offered': subjects[0].split(',')})
    ratio = list(University_data['FemaletoMaleRatio'].values)
    University_data = University_data.assign(Female_ratio=(int(ratio[0].split(':')[0])))
    University_data.loc[:, 'Male_ratio'] = int(ratio[0].split(':')[1])

    University_data.loc[:, 'Resident_students'] = University_data['Total_Num_of_Students'] - University_data[
        'Num_of_Intl_students']
    students_count = [University_data['Resident_students'].values[0],
                      University_data['Num_of_Intl_students'].values[0]]
    staff_ratio = University_data['StudentStaffRatio'].values[0]
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{}, {"type": "domain"}],
               [{"colspan": 2}, None]],
        subplot_titles=(" ", "Female to Male ratio", "Residential&International Students"))
    fig.add_trace(go.Indicator(value=staff_ratio, align="center", number={'font': {'color': '#316D94'}},
                               title={"text": "Student to Staff Ratio:"}, domain={'x': [0, 0.5], 'y': [0.5, 1]}))
    female_to_male_ratio1 = [University_data['Female_ratio'].values[0], University_data['Male_ratio'].values[0]]

    fig.add_trace(go.Pie(labels=['Female', 'Male'], values=female_to_male_ratio1, scalegroup='one',
                         marker=dict(colors=['#BB8FCE', '#316D94'], line=dict(color='#000000', width=2))), 1, 2)

    fig.add_trace(go.Bar(x=['ResidentialStudents', 'International_students'], y=students_count,
                         marker={'color': students_count, 'colorscale': 'Earth'}), row=2, col=1)
    fig.update_layout(height=650, width=700, showlegend=True,
                      title=dict(text=f"{selected_university} Key Stats"))
    col22.plotly_chart(fig)
    university_location(University_data['UniversityRank'].values[0], selected_university,
                        University_data['Latitude'].values, University_data['Longitude'].values)


def country_stats(gdp, unemploymentdata, Investment_data, gdp_2020, country):
    st.text("...")
    if country in gdp['Countries'].values:
        country_gdp_data = gdp[gdp['Countries'] == country].drop(['Unnamed: 0'], axis=1).dropna(axis=1).iloc[:, :-1].T

        values_ = []
        for x in country_gdp_data.values:
            values_.append(x[0])

        fig11 = go.Figure(go.Scatter(x=country_gdp_data.index, y=values_, mode='lines+markers',
                                     marker=dict(size=8, line=dict(width=2, color='black')), name='GDP'))
        fig11.update_layout(width=700, height=300, title='GDP of the country over the years')
        st.plotly_chart(fig11)

    if country in gdp_2020['Countries'].values:
        gdp2 = gdp_2020[gdp_2020['Countries'] == country]['GDP(US$millions)'].values[0]
        gdp21 = gdp2.split(',')
        fig22 = go.Figure(go.Indicator(value=float(''.join(gdp21)), align="center",
                                       number={'font': {'color': '#316D94'}, 'prefix': "(USmillion$)"},
                                       title={"text": "GDP in 2020"}))
        fig22.update_layout(width=700, height=225)
        st.plotly_chart(fig22)

    if country in unemploymentdata['Country Name'].values:
        unemployment_country_data = unemploymentdata[unemploymentdata['Country Name'] == country].dropna(axis=1).iloc[:,
                                    2:].T
        values_2 = []
        for x in unemployment_country_data.values:
            values_2.append(x[0])

        fig33 = go.Figure(go.Scatter(x=unemployment_country_data.index, y=values_2, mode='lines+markers',
                                     marker=dict(color='Red', size=8, line=dict(width=2, color='black')),
                                     name='UnemploymentRate'))
        fig33.update_layout(width=700, height=300, title='Unemployment Rate in the country over the Years')
        st.plotly_chart(fig33)

    if country in Investment_data['Country Name'].values:
        Investment_on_education = Investment_data[Investment_data['Country Name'] == country].dropna(axis=1).iloc[:,
                                  1:].T

        values_3 = []
        for x in Investment_on_education.values:
            values_3.append(x[0])
        fig44 = go.Figure(go.Scatter(x=Investment_on_education.index, y=values_3, mode='lines+markers',
                                     marker=dict(color='Green', size=8, line=dict(width=1, color='black'))))
        fig44.update_layout(width=700, height=300, title='Investment_on_education(%of GDP)')

        st.plotly_chart(fig44)
        if len(Investment_on_education) < 5:
            st.error(f"{country} has less data Investment_of_GDP(%) on Education")


def university_location(Universityrank, university, lat, lon):
    column111, column222 = st.beta_columns(2)
    with column111:
        university_location_map = folium.Map(location=[lat, lon], zoom_start=13)
        folium.Marker(location=(lat, lon), popup=university).add_to(university_location_map)
        folium_static(university_location_map)
    with column222:
        rank = go.Figure(go.Indicator(value=Universityrank, align="center",
                                      number={'font': {'color': '#316D94'}},
                                      title={"text": "University Rank all over the world"}))
        rank.update_layout(width=700, height=500)

        st.plotly_chart(rank)


df, gdpdf, unemployment_data, Investment, gdp_202 = load_data()
subjects_offered = list(
    set(i for i in df["subjects_offered"].str.cat(sep=',').replace(', ', ',').split(',') if i))
subjects_offered.sort()
st.subheader('Select the subject:point_down: :-')
selected_subject = st.selectbox(label='subjects', options=subjects_offered)
if selected_subject:
    country_data = df.loc[df['subjects_offered'].str.contains(selected_subject, regex=True)]
    country = list(country_data['Country'].value_counts().nlargest(30).index)
    number_of_universities = list(country_data['Country'].value_counts().nlargest(30).values)
    col1, col2 = st.beta_columns([2, 1])
    fig1 = go.Figure(data=go.Choropleth(
        locations=country,  # Spatial coordinates
        z=number_of_universities,  # Data to be color-coded
        locationmode='country names',  # set of locations match entries in `locations`
        colorscale='Reds',
        colorbar=dict(len=1, title="Count")
    ))
    fig1.update_layout(width=800, height=500,
                       title_text=f"Number of universities in a country that provide '{selected_subject}'",
                       geo=dict(
                           showframe=False
                       )
                       )
    col1.plotly_chart(fig1)
    fig = go.FigureWidget(data=[go.Bar(y=country, x=number_of_universities, orientation='h')])
    fig.update_layout(width=550, height=550, yaxis=dict(autorange="reversed"))
    col2.plotly_chart(fig)
    st.subheader('Select the Country:point_down: :-')
    selected_country = st.selectbox(label="countries", options=country)
    html_temp = f"""
                <body style="background-color:red;">
                <div style="background-color:#DB7093 ;padding:6px">
                <h2 style="color:white;text-align:center;">{selected_country} Stats:</h2>
                </div>
                </body>
                """
    st.markdown(html_temp, unsafe_allow_html=True)
    column1, column2 = st.beta_columns([1.2, 1])

    with column1:
        geolocator = Nominatim(user_agent='project')
        try:
            location = geolocator.geocode(selected_country, timeout=10)
            if location is not None:
                latitude = location.latitude
                longitude = location.longitude
                st.subheader(f"Universities that provide {selected_subject} in {selected_country}")
                fig = folium.Map(location=[latitude, longitude], zoom_start=5)
                list_of_universities = country_data[country_data['Country'] == selected_country].dropna(axis=0)
                colors = ['lightblue', 'lightgreen', 'orange', 'red']
                for lat, lon, university in zip(list_of_universities['Latitude'].values,
                                                list_of_universities['Longitude'].values,
                                                list_of_universities['UniversityName'].values):
                    folium.CircleMarker(location=(lat, lon), popup=university, radius=7, color='b',
                                        fill_color=random.choice(colors),
                                        fill=True,
                                        fill_opacity=0.8
                                        ).add_to(fig)
                folium_static(fig)
            else:
                st.error(f"Sorry couldn't get the location {selected_subject}")
        except:
            st.error("THERE IS SOMETHING WRONG WITH THE SERVER... WAIT OR RELOAD!!")

        st.info('Note: Here, some of the locations are misleading..')
    selected_country_universities = country_data[country_data['Country'] == selected_country]

    plots(selected_country_universities)
    with column2:
        country_stats(gdpdf, unemployment_data, Investment, gdp_202, selected_country)

expander = st.beta_expander("About us:")
with expander:
    st.write("We are students of NIT Nagaland. We've done this project to give the information for the people \
    who want to study abroad.")
    st.write("Data source : ")
    st.write(
        "1) https://www.timeshighereducation.com/world-university-rankings/2020/world-ranking#!/page/0/length/25/sort_by/rank/sort_order/asc/cols/stats")
    st.write("2) https://data.worldbank.org/")
    st.write("3) https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)")

Reach_us = st.beta_expander('Reach Us:')
with Reach_us:
    st.write("Devanshi: https://www.linkedin.com/in/devanshi-mishra-nitn")
    st.write("Kishore: https://www.linkedin.com/in/kishorekadatatlu")

Project_repo = st.beta_expander("Project Repo:")
with Project_repo:
    st.write('github: https://github.com/kadatatlukishore/Best-Universities-to-Study-Abroad-2021 ')
