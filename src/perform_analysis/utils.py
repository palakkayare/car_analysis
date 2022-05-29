import matplotlib.pyplot as plt
from io import BytesIO
import base64
from sklearn.cluster import KMeans


def get_image():
    # Creates a bytes buffer for the image to save
    # plt.switch_backend('AGG')
    buffer = BytesIO()
    # Creates the plot with the use of BytesIO object as its 'file'
    plt.savefig(buffer, format= 'png')
    # Set the cursor the beginning of the stream
    buffer.seek(0)
    # retreive the entire content of the 'file'
    image_png = buffer.getvalue()

    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    # free the memory of the buffer
    buffer.close()

    return graph

def get_clean_data(df):
    df['car'] = df.Make + ' ' + df.Model
    c = ['Make','Model','car','Variant','Body_Type','Fuel_Type','Fuel_System','Type','Drivetrain','Ex-Showroom_Price','Displacement','Cylinders',
        'ARAI_Certified_Mileage','Power','Torque','Fuel_Tank_Capacity','Height','Length','Width','Doors','Seating_Capacity','Wheelbase','Number_of_Airbags']
    df_full = df.copy()
    df['Ex-Showroom_Price'] = df['Ex-Showroom_Price'].str.replace('Rs. ','',regex=False)
    df['Ex-Showroom_Price'] = df['Ex-Showroom_Price'].str.replace(',','',regex=False)
    df['Ex-Showroom_Price'] = df['Ex-Showroom_Price'].astype(int)
    df = df[c]
    df = df[~df.ARAI_Certified_Mileage.isnull()]
    df = df[~df.Make.isnull()]
    df = df[~df.Width.isnull()]
    df = df[~df.Cylinders.isnull()]
    df = df[~df.Wheelbase.isnull()]
    df = df[~df['Fuel_Tank_Capacity'].isnull()]
    df = df[~df['Seating_Capacity'].isnull()]
    df = df[~df['Torque'].isnull()]
    df['Height'] = df['Height'].str.replace(' mm','',regex=False).astype(float)
    df['Length'] = df['Length'].str.replace(' mm','',regex=False).astype(float)
    df['Width'] = df['Width'].str.replace(' mm','',regex=False).astype(float)
    df['Wheelbase'] = df['Wheelbase'].str.replace(' mm','',regex=False).astype(float)
    df['Fuel_Tank_Capacity'] = df['Fuel_Tank_Capacity'].str.replace(' litres','',regex=False).astype(float)
    df['Displacement'] = df['Displacement'].str.replace(' cc','',regex=False)
    df.loc[df.ARAI_Certified_Mileage == '9.8-10.0 km/litre','ARAI_Certified_Mileage'] = '10'
    df.loc[df.ARAI_Certified_Mileage == '10kmpl km/litre','ARAI_Certified_Mileage'] = '10'
    df['ARAI_Certified_Mileage'] = df['ARAI_Certified_Mileage'].str.replace(' km/litre','',regex=False).astype(float)
    df.Number_of_Airbags.fillna(0,inplace= True)
    df['price'] = df['Ex-Showroom_Price'] * 0.014
    df.drop(columns='Ex-Showroom_Price', inplace= True)
    df.price = df.price.astype(int)
    HP = df.Power.str.extract(r'(\d{1,4}).*').astype(int) * 0.98632
    HP = HP.apply(lambda x: round(x,2))
    TQ = df.Torque.str.extract(r'(\d{1,4}).*').astype(int)
    TQ = TQ.apply(lambda x: round(x,2))
    df.Torque = TQ
    df.Power = HP
    df.Doors = df.Doors.astype(int)
    df.Seating_Capacity = df.Seating_Capacity.astype(int)
    df.Number_of_Airbags = df.Number_of_Airbags.astype(int)
    df.Displacement = df.Displacement.astype(int)
    df.Cylinders = df.Cylinders.astype(int)
    df.columns = ['make', 'model','car', 'variant', 'body_type', 'fuel_type', 'fuel_system','type', 'drivetrain', 'displacement', 'cylinders',
                'mileage', 'power', 'torque', 'fuel_tank','height', 'length', 'width', 'doors', 'seats', 'wheelbase','airbags', 'price']
    return df

def get_clusters(df):
    df = df[df.price < 60000]
    num_cols = [ i for i in df.columns if df[i].dtype != 'object']
    km = KMeans(n_clusters=8, n_init=20, max_iter=400, random_state=0)
    clusters = km.fit_predict(df[num_cols])
    df['cluster'] = clusters
    df.cluster = (df.cluster + 1).astype('object')

    return df

color = {'Mahindra Xuv500':'#481769', 'Tata Hexa':'#481769', 'Toyota Innova Crysta':'#481769', 'Jeep Compass':'#481769', 'Toyota Corolla Altis':'orange', 'Honda Civic':'#481769', 'Hyundai Elantra':'#481769', 'Hyundai Tucson':'#481769', 'Tata Harrier':'#481769', 'Skoda Octavia':'#481769', 'Datsun Go':'#481769', 'Tata Tiago':'#481769', 'Maruti Suzuki Ignis':'#481769', 'Renault Triber':'#481769', 'Premier Rio':'#481769', 'Toyota Etios Liva':'#481769', 'Tata Bolt':'#481769', 'Hyundai Xcent Prime':'#481769', 'Maruti Suzuki Dzire Tour':'#481769', 'Hyundai Elite I20':'#481769', 'Volkswagen Polo':'#481769', 'Maruti Suzuki Dzire':'#481769', 'Ford Freestyle':'#481769', 'Volkswagen Ameo':'#481769', 'Ford Aspire':'#481769', 'Toyota Platinum Etios':'#481769', 'Toyota Etios Cross':'#481769', 'Mahindra Verito Vibe':'#481769', 'Fiat Urban Cross':'#481769', 'Toyota Glanza':'#481769', 'Fiat Avventura':'#481769', 'Honda Jazz':'#481769', 'Mahindra Kuv100 Nxt':'#481769', 'Maruti Suzuki Swift':'#481769', 'Tata Altroz':'#481769', 'Tata Tigor':'#481769', 'Tata Zest':'#481769', 'Honda Amaze':'#481769', 'Maruti Suzuki Gypsy':'#481769', 'Hyundai Venue':'#481769', 'Tata Nexon':'#481769', 'Fiat Linea':'#481769', 'Mahindra Bolero Power Plus':'#481769', 'Maruti Suzuki Vitara Brezza':'#481769', 'Hyundai I20 Active':'#481769', 'Ford Ecosport':'#481769', 'Renault Duster':'#481769', 'Hyundai Verna':'#481769', 'Mahindra Xuv300':'#481769', 'Renault Lodgy':'#481769', 'Volkswagen Vento':'#481769', 'Honda Brv':'#481769', 'Mahindra Thar':'#481769', 'Force Gurkha':'#481769', 'Maruti Suzuki Xl6':'#481769', 'Mahindra Tuv300 Plus':'#481769', 'Mahindra Marazzo':'#481769', 'Mahindra Scorpio':'#481769', 'Ford Figo':'#481769', 'Maruti Suzuki Baleno':'#481769', 'Hyundai Grand I10':'#481769', 'Fiat Linea Classic':'#481769', 'Nissan Sunny':'#481769', 'Maruti Suzuki Ertiga':'#481769', 'Maruti Suzuki Baleno Rs':'#481769', 'Honda Wr-V':'#481769', 'Mahindra Tuv300':'#481769', 'Maruti Suzuki S-Cross':'#481769', 'Renault Captur':'#481769', 'Mahindra Xylo':'#481769', 'Kia Seltos':'#481769', 'Nissan Terrano':'#481769', 'Tata Safari Storme':'#481769', 'Hyundai Grand I10 Nios':'#481769', 'Hyundai Xcent':'#481769', 'Nissan Micra':'#481769', 'Mahindra Bolero':'#481769', 'Maruti Suzuki Ciaz':'#481769', 'Skoda Rapid':'#481769', 'Hyundai Creta':'#481769', 'Tata Tiago Nrg':'#481769', 'Mahindra Nuvosport':'#481769', 'Nissan Kicks':'#481769', 'Fiat Punto Evo':'#481769', 'Toyota Yaris':'#481769', 'Mahindra Verito':'#481769', 'Honda City':'#481769'}
palette = {'Maruti Suzuki':'#46327e', 'Datsun':'#46327e', "Renault":'#46327e', 'Premier':'#46327e', 'Volkswagen':'#46327e', 'Ford':'#46327e', 'Fiat':'#46327e', 'Force':'#46327e', 'Nissan':'#46327e', 'Mahindra':'#46327e', 'Tata':'#46327e', 'Toyota':'orange', 'Jeep':'#46327e', 'Honda':'#46327e', 'Kia':'#46327e', 'Hyundai':'#46327e', 'Skoda':'#46327e'}