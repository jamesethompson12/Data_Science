# check required packages are installed 

required_packages <- c('gapminder', 'dplyr', 'rbokeh', 'ggplot2', 'tidyverse')

lib_install_load <- function(libraries, warnings = FALSE)
   for (this_lib in libraries) {
      if (require(this_lib, quietly = warnings, character.only = TRUE) == FALSE)
      {
         install.packages(this_lib)
      }
      library(this_lib, character.only = TRUE, quietly = warnings)
   }

lib_install_load(required_packages)




# hold gapminder data in local variable for easy viewing
gapminder_dat <- gapminder

gapm_2002 <- gapminder_dat %>% 
   filter(year == 2002)


# plot of life expectancy vs GDP per capita for 2002
figure(data = gapm_2002, 
       title = 'Global life expectancy vs. GDP per capita for 2002', 
       xlab = 'GDP per capita', 
       ylab = 'Life Expectancy (yrs)', 
       legend_location = 'bottom_right') %>%
   ly_points(x = gdpPercap, y = lifeExp, color = continent, hover = c(continent, country, pop))


 
# plot UK's GDP value over time
gapminder_UK <- gapminder_dat %>% 
   mutate(gdp_pop_millions = gdpPercap * pop / 10^6) %>%
   filter(country == 'United Kingdom')
    
figure(data = gapminder_UK, title = 'UK GDP value over time', xlab = 'Year', ylab = 'GDP * population (millions)') %>%
   ly_lines(x = year, y = gdp_pop_millions, width = 2)



# plot Europe's life expectancy over time with a line to specifically indicate the UK
gapminder_Europe <- gapminder_dat %>%
   filter(continent == 'Europe')

uk_line <- lm(lifeExp ~ year, gapminder_UK)



figure(tools = 'resize', 
       data = gapminder_Europe, 
       title = 'European life expecancy over time (with UK line)', 
       xlab = 'Year', 
       ylab = 'Life Expectancy (Yrs)', 
       legend_location = 'bottom_right') %>%
   ly_points(x = year, y = lifeExp, color = country, alpha = 0.5) %>%
   ly_abline(uk_line)

# ggpolt2 reproduction of above graph for demo purposes 
# Wrapped in function to prevent execution (DO NOT EXECUTE!) - Rendering rbokeh and ggplot2 graphs 
# at the same time may cause R to crash
ggplot_ver <- function() {
   gapminder_Europe %>%
       ggplot(aes(x = year, y = lifeExp, color = country)) +
          geom_point(aes(alpha = 0.5)) +
          geom_abline(uk_line) 
}



# mean per continent
 life_exp_continent <- gapminder_dat %>%
    group_by(continent, year) %>%
    summarise(mean_life_exp = mean(lifeExp)) %>%
    spread(key = year, value = mean_life_exp) %>%
    transpose()
