This project implements a web search engine on UIC domain. This project was developed as a part of the Information retrieval course in Spring 2020. A more detailed information on the project is available in the report. Please refer to report.pdf.
How to run the code: python3 main.py
Components:
1. Web crawler: Web search engines get their information by web
crawling from site to site. Web crawler is implemented in parallel by using the Queue module to access the resources in a synchronised way.
2. Pre-processing: Crawled pages are then pre-processed to remove the noise of search results and also improve the performance of search engine.
3. Vector space model: Vector Space Model is used to represent text documents (and any objects, in general) as vectors of identifiers, such as index terms.
4. Page rank algorithm: Page Rank Algorithm built for the UIC domain extracts information from all the URL’s of the UIC. The collected data includes texts, phrases from the valid HTML tags, URL’s pointed by and to the current URL. The related data is crawled and indexed and stored in the filesystem. When users perform a search query by specifying the search term, the related query is transferred to the search engine index and optimisation algorithms are performed to retrieve SERPs.
5. UI: User Interface is designed in a simple way as with any other search engine. A text box is placed where the user can enter the search query and a search button is placed. As user enters the search query and clicks on the button search results are displayed on screen.
Conclusions:
The query dependent page rank algorithm implemented can be tweaked further based on multiple query terms and make it more efficient a model. The probability function can also be reviewed to achieve better precision.
