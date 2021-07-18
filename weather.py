
import tkinter as tk
import requests
from PIL import Image,ImageTk
import json
from io import BytesIO
import datetime

APPID = "4aff35c2c2b88dccc44d0c99a4427977"

def write_into_file(data):
    with open('data.json','w') as file:
        json.dump(data,file)

def getweather(window):
    city = textfield.get()
    api_response_url = "https://api.openweathermap.org/data/2.5/weather?q= "+ city + "&appid=" + APPID
    response = requests.get(api_response_url)
    response_data = response.json()
    write_into_file(response_data)

    try:
        #icons api
        icons_url = f"http://openweathermap.org/img/wn/{response_data['weather'][0]['icon']}@2x.png"
        icons_response = requests.get(icons_url)
        icon_data = icons_response.content
        icon_image = ImageTk.PhotoImage(Image.open(BytesIO(icon_data)))

        #country flags api
        country_flag_url = f"https://www.countryflags.io/{response_data['sys']['country']}/shiny/64.png"
        country_flag_response = requests.get(country_flag_url)
        country_flag_data = country_flag_response.content
        country_flag = ImageTk.PhotoImage(Image.open(BytesIO(country_flag_data)))

        #take data from the response
        condition = (response_data['weather'][0]['main'])

        #changing background image
        bg_image_data= Image.open('./Images/' +condition +'.jpg')  
        image_resized = bg_image_data.resize((700,700),Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(image_resized)

        temp = int(response_data['main']['temp']-273)
        temp_min = int(response_data['main']['temp_min']-273)
        temp_max = int(response_data['main']['temp_max']-273)
        pressure = response_data['main']['pressure']
        humidity = response_data['main']['humidity']
        wind = response_data['wind']['speed']
        sunrise_unix = response_data['sys']['sunrise']
        sunrise = datetime.datetime.fromtimestamp(sunrise_unix)
        sunset_unix = response_data['sys']['sunset']
        sunset = datetime.datetime.fromtimestamp(sunset_unix)
        final_data = f"{condition} \n  {temp}℃"
        final_info = f'Min Temp: {temp_min}℃ \n Max Temp: {temp_max}℃ \n Pressure: {pressure} \n Humidity: {humidity} \n Wind: {wind} \n Sunrise: {sunrise} \n Sunset: {sunset}'
        label1.config(text=final_data)
        label2.config(text=final_info)

        #added image
        label3.configure(image=bg_image)
        label3.image =(bg_image)
        icons_label.configure(image=icon_image)
        icons_label.image= (icon_image)
        country_flag_label.configure(image=country_flag)
        country_flag_label.image=(country_flag)
    except KeyError:
        label1.config(text= response_data['message'])
        label2.config(text= response_data['cod'])
    




window = tk.Tk()
window.title("Weather App")
window.geometry("700x700")

#read image
bg_image_data= Image.open('./Images/bg3.jpg')  
image_resized = bg_image_data.resize((700,700),Image.ANTIALIAS)
bg_image = ImageTk.PhotoImage(image_resized)
label3 = tk.Label(window,image=bg_image)
label3.place(x=0,y=0) 

#textfield added
textfield = tk.Entry(window,bg='white',justify='center',font=('poppins',35,'bold'),width=20)
textfield.pack(pady=20)

#button added
button=tk.Button(window,text="Get Weather")
button.pack()
button.bind('<Button>',getweather)

icons_label = tk.Label(window,bg='#afafaf')
icons_label.pack()
label1 = tk.Label(window,bg='#afafaf',font =('poppins',20,'bold'))
label1.pack()
country_flag_label = tk.Label(window,bg='#afafaf')
country_flag_label.pack()
label2 = tk.Label(window,bg='#afafaf',font =('poppins',20,'bold'))
label2.pack()

window.mainloop()
