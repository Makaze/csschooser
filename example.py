import csschooser

soup = csschooser.get_soup("https://google.com") # Example URL

selector = csschooser.interactive_select(soup)

for tag in soup.select(selector):
    print(tag.get_text().strip())