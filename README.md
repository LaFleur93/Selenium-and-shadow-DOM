# Selenium-and-shadow-DOM
This application allows the user to locate and insert values in elements that are under shadow hosts.

<h2> Introduction </h2>

In the Vertical Farming industry, it is vital for the business to have information about the health of the products they are producing. During each production day, the shrinkage must be reported per variety of plant.

This program allows the user to report the shrinkage by simply placing the "Harvest Performance" (HP) in % as it is shown in the picutre. This measures how much of the product can actually be sold compared to the total amount of plants.

<img src="https://github.com/LaFleur93/Selenium-and-shadow-DOM/assets/74310745/e5c7e47b-2d73-4f4a-b922-9234db00edba" width=500px/>

Once the HPs are set, the user can insert all of these values on the company's platform for the many fields in the different farms in a very straightforward way, withouth wasting time going one by one.

<h2> Behind the code </h2>

The program is written on Python using undetected_chromedriver library as webdriver and Selenium to find the elements on the website. The program has to deal with shadow hosts, having to add an extra step to handle elements inside these hosts.
