> ### Tidy Data Project: Cleaning an Olympic Medalist Dataset :dancers:

This Jupyter Notebook explores and implements the principles of tidy data laid out in [*Tidy Data* by Hadley Wickham](https://vita.had.co.nz/papers/tidy-data.pdf). The file 
`olympic_08_medalists.csv` has been adapted from [Giorgio Comai's data](https://edjnet.github.io/OlympicsGoNUTS/2008/) and lists every medalist from the 2008 Summer Olympics.
In accordance with the principles, each variable is in its own column and each observation forms its own row.

---

#### Notebook Organization :notebook_with_decorative_cover:

* Data Cleaning & Tidy Process
  * Introduction to Data
    * *`pandas`, `seaborn`, and `matplotlib.pyplot` are imported*
  * Tidy Data Principle: Each Variable in its Own Column
    * *`pd.melt()` and `str.split` are used to melt the data and divide variables into separate columns*
* Visualizations
  * Overall Medal Distribution
  * Medalists by Sex
  * Medalists per Sport
* `pivot_table` Aggregation
  * *Table is created that records the number of medalists in each place for each sport.*
 
---

> ### Visualizations Created :bar_chart:

![image](https://github.com/user-attachments/assets/b5803fef-5caa-42c2-a845-79daab87fb1f)  

---

![image](https://github.com/user-attachments/assets/0d8fff13-42c4-4f32-96b3-dcce83270fda)  

---

![image](https://github.com/user-attachments/assets/9d8f15e2-5998-4968-88b3-6c9ab102747e)
