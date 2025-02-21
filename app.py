from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as urlreq

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin() # required for cloud, not for local deplyoment
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            client = urlreq(flipkart_url)
            flipkartPage = client.read()
            client.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.find_all("div",{"class":"cPHDOP col-12-12"})
            del bigboxes[0:2]
            box = bigboxes[0]
            # print(type(box))
            productLink="https://www.flipkart.com"+bigboxes[0].div.div.div.a['href']
            # print("cool 2")
            prodRes = requests.get(productLink)
            prodRes.encoding = 'utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            commentboxes = prod_html.find_all("div",{"class","RcXBOT"})
            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    # name.encode(encoding='utf-8')
                    print("name")
                    name = commentbox.div.div.find("div",{"class":"row gHqwa8"}).div.p.text

                except:
                    name = 'No Name'

                try:
                    # rating.encode(encoding='utf-8')
                    print("rating")
                    rating = commentbox.div.div.div.div.text


                except:
                    rating = 'No Rating'

                try:
                    print("header")
                    # commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    print("review")
                    custComment = commentbox.div.div.find("div",{"class":"ZmyHeo"}).div.text
                    # custComment.encode(encoding='utf-8')
                    # custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ", e)

                print("dict creation")
                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}

                reviews.append(mydict)
                print("appending")
            return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8001, debug=True)
    app.run(debug=True)