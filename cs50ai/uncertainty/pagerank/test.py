import random
page = {'1.html': {'2.html'}, '2.html': {'1.html', '3.html'}, '3.html': {'4.html', '2.html'}, '4.html': {'2.html'}}

n=10

linked_pages = []
all_pages = []
for key, value in page.items():
    linked_pages.append(key)
    all_pages.append(value)

for i in range(10):
    rand_page = random.choice(list(page.keys()))
    print(rand_page)

print("linked pages:", linked_pages)
print("$"*80)
print("all_pages:", all_pages)
print("$"*80)
for i in range(10):
    select = random.choices([linked_pages, all_pages], [0.85, 0.15], k=1)
    print(f"select {i}:", select)

visit_count = dict()
for _ in range(n):
    rand_page = random.choice(list(page.keys()))
    if rand_page in visit_count:
        visit_count[rand_page] += 1
    else:
        visit_count[rand_page] = 1
    print(f"random page {_}:", rand_page)
    print("visit count:",visit_count)

sum = 0
for key, value in visit_count.items():
    print("key:", key)
    print("value:", value)
    visit_count[key] = value / n
    print("visit count:", visit_count)
    sum += visit_count[key]
print("final count:", visit_count)
print("sum:", sum)
