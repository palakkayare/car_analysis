# Django and project related imports
from django.shortcuts import render
from .forms import CsvForm 
from .models import Csv
from django.contrib.auth.decorators import login_required
from .utils import get_clean_data, get_clusters, get_image, color, palette

# Extra library imports for data analysis
import base64
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans

@login_required
def upload_file_view(request):
    error_message = None
    success_message = None
    form = CsvForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvForm()
        try:
            obj = Csv.objects.get(activated=False)
            obj.save()
            success_message ="Uploaded successfully"
        except Exception as e:
            print(e)
            error_message="Oops. Something went wrong...." 
    context = {
        'form': form,
        'success_message': success_message,
        'error_message': error_message,
    }    
    return render(request, 'perform_analysis/upload.html', context)

@login_required
def analysis_view(request):
    table = ""
    primary_height = 600
    secondary_height = 400
    csv = Csv.objects.get(activated=False)
    df = pd.read_csv(csv.file_name.path)
    cleaned_df = get_clean_data(df)
    plt.switch_backend('AGG')

    # Check important features within the dataset
    l_D = len(df)
    c_m = len(df.Make.unique())
    c_c = len(df.Model.unique())
    n_f = len(df.columns)
    fig = px.bar(x=['Observations',"Makers",'Models','Features'],y=[l_D,c_m,c_c,n_f], width=800,height=400)
    fig.update_layout(
        title="Important features of our dataset",
        xaxis_title="",
        yaxis_title="Counts",
        font=dict(
            size=16,
        )
    )

    bytess = fig.to_image(format="png", width=600, height=350, scale=2)
    imp_features = base64.b64encode(bytess).decode('ascii')

    # Distribution of cars price data in normal and log scales.

    fig,(ax1,ax2) = plt.subplots(2,1,figsize=(14,11))
    sns.histplot(data=cleaned_df, x='price',bins=50, alpha=.6, color='darkblue', ax=ax1)
    ax12 = ax1.twinx()
    sns.kdeplot(data=cleaned_df, x='price', alpha=.2,fill= True,color="#254b7f",ax=ax12,linewidth=0)
    ax12.grid()
    ax1.set_title('Histogram of cars price data',fontsize=16)
    ax1.set_xlabel('')
    logbins = np.logspace(np.log10(3000),np.log10(744944.578),50)
    sns.histplot(data=cleaned_df, x='price',bins=logbins,alpha=.6, color='darkblue',ax=ax2)
    ax2.set_title('Histogram of cars price data (log scale)',fontsize=16)
    ax2.set_xscale('log')
    ax22 = ax2.twinx()
    ax22.grid()
    sns.kdeplot(data=cleaned_df, x='price', alpha=.2,fill= True,color="#254b7f",ax=ax22,log_scale=True,linewidth=0)
    ax2.set_xlabel('Price (log)', fontsize=14)
    ax22.set_xticks((800,1000,10000,100000,1000000))
    ax2.xaxis.set_tick_params(labelsize=14)
    ax1.xaxis.set_tick_params(labelsize=14)
    cars_price_data = get_image()


    # Box plot of price varience

    plt.figure(figsize=(12,6))
    sns.boxplot(data=cleaned_df, x='price',width=.3,color='blue', hue= 'fuel_type')
    plt.title('Box plot of Price',fontsize=18)
    plt.xticks([i for i in range(0,800000,100000)],[f'{i:,}$' for i in range(0,800000,100000)],fontsize=14)
    plt.xlabel('price',fontsize=14)
    box_plot_price = get_image()

    # Cars by body type
    plt.figure(figsize=(16,7))
    sns.countplot(data=cleaned_df, y='body_type',alpha=.6,color='darkblue')
    plt.title('Cars by car body type',fontsize=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('')
    plt.ylabel('')
    cars_by_cars_body_type = get_image()

    # Box plot of Price of every body type
    plt.figure(figsize=(18,6))
    sns.boxplot(data=cleaned_df, x='price', y='body_type', palette='viridis')
    plt.title('Box plot of Price of every body type',fontsize=18)
    plt.ylabel('')
    plt.yticks(fontsize=14)
    plt.xticks([i for i in range(0,800000,100000)],[f'{i:,}$' for i in range(0,800000,100000)],fontsize=14)
    box_plot_price_of_every_bodytype = get_image()

    # Cars count by fuel type
    plt.figure(figsize=(11,6))
    sns.countplot(data=cleaned_df, x='fuel_type',alpha=.6, color='darkblue')
    plt.title('Cars count by engine fuel type',fontsize=18)
    plt.xlabel('Fuel Type', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylabel('')
    cars_count_by_fuel_type = get_image()

    # Cars count by engine size
    plt.figure(figsize=(14,6))
    sns.histplot(data=cleaned_df, x='displacement',alpha=.6, color='darkblue',bins=10)
    plt.title('Cars by engine size',fontsize=18)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    cars_count_by_engine_size = get_image()

    # Cars count by horsepower
    plt.figure(figsize=(14,6))
    sns.histplot(data=cleaned_df, x='power',alpha=.6, color='darkblue')
    plt.title('Cars by horsepower (in CC)',fontsize=18)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    cars_count_by_horsepower = get_image()

    # Main features regarding the car
    table = cleaned_df[cleaned_df.model == "Corolla Altis"].to_html()

    # Relation between horsepower and price
    plt.figure(figsize=(10,8))
    sns.scatterplot(data=cleaned_df, x='power', y='price',hue='body_type',palette='viridis',alpha=.89, s=120 );
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('power',fontsize=14)
    plt.ylabel('price',fontsize=14)
    plt.title('Relation between horsepower and price',fontsize=20)
    relation_between_power_price = get_image()

    # Relation between mileage and price        
    fig = plt.figure(figsize=(10,8))
    ax= fig.add_subplot()
    sns.jointplot(data=cleaned_df, x='mileage', y='price',kind= 'reg',ax=ax, palette='viridis',height=8,  ratio=7)
    ax.text(.5,.7,'Relation between mileage and price', fontsize=18)
    ax.set_xlabel('Power (HP)', fontsize= 15)
    relation_between_mileage_price = get_image()

    # Correlation between variables        
    plt.figure(figsize=(15,8))
    sns.heatmap(cleaned_df.corr(), annot=True, fmt='.2%')
    plt.title('Correlation between differet variable',fontsize=20)
    plt.xticks(fontsize=14, rotation=320)
    plt.yticks(fontsize=14)
    correlation_between_variables = get_image()
            
    # Extensive scatter plot grid of more numerical variable to investigate the realtion in more detail
    sns.pairplot(cleaned_df,vars=[ 'displacement', 'mileage', 'power', 'price'], hue= 'fuel_type',
        palette=sns.color_palette('magma',n_colors=4),diag_kind='kde',height=2, aspect=1.8)
    extensive_scatter_plot = get_image()

    # 3D scatter plot to check for obvious clusters with main features as price horsepower and mileage
    fig = px.scatter_3d(cleaned_df, x='power', z='price', y='mileage',color='make',width=1000,height=950)
    fig.update_layout(showlegend=True)
    bytess = fig.to_image(format="png")
    threeD = base64.b64encode(bytess).decode('ascii')

    context = {
        "imp_features": imp_features,
        "cars_price_data": cars_price_data,
        "box_plot_price": box_plot_price,
        "cars_by_cars_body_type": cars_by_cars_body_type,
        "box_plot_price_of_every_bodytype": box_plot_price_of_every_bodytype,
        "cars_count_by_fuel_type": cars_count_by_fuel_type,
        "cars_count_by_engine_size": cars_count_by_engine_size,
        "cars_count_by_horsepower": cars_count_by_horsepower,
        "relation_between_power_price": relation_between_power_price,
        "relation_between_mileage_price": relation_between_mileage_price,
        "correlation_between_variables": correlation_between_variables,
        "extensive_scatter_plot": extensive_scatter_plot,
        "table": table,
        "primary_height": primary_height,
        "secondary_height": secondary_height,
        "threeD": threeD
    }

    return render(request, 'perform_analysis/analysis_report.html', context)

def cluster_analysis_view(request):
    table = ""
    primary_height = 600
    secondary_height = 400

    csv = Csv.objects.get(activated=False)
    df = pd.read_csv(csv.file_name.path)
    cleaned_df = get_clean_data(df)
    cleaned_df = get_clusters(cleaned_df)

    plt.switch_backend('AGG')


    # Plot of price and power
    plt.figure(figsize=(10,8))
    sns.scatterplot(data=cleaned_df, y='price', x='power',s=120,hue='cluster',palette='viridis')
    plt.legend(ncol=4)
    plt.title('Scatter plot of price and horsepower with clusters predicted', fontsize=18)
    plt.xlabel('power',fontsize=16)
    plt.ylabel('price',fontsize=16)
    price_vs_horsepower = get_image()
    

    # Plot of mileage and power
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=cleaned_df, x='power', y='mileage',s=120,hue='cluster',palette='viridis')
    plt.legend(ncol=4)
    plt.title('Scatter plot of milage and horsepower with clusters', fontsize=18)
    plt.xlabel('power',fontsize=16)
    plt.ylabel('mileage',fontsize=16)
    power_vs_mileage = get_image()
    

    # Plot of fuel tank and engine_size
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=cleaned_df, x='fuel_tank', y='displacement',s=120,hue='cluster',palette='viridis')
    plt.legend(ncol=4)
    plt.title('Scatter plot of engine size and fuel tank with clusters', fontsize=18);
    plt.xlabel('Fuel Tank Capacity ',fontsize=16)
    plt.ylabel('Engine size',fontsize=16)
    fuel_tank_vs_engine_size = get_image()
    
    # 3D Plot of price - mileage - power
    fig = px.scatter_3d(cleaned_df, x='power', z='price', y='mileage',color='cluster',
                    height=700, width=800,color_discrete_sequence=sns.color_palette('colorblind',n_colors=8,desat=1).as_hex(),
                   title='price power, and mileage')
    bytess = fig.to_image(format="png")
    price_vs_power_vs_mileage = base64.b64encode(bytess).decode('ascii')
    

    # Check average price
    plt.figure(figsize=(14,6))
    sns.barplot(data=cleaned_df, x='cluster', ci='sd', y='price', palette='viridis',order=cleaned_df.groupby('cluster')['price'].mean().sort_values(ascending=False).index)
    plt.yticks([i for i in range(0,65000,5000)])
    plt.title('Average price of each cluster',fontsize=20)
    plt.xlabel('Cluster',fontsize=16)
    plt.ylabel('Avg car price', fontsize=16)
    plt.xticks(fontsize=14)
    average_price = get_image()
    
    
    # Number of cars in each cluster
    plt.figure(figsize=(14,6))
    sns.countplot(data=cleaned_df, x= 'cluster', palette='viridis',order=cleaned_df.cluster.value_counts().index)
    plt.title('Number of cars in each cluster',fontsize=18)
    plt.xlabel('Cluster',fontsize=16)
    plt.ylabel('Number of cars', fontsize=16)
    plt.xticks(fontsize=14)
    cars_count_in_each_cluster = get_image()

    # Cluster of the Toyota Corolla (and its variants)
    clusters_toyota_corolla = cleaned_df[cleaned_df.model == 'Corolla Altis'].to_html()

    # cleaned_df[cleaned_df.model == 'Corolla Altis']

    df_c = cleaned_df[cleaned_df.cluster.isin([1,5])]
    print(df_c['car'].unique())
    
    p_dic = palette
    c_dic = color

    # Price and number of cars in clusters
    order = list(df_c.make.value_counts().index)

    plt.figure(figsize=(8,6))
    sns.countplot(data=df_c, x='make', palette=p_dic, alpha= .9,order=order)
    plt.xlabel('Make',fontsize=16)
    plt.ylabel('Count',fontsize=16)
    plt.title('Car makers in the clusters of the Corolla (and each model variant they have)',fontsize=14)
    make_count_of_cars = get_image()

    plt.figure(figsize=(8,6))
    sns.boxplot(data= df_c, x= 'make', y='price', order=order,palette=p_dic)
    plt.xlabel('Make',fontsize=16)
    plt.ylabel('Price',fontsize=16)
    plt.title('Prices of Car makers (including each model variant they have)',fontsize=14)
    make_price_of_cars = get_image()

    # Count of each body type in the targeted clusters (including variants)
    plt.figure(figsize=(8,6))
    sns.countplot(data=df_c,x='body_type',palette='viridis')
    plt.xlabel('Body type',fontsize=16)
    plt.ylabel('Count of variants',fontsize=16)
    plt.title('count of each body type in the targeted clusters (including variants)',fontsize=14)
    counts_of_body_type_vs_varients = get_image()

    context = {
        "clusters_toyota_corolla": clusters_toyota_corolla,
        "filtered_clusters_toyota_corolla": df_c.to_html(),
        "price_vs_horsepower": price_vs_horsepower,
        "power_vs_mileage": power_vs_mileage,
        "fuel_tank_vs_engine_size": fuel_tank_vs_engine_size,
        "price_vs_power_vs_mileage": price_vs_power_vs_mileage,
        "average_price": average_price,
        "cars_count_in_each_cluster": cars_count_in_each_cluster,
        "make_count_of_cars": make_count_of_cars,
        "make_price_of_cars": make_price_of_cars,
        "counts_of_body_type_vs_varients": counts_of_body_type_vs_varients,
        "primary_height": primary_height,
        "secondary_height": secondary_height
    }

    return render(request, "perform_analysis/cluster_analysis_report.html", context)

@login_required
def show_csv_data(request):
    csv = Csv.objects.get(activated=False)
    df = pd.read_csv(csv.file_name.path)
    return render(request, "perform_analysis/render_csv.html", {'loaded_data' : df.to_html()})

@login_required
def show_cleaned_csv_data(request):
    csv = Csv.objects.get(activated=False)
    df = pd.read_csv(csv.file_name.path)
    cleaned_df = get_clean_data(df)
    return render(request, "perform_analysis/render_csv.html", {'loaded_data' : cleaned_df.to_html()})
        
@login_required
def index_view(request):
    return render(request, "perform_analysis/index.html")

def clustered_data_view(request):
    
    csv = Csv.objects.get(activated=False)
    df = pd.read_csv(csv.file_name.path)
    cleaned_df = get_clean_data(df)
    cleaned_df = get_clusters(cleaned_df)

    return render(request, "perform_analysis/render_csv.html", {'loaded_data' : cleaned_df.to_html()})