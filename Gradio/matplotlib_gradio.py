import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt

data={'Month':['Jan','Feb', 'Mar','Apr', 'May', 'Jun' ],
     "Sales":[11500,13900,15400,13000,17000,15500],
     'Profit':[2000,2100,2500,1800,3800,3500]}

df= pd.DataFrame(data)

def plot_graph(plot_type):
    
    fig=plt.figure(figsize=(10,5))
    
    if plot_type == 'Line Plot':
        
        plt.plot(df['Month'],df['Sales'],color='blue', marker='s',linestyle='-',label='Sales')
        plt.title('Sales Trend over Month')
        plt.xlabel('Months')
        plt.ylabel('Sales in $')
        plt.grid(True)
        plt.legend()
        
    elif plot_type == 'Stacked Bar Plot':
        width=0.3
        plt.bar(df['Month'],df['Sales'], width= width,color='blue',label='Sales')
        plt.bar(df['Month'],df['Profit'], width= width,color='red',label='Sales',bottom=df['Sales'])
        plt.title('Sales And Profit over Month')
        plt.xlabel('Months')
        plt.ylabel('Sales in $')
        plt.grid(True)
        plt.legend()
    
    elif plot_type == 'pie Chart':
        
        plt.pie(df['Profit'], labels=df['Month'], autopct='%1.2f%%',startangle= 45, colors=plt.cm.Paired.colors)  
        plt.title('Profit by Month')
        
    elif plot_type == 'Scatter Plot':
        
        plt.scatter(df['Sales'], df['Profit'],color='green',s =100, edgecolors='black')
        plt.title('Sales Vs Profit over months')
        plt.xlabel('Months')
        plt.ylabel('Sales in $')
        plt.grid(True)
        
    elif plot_type == 'Histogram':
        plt.hist(df['Sales'],bins=5,color='lightgreen', edgecolor='black')
        plt.title('Sales Distribution')
        plt.xlabel('Sales')
        plt.ylabel('Frequency')

        
    elif plot_type == 'Box Plot':
        plt.boxplot(df['Profit'],vert=False, patch_artist=True, boxprops=dict(facecolor='lightgreen'))
        plt.title('Sales Box plot')
        plt.ylabel('Sales')
    
    plt.tight_layout()
    return fig         
    
    
# gradio ui

demo = gr.Interface(
    fn=plot_graph,
    inputs=gr.Radio(['Line Plot', 'Stacked Bar Plot', 'pie Chart', 'Scatter Plot', 'Histogram', 'Box Plot'], label='Select Plot Type'),
    outputs=gr.Plot(label='Sales Data Visualization'),
    title='Sales & Profit Visual insights',
    description='choose a plot type to visualize the sales and profit data over the months.',
)

demo.launch()