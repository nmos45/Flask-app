def appropriate(review):
    review = review.split()
    new_review = ""
    infile = open("censored.txt",'r')
    infile = infile.readlines()
    censored_words = [line.strip() for line in infile]
    for word in review:
        word = word.lower()
        if word in censored_words:
            new_review += '*' * len(word) + ' '
        else:
            new_review += word + ' '
    return new_review



print(appropriate("HELLO you fuck"))



# def appropriate(review):
#     result = False
#     new_review = ""
#     infile = open("censored.txt",'r')
#     infile = infile.readlines()
#     for word in review:
#         if word in censored_words:
#             new_review += '*' * len(word)
#         else:
#             new_review += word
#     return new_review
