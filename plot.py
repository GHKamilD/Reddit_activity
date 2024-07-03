import matplotlib.pyplot as plt
import ast
import os
import numpy as np
import random

def read_existing_data(filename):
    data = {}
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                author, count = ast.literal_eval(line.strip())
                data[author] = count
    return data

# Choose which data to plot (comment_counter or post_counter)
data = read_existing_data('posty.txt')  # or 'posty.txt' for post data

# Sort the data by count
sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

# Take top 10 and combine the rest
top_10 = sorted_data[:30]
others_sum = sum(count for _, count in sorted_data[30:])

# Add "Others" to the list
#top_10.append(("Others", others_sum))

# Separate the data into two lists for plotting
authors, counts = zip(*top_10)

cmap = plt.get_cmap('tab20')
colors = [cmap(i) for i in np.linspace(0, 1, len(authors))]
random.shuffle(colors)

# Create the horizontal bar chart
plt.figure(figsize=(12, 8))
bars = plt.barh(authors, counts, color=colors)
plt.xlabel('Liczba postów')  # or 'Number of Posts' if using post data
plt.ylabel('Użytkownicy')
plt.title('Najczęściej postujący użytkownicy')  # or 'Posts' if using post data

# Color the "Others" bar differently
bars[-1].set_color('lightgray')



# Add text in the bottom right corner
plt.text(0.95, 0.01, 'Na podstawie postów umieszczonych między 15.05.2024 a 26.06.2024',
         verticalalignment='bottom', horizontalalignment='right',
         transform=plt.gca().transAxes,
         color='gray', fontsize=10)

# Add value labels on the bars
for i, (value, bar) in enumerate(zip(counts, bars)):
    plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{value:,}',
             va='center', ha='left', fontweight='bold')

# Adjust layout and display
plt.tight_layout()
plt.gca().invert_yaxis()  # To have the highest count at the top
plt.savefig('posty.png')  # or 'author_posts_top10_with_others.png' if using post data
plt.show()