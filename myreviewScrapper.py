from flask import Flask,render_template,request
from flask_cors import CORS,cross_origin
import requests
import os
from bs4 import BeautifulSoup
print("hello")


app = Flask(__name__)


@app.route('/',methods=['GET'])
@cross_origin()
def home_page():
    return render_template("index.html")

@app.route('/review',methods=['POST'])
@cross_origin()
def review_page():
    print(request,"\n")
    print(request.get_json())
    searchString = request.form['content'].replace(" ","")
    print(searchString)
    try:
        resp = requests.get("https://www.flipkart.com/search?q=" + searchString)
        print(resp.status_code)
        # print(resp.text)

        soup = BeautifulSoup(resp.text, 'html.parser')

        l = soup.find("div", {"class": "_3wU53n"})
        bigboxes = soup.findAll("div", {"class": "bhgxx2 col-12-12"})
        print(bigboxes)
        print("-----")
        del bigboxes[0:3]
        box = bigboxes[0]
        productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
        print(box)
        print("-----")
        print(productLink)

        prodRes = requests.get(productLink)
        prodRes.encoding = 'utf-8'
        prod_soup = BeautifulSoup(prodRes.text, "html.parser")
        # print(prod_soup.text)

        commentBoxes = prod_soup.findAll("div", {"class": "_3nrCtb"})
        print(commentBoxes)
        reviewsList = []
        for comment in commentBoxes:
            try:
                name = comment.findAll("p", {"class": "_3LYOAd _3sxSiS"})[0].text
                print("name=", name)
            except:
                name = "No name"
                print(name)
            try:
                commentHeader = comment.findAll("p", {"class": "_2xg6Ul"})[0].text
                print("header=", commentHeader)
            except:
                commentHeader = "No header"
                print(commentHeader)
            try:
                commentContent = comment.findAll("div", {"class": "qwjRop"})[0].div.div.text
                print("commentContent=", commentContent)
            except:
                commentContent = "No comment"
                print(commentContent)
            try:
                rating = comment.div.div.div.div.text
                print("rating = ", rating)
            except:
                rating = "No rating"
                print(rating)

            mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHeader,
                      "Comment": commentContent}

            reviewsList.append(mydict)

        reviewsList.pop()
        print(reviewsList)
        print(reviewsList[0].keys())
        return render_template("review.html", reviewsList=reviewsList)
    except :
        return render_template("index.html")



port = int(os.getenv("PORT"))
if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
    app.run(host='0.0.0.0', port=port)






