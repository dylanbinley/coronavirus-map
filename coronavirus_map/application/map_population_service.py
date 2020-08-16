# we need a service that runs the full pipeline:
#     1. pulls new data from GDELT
#     2. filters out irrelevant data
#     3. plots relevant data
#     4. writes map to HTML file
# the following code impliments part of that pipeline and can be combined with
# training_scripts.domain.news_retrieval_service for full effect

# todo: import news retrieval service
import coronavirus_map.domain.news_filtering_service as news_filtering_service
import coronavirus_map.domain.map_generation_service as map_generation_service

# todo: create retriever
filterer = news_filtering_service.NewsFilteringService()
mapper = map_generation_service.MapGenerationService()

# todo: use retriever to get data_dicts
covid_data_dicts = filterer.find_coronavirus_stories(data_dicts)
plotly_map = mapper.generate_map(covid_data_dicts)
# todo: write plotly map to html file
plotly_map.show()
