import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Calculate BMI
weight = df['weight']
height = df['height']/100
BMI = weight.div(height.pow(2))

# Add 'overweight' column
df['overweight'] = BMI > 25
df['overweight'] = df['overweight'].map({True: 1, False: 0})

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = df['cholesterol'].map({1: 0, 2: 1, 3: 1})
df['gluc'] = df['gluc'].map({1: 0, 2: 1, 3: 1})

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars = 'cardio', value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    # df_cat = None

    # Draw the catplot with 'sns.catplot()'
    g = sns.catplot(x = 'variable', hue = 'value', col = 'cardio', kind = 'count', order = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'], data = df_cat)
    g.set_ylabels('total')
    fig = g.fig
    # snippet adapted from comment in "Getting 2 errors: test_line_plot_labels" (https://forum.freecodecamp.org/t/getting-2-errors-test-line-plot-labels/428555/5) by too0ky (https://forum.freecodecamp.org/u/too0ky); accessed October 7, 2021

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi'])
              & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975))
              & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr(method = 'pearson')

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr))
    # snippet from "How to create a Triangle Correlation Heatmap in seaborn – Python?" (https://www.geeksforgeeks.org/how-to-create-a-triangle-correlation-heatmap-in-seaborn-python/) by Vanshika Goyal (https://auth.geeksforgeeks.org/user/vanshikagoyal43/articles), used under CC BY-SA (https://creativecommons.org/licenses/by-sa/4.0/) / adapted from original; accessed October 5, 2021

    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(data = corr, annot = True, fmt = '.1f', mask = mask, cmap = 'icefire')

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig