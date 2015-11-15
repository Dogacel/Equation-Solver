import polyroots

obj = polyroots.polyroots([1,4,6,6,6,4,1],overflow=5,precision=4)
print(obj.solve(-2j))