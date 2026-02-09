county_df = df.loc[(df['countycode'] != 0) &
                  (df['state'] != 'US')]

# county_df = df.loc[(df['countycode'] != 0) &
#                   (df['state'] != 'US') &
#                   (df['state'] == 'CA')]

county_df['year'] = pd.Categorical(county_df['year'], ordered = True)
county_df['obesity_percent'] = (county_df['obesity']*100)
county_df['county_drop'] = county_df['county'].str.replace(' County', '')
county_df = county_df.round(2)

state_interest = county_df.loc[county_df['state'] == 'CA']

county_bar = px.bar(state_interest,
                   x = 'county_drop',
                   y = var_of_interest,
                   title = '______ Percentages in CA Counties')
county_bar.update_xaxes(tickangle = 60)

county_shape = gpd.read_file(here('data/cb_2018_us_county_5m.shp'))
county_shape = county_shape.clean_names(case_type = 'snake')
county_shape = county_shape.rename(columns = {'statefp': 'statecode',
                                              'countyfp': 'countycode',
                                              'name': 'county_drop'})
county_shape = county_shape.loc[:, ['statecode', 'countycode', 'county_drop', 'geoid', 'geometry']]
county_shape[['statecode', 'countycode', 'geoid']] = county_shape[['statecode', 'countycode', 'geoid']].astype(int)

county_shape.head()

all_county_mappo = county_shape.merge(county_df).set_index('fipscode')
county_mappo = county_shape.merge(state_interest).set_index('fipscode')
print(county_mappo.head())

# county_shape = gpd.read_file(here('data/cb_2018_us_county_5m.shp'))
# county_shape = county_shape.clean_names(case_type = 'snake')
# county_shape = county_shape.rename(columns = {'statefp': 'statecode',
#                                               'countyfp': 'countycode',
#                                               'name': 'county_drop'})
# county_shape = county_shape.loc[:, ['statecode', 'countycode', 'county_drop', 'geoid', 'geometry']]
# county_shape[['statecode', 'countycode', 'geoid']] = county_shape[['statecode', 'countycode', 'geoid']].astype(int)

# all_county_mappo = county_shape.merge(county_df).set_index('fipscode')
# county_mappo = county_shape.merge(state_interest).set_index('fipscode')
# print(county_mappo.head())


# all counties in US
all_county_min_value = all_county_mappo[var_of_interest].min()
all_county_max_value = all_county_mappo[var_of_interest].max()

# county
county_obesity_map = px.choropleth(all_county_mappo,
                    geojson = all_county_mappo['geometry'],
                    locations = all_county_mappo.index,
                    color = var_of_interest,
                    color_continuous_scale = 'Viridis',
                    range_color = [all_county_min_value, all_county_max_value],
                    scope = 'usa')
county_obesity_map.show()

pn.ggplot.show(
  pn.ggplot(all_county_mappo.loc[all_county_mappo['state'] == 'CA'])
  + pn.geom_map(pn.aes(fill = 'life_expect'))
  + pn.scale_x_continuous(limits = [-124, -114])
  + pn.scale_y_continuous(limits = [42, 32])
  + pn.theme_classic()
)

# all counties in CA
county_min_value = county_mappo[var_of_interest].min()
county_max_value = county_mappo[var_of_interest].max()

# county
county_obesity_map = px.choropleth(county_mappo,
                    geojson = county_mappo['geometry'],
                    locations = county_mappo.index,
                    color = var_of_interest,
                    color_continuous_scale = 'Viridis',
                    range_color = [county_min_value, county_max_value],
                    center = {'lat': 36.7783, 'lon': -119.4179},
                    fitbounds = 'locations',
                    scope = 'usa')
county_obesity_map.show()