import json
import model_use_Extractor as extractor
import model_use_review_Classifier as review_pairs
import flipkart_scraper
import amazon_scraper
import pandas as pd
from functools import cmp_to_key
import sys
import os

# os.chdir('Backend/Final')
search_keyword = sys.argv[1]
# search_keyword = "laptop"
df_f = flipkart_scraper.flipkart_scraper_func(search_keyword=search_keyword)
df_f.to_json("df_f.json", orient="records")  # -------------------------------

df_a = amazon_scraper.amazon_scraper_func(
    search_keyword=search_keyword, sr_no=df_f["Srno"].iloc[-1] + 1
)
if df_a.empty:
    product_details = df_f
else:
    df_a.to_json("df_a.json", orient="records")  # -------------------------------
    product_details = pd.concat([df_f, df_a], ignore_index=True)

merged_reviews = ""
review_extract_list = []
review_params_list = []
temp_product_reviews_list = list(product_details["Reviews"])


for review_list in temp_product_reviews_list:
    merged_reviews = (" ".join(review_list)).strip()
    if merged_reviews != "":
        review_extract_list.append(
            extractor.summary_func(text=merged_reviews, handicap=0.85)
        )
        review_params_list.append(review_pairs.sentiment_func(review_list))
    else:
        review_params_list.append([0, 0])
        review_extract_list.append("No Review")
    merged_reviews = ""
    # print("ERROR Encountered...Dumping : \n\n", review, '\n', review_list, merged_reviews)


product_details.update({"Reviews": review_extract_list})
product_details["Review_Params"] = review_params_list

rank_list = []
tot_review_list = [i[1] for i in review_params_list]
price_list = list(product_details["Price"])

max_reviews = max(tot_review_list)
min_reviews = min(tot_review_list)
max_price = max(price_list)
min_price = min(price_list)

norm_price = lambda price: (price - min_price) / (max_price - min_price)
norm_reviews = (
    lambda no_of_reviews: (no_of_reviews - min_reviews) / (max_reviews - min_reviews)
    if max_reviews != min_reviews
    else 1
)
rank = lambda e, price: (1 / (1 + 2.7183 ** (-35 * (e[0] - 0.535)))) * norm_reviews(
    e[1]
) - norm_price(price)

for index, row in product_details.iterrows():
    rank_list.append(
        [row["Srno"], row["Ratings"], rank(row["Review_Params"], row["Price"])]
    )


def A(x):
    return x[2]


def B(x):
    return x[1]


def cmp_with(f, x, y):
    fx = f(x)
    fy = f(y)
    if fx < fy:
        return -1
    elif fx > fy:
        return 1
    else:
        return 0


rank_list.sort(
    reverse=True, key=cmp_to_key(lambda x, y: cmp_with(A, x, y) or cmp_with(B, x, y))
)
rank_list = [int(i[0]) for i in rank_list]

product_details.to_json("final_products.json", orient="records")

with open("rank_list.json", "w") as f:
    json.dump(rank_list, f)
