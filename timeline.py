import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# Set up the argument parser
parser = argparse.ArgumentParser()
parser.add_argument("csv", help="path to the CSV file")
args = parser.parse_args()

# Read the CSV file
chartdata = pd.read_csv(args.csv, encoding='latin1')

# Convert the 'timeline' column to datetime format
dates = pd.to_datetime(chartdata['timeline'])

# Get the minimum and maximum dates
min_date = date(np.min(dates).year - 1, np.min(dates).month, np.min(dates).day)
max_date = date(np.max(dates).year + 1, np.max(dates).month, np.max(dates).day)

# Get the event labels
labels = chartdata['event']

# Combine the labels and dates into a single list of strings
labels = ['{0:%d %b %Y}:\n{1}'.format(d, l) for l, d in zip (labels, dates)]

# Create a figure and axis object using matplotlib
fig, ax = plt.subplots(figsize=(12, 40))

# Set the interval between events
interval = 5

# Set the limits for the x and y axes to start from the top
_ = ax.set_xlim(-26, 20)
_ = ax.axvline(0, ymin=0, ymax=len(dates) * interval + 1, c='deeppink', zorder=1)

# Add a vertical line at x=0
_ = ax.axvline(0, ymin=0.05, ymax=len(dates) * interval, c='deeppink', zorder=1)

# Create fake date values that are equally spaced by the interval and in descending order
fake_d = np.arange(len(dates), 0, -1) * interval

# Add scatter plots at the fake dates
_ = ax.scatter(np.zeros(len(fake_d)), fake_d, s=120, c='palevioletred', zorder=2)
_ = ax.scatter(np.zeros(len(fake_d)), fake_d, s=30, c='darkmagenta', zorder=3)

# Create label offsets to position the labels to the left or right of the vertical line
# Increase the offset values to add more padding between the labels
label_offsets = np.repeat(6.0, len(fake_d))
label_offsets[1::2] = -6.0

# Add the labels to the plot, aligning them to the left or right of the vertical line
for i, (l, d) in enumerate(zip(labels, fake_d)):
    align = 'right'
    if i % 2 == 0:
        align = 'left'
    _ = ax.text(label_offsets[i], d, l, ha=align, fontfamily='serif', 
                fontweight='bold', color='royalblue',fontsize=12)

# Create horizontal line values to connect the labels to the scatter plots
stems = np.repeat(6.0, len(fake_d))
stems[1::2] *= -1.0

# Add horizontal lines to connect the labels to the scatter plots
x = ax.hlines(fake_d, 0, stems, color='darkmagenta')

# Hide the lines around the chart
for spine in ["left", "top", "right", "bottom"]:
    _ = ax.spines[spine].set_visible(False)

# Hide the tick labels
_ = ax.set_xticks([])
_ = ax.set_yticks([])

# Set the title for the chart
_ = ax.set_title('Timeline of Events', 
                 fontweight="bold", 
                 fontfamily='serif', 
                 fontsize=10, 
                 color='darkgreen')

# displays the plot
plt.show()
