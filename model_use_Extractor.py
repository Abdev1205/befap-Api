import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
import string
from nltk.corpus import stopwords
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

warnings.filterwarnings("ignore")


def remove_punctuation_marks(text):
    punctuation_marks = dict(
        (ord(punctuation_mark), None) for punctuation_mark in string.punctuation
    )
    return text.translate(punctuation_marks)


def get_lemmatized_tokens(text):
    normalized_tokens = nltk.word_tokenize(remove_punctuation_marks(text.lower()))
    return [
        nltk.stem.WordNetLemmatizer().lemmatize(normalized_token)
        for normalized_token in normalized_tokens
    ]


temp_text = ""


def get_average(values):
    greater_than_zero_count = total = 0
    for value in values:
        if value != 0:
            greater_than_zero_count += 1
            total += value
    # print(total, greater_than_zero_count, '\n')
    try:
        return (
            total / greater_than_zero_count
        )  # -----------------------------------------------------------------
    except:
        print(total, greater_than_zero_count, "\n", temp_text)
        return 0.5 / 25


def get_threshold(tfidf_results):
    i = total = 0
    while i < (tfidf_results.shape[0]):
        total += get_average(tfidf_results[i, :].toarray()[0])
        i += 1
    return total / tfidf_results.shape[0]


def get_summary(documents, tfidf_results, handicap=0.85):
    summary = ""
    i = 0
    while i < (tfidf_results.shape[0]):
        if (get_average(tfidf_results[i, :].toarray()[0])) >= get_threshold(
            tfidf_results
        ) * handicap:
            summary += " " + documents[i]
        i += 1
    return summary


def summary_func(text="", handicap=0.9):  # Use this
    # documents = purifier(text)
    global temp_text
    temp_text = text
    documents = nltk.sent_tokenize(text)

    tfidf_results = TfidfVectorizer(
        tokenizer=get_lemmatized_tokens, stop_words=stopwords.words("english")
    ).fit_transform(documents)
    return get_summary(documents, tfidf_results, handicap)


# print(
#     summary_func(
#         text=""" This product is very super ,and i like bass and smooth sound. it's worth for this price.its very comfortable .and battery also super.Iam impress to captured and edit this product. please rating my picture. 1 to 10READ MORE Good sound quality , with very soft bud and high bass . The look is very attractive and light weight product. Best quality earbuds under affordable pricing. Lovely product it's best for gym workoutREAD MORE Thanks to flipkart for fastest delivered only in 13 hr and the y1 is a quality product, super bass and sound clarity is good.READ MORE A very well crafted piece of audio delivery by Boult Audio. I really liked the fit, the build and the capacity to play high and low notes in this earbuds. I'm totally in love with the connectivity and how well does the Bluetooth connection works. Used it in few meetings and the sound delivery is perfect and without any delay. Value for money!!READ MORE I was in search of new trends design earbuds and i found this, it is stylish and new design by boult loved it.. i can easily connect it to laptop and phone it just takes second.. it's sound quality is superb and it has good battery power support good earbuds at this price ,case cap is doing well job hereREAD MORE Best product at this price range:- Small box, easily fits in pocket- Stylish look- Awesome Bass, Best at this price- comfort fit, doesnt fall even if you dance- Small and cool to use- Battery, yet to discover- expecting better outcomeHighly recommended if you are a Bass lover...READ MORE Excellent sound and bass. The sound quality is amazing and remains decent on high volume too. It comes with long battery which is sufficient for a whole day. Overall it's a good value for money deal. Don't think just go for it! Loved it!READ MORE Honest review of this product :Build and design : NiceBattery backup : Awesome , upto 8 hrs in single charge.Mic quality : Good , not for calling professionals. Sound Quality : Good Buy this product if your budget is 1300. These are the best at this price of your budget is 1000 you can checkout movi dupods F30.READ MORE The quality of the product is like dreams, thank you so much boult for creating such an amazing product that too is this budget. Everything about the product is outstanding from sound quality to bass to design. Hatts to the sound engineer for the equilar. The best product in the Indian market.READ MORE As you can see in pics I have two more earbuds and earpods of boult audio and on that basis I can say Sound quality in these earphones are amazing. The mids are crisp and clear, the vocals are good the bass is also heavy. ... These boult earphones are really budget friendly and has some good premium features.. so big 👍READ MORE""".replace(
#             "READ MORE" or "..." or "..", " "
#         ),
#         handicap=0.85,
#     )
#)
