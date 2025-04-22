#!/usr/bin/env python
# coding: utf-8

# In[1]:


# get_ipython().system('pip install pandas plotly')


# In[2]:


import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import plotly.io as pio 
import plotly.colors as colors
pio.templates.default = "plotly_white"


# In[3]:


data = pd.read_csv("./Sample - Superstore.csv", encoding="latin-1")



# In[5]:


data.info()


# In[4]:


data['Order Date'] = pd.to_datetime(data['Order Date'])


# In[5]:


data['Ship Date'] = pd.to_datetime(data['Ship Date'])


# In[6]:


data['Order Month'] = data['Order Date'].dt.month
data['Order Year'] = data['Order Date'].dt.year
data['Order Day of Week'] = data['Order Date'].dt.dayofweek


# In[7]:


salesbymonth = data.groupby('Order Month')['Sales'].sum().reset_index()


# In[128]:


fig1 = px.line(salesbymonth,
             x='Order Month',
             y='Sales',
              title='Monthly Sales Analysis')


# In[15]:


salesbycategory = data.groupby('Category')['Sales'].sum().reset_index()


# In[129]:


fig2 = px.pie(salesbycategory,
            values='Sales',
            names='Category',
            hole=0.2,
            color_discrete_sequence=px.colors.qualitative.Pastel)
fig2.update_traces(textposition='inside',textinfo='percent+label')
fig2.update_layout(title_text='Sales Analysis by Catergory')


# In[17]:


salesbysubcategory = data.groupby('Sub-Category')['Sales'].sum().reset_index()


# In[130]:


fig3= px.bar(salesbysubcategory,
           x='Sub-Category',
           y='Sales',
           title='Sales by Sub-Catergory',

           )


# In[19]:


Profitbymonth = data.groupby('Order Month')['Profit'].sum().reset_index()


# In[131]:


fig4=px.line(Profitbymonth,
           x= 'Order Month',
          y='Profit',
          title='Profit by Month',)



# In[64]:


profitbycategorysubcategory = data.groupby('Sub-Category')['Profit'].sum().reset_index()


# In[132]:


fig5= px.bar(profitbycategorysubcategory,
           x='Sub-Category',
           y='Profit',
           title='Profit by Sub-Catergory',

           )




# In[69]:


salesprofitbysegment = data.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()


# In[70]:


color_palette = px.colors.qualitative.Pastel


# In[133]:


fig6=go.Figure()
fig6.add_trace(go.Bar(x=salesprofitbysegment['Segment'],
                     y=salesprofitbysegment['Sales'],
                     name='Sales',

                     marker_color=color_palette[0],
                     width=0.4))
fig6.add_trace(go.Bar(x=salesprofitbysegment['Segment'],
                     y=salesprofitbysegment['Profit'],
                     name='Profit',
                     marker_color=color_palette[1],
                     width=0.4))

fig6.update_layout(title='Sales and Profit Analysis by Customer Segment',
                 xaxis_title='Customer Segment',yaxis_title='Amount')


# In[134]:


salesprofitbysegment = data.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
salesprofitbysegment['Sales_to_Profit_Ratio'] = salesprofitbysegment['Sales']/salesprofitbysegment['Profit']
(salesprofitbysegment[['Segment','Sales_to_Profit_Ratio']])


# In[135]:


import dash
from dash import dcc, html



# In[123]:


app = dash.Dash('SalesDashboard')
server = app.server 

# In[122]:


import nest_asyncio
nest_asyncio.apply()
from dash.dependencies import Input, Output


# In[124]:


all_figs = {
    'fig1': fig1,
    'fig2': fig2,
    'fig3': fig3,
    'fig4': fig4,
    'fig5': fig5,
    'fig6': fig6,
}


# In[125]:


app.layout = html.Div([
    html.H1("Sales Interactive Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Choose Theme:"),
        dcc.RadioItems(
            id='theme-toggle',
            options=[
                {'label': '🌞 Light Theme', 'value': 'plotly'},
                {'label': '🌚 Dark Theme', 'value': 'plotly_dark'}
            ],
            value='plotly',  # default theme
            inline=True,
            labelStyle={'marginRight': '20px'}
        )
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    html.Div(id='charts-container', style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(450px, 1fr))',
        'gap': '20px',
        'padding': '10px'
    })






])


# In[126]:


@app.callback(
    Output('charts-container', 'children'),
    Input('theme-toggle', 'value')
)
def update_theme(selected_theme):
    styled_charts = []

    for i in range(1, 7):
        fig = all_figs[f'fig{i}']
        fig.update_layout(template=selected_theme)
        styled_charts.append(html.Div([
            dcc.Graph(figure=fig)
        ], style={
            'backgroundColor': '#1e1e1e' if selected_theme == 'plotly_dark' else 'white',
            'padding': '15px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 6px rgba(0,0,0,0.2)'
        }))

    return styled_charts



# In[127]:


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=10000)



# In[ ]:




