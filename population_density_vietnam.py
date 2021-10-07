# In[1]
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Acquiring the population data from the web

# data = pd.read_html(
#     'https://meta.vn/hotro/dien-tich-va-dan-so-cac-tinh-viet-nam-10058')

# for population_data in data:
#     print(population_data)

# population_data.to_excel(r'E:\GIS\PopulationVietNam\pop.xlsx')

# In[2]
population_data = pd.read_excel(
    r'E:\GIS\PopulationVietNam\pop.xlsx', skiprows=[0])

# In[3]

population_data = population_data[[
    'Tỉnh/Thành phố', 'Dân số (người)']]
population_data.rename(columns={'Tỉnh/Thành phố': 'District',
                       'Dân số (người)': 'Population'}, inplace=True)


# In[4]
population_data['Population']
count = len(population_data['Population'])
for i in range(0, count):
    pop = population_data['Population'][i]
    new_pop = float(pop.replace(".", ""))
    population_data.replace(pop, new_pop, inplace=True)

    # area = population_data['Area'][i]
    # new_area = float(area)
    # population_data.replace(area, new_area, inplace=True)

# In[]

nep_districts = gpd.read_file(
    r'E:\GIS\PopulationVietNam\VNM_adm\VNM_adm1.shp')

nep_districts = nep_districts[['NAME_1', 'geometry']]
nep_districts.rename(columns={'NAME_1': 'District'}, inplace=True)

# In[]
nep_districts.to_crs(epsg=32645, inplace=True)

# In[]


population_data.replace('Đắk Nông', 'Đăk Nông', inplace=True)
population_data.replace('Thành phố Hồ Chí Minh',
                        'Hồ Chí Minh city', inplace=True)
population_data.replace('Thừa Thiên Huế', 'Thừa Thiên - Huế', inplace=True)

for index, row in nep_districts['District'].iteritems():
    if row in population_data['District'].tolist():
        pass
    else:
        print('The district ', row, ' is NOT in the population_data list')

# In[]
nep_districts['Area'] = nep_districts.area/1000000

# In[]
nep_districts = nep_districts.merge(population_data, on='District')

# In[]
nep_districts['pop_den (people/sq. km)'] = nep_districts['Population'] / \
    nep_districts['Area']
# In[]
nep_districts.plot(column='pop_den (people/sq. km)',
                   cmap='Spectral', legend=True, figsize=(6, 12))

# %%
