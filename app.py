import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.collections import PatchCollection

# Page configuration
st.set_page_config(
    page_title="U.S. Worker Breakdown by Education", layout="wide"
)

st.title("Work Arrangement by Education Level (2023)")
st.write(
    "Interactive visualization based on U.S. Census Bureau survey data."
)

# Sidebar Filter
st.sidebar.header("Controls")
selected_categories = st.sidebar.multiselect(
    "Filter Education Levels:",
    options=[
        "High school or less",
        "Some college",
        "Bachelor's degree",
        "Graduate degree",
    ],
    default=[
        "High school or less",
        "Some college",
        "Bachelor's degree",
        "Graduate degree",
    ],
)

COL_WIDTH = 16
GAP = 4


def get_category_grid(cat_name):
    grid = []
    if cat_name == "High school or less":
        for col in range(COL_WIDTH):
            h = 60 if col == 0 else 59
            col_colors = []
            for row in range(h):
                if row < 2:
                    col_colors.append("yellow")
                elif row == 2 or (row == 3 and col <= 4):
                    col_colors.append("purple")
                else:
                    col_colors.append("red")
            grid.append(col_colors)

    elif cat_name == "Some college":
        for col in range(COL_WIDTH):
            h = 47 if col <= 4 else 46
            col_colors = []
            for row in range(h):
                if row < 3 or (row == 3 and col <= 8):
                    col_colors.append("yellow")
                elif row == 3 or row in (4, 5) or (row == 6 and col <= 2):
                    col_colors.append("purple")
                else:
                    col_colors.append("red")
            grid.append(col_colors)

    elif cat_name == "Bachelor's degree":
        for col in range(COL_WIDTH):
            h = 47 if col <= 14 else 46
            col_colors = []
            for row in range(h):
                if row <= 7 or (row == 8 and col <= 1):
                    col_colors.append("yellow")
                elif row == 8 or (9 <= row <= 14) or (row == 15 and col <= 10):
                    col_colors.append("purple")
                else:
                    col_colors.append("red")
            grid.append(col_colors)

    elif cat_name == "Graduate degree":
        for col in range(COL_WIDTH):
            h = 27 if col <= 11 else 26
            col_colors = []
            for row in range(h):
                if row <= 3 or (row == 4 and col <= 9):
                    col_colors.append("yellow")
                elif row == 4 or (5 <= row <= 9) or (row == 10 and col <= 5):
                    col_colors.append("purple")
                else:
                    col_colors.append("red")
            grid.append(col_colors)

    return grid


if not selected_categories:
    st.info("Select at least one education level from the sidebar to display.")
else:
    fig, ax = plt.subplots(figsize=(9, 10), dpi=200, facecolor="#ffffff")
    ax.set_facecolor("#ffffff")

    patches_red, patches_purple, patches_yellow = [], [], []
    x_positions = []
    current_x = 0

    for cat_name in selected_categories:
        x_positions.append(current_x + COL_WIDTH / 2)
        grid = get_category_grid(cat_name)

        for col_idx, col_colors in enumerate(grid):
            x = current_x + col_idx
            for row_idx, color in enumerate(col_colors):
                rect = plt.Rectangle((x, row_idx), 0.88, 0.88)
                if color == "yellow":
                    patches_yellow.append(rect)
                elif color == "purple":
                    patches_purple.append(rect)
                else:
                    patches_red.append(rect)

        current_x += COL_WIDTH + GAP

    ax.add_collection(
        PatchCollection(patches_red, facecolor="#e38083", edgecolor="none")
    )
    ax.add_collection(
        PatchCollection(patches_purple, facecolor="#9992c3", edgecolor="none")
    )
    ax.add_collection(
        PatchCollection(patches_yellow, facecolor="#f7cf68", edgecolor="none")
    )

    max_x = max(current_x - GAP, 1)

    # Legend Construction
    leg_x = max_x - 1
    leg_y = 66

    ax.text(
        leg_x,
        leg_y,
        "TYPE OF\nWORKER",
        ha="right",
        va="top",
        fontsize=11,
        color="#4a4a4a",
        fontfamily="sans-serif",
        fontweight="normal",
        linespacing=1.05,
    )

    legend_items = [
        ("In person", "#f0a2a1", 11.5),
        ("Hybrid", "#aaa5c5", 8.5),
        ("Fully remote", "#f3d179", 13.5),
    ]

    for idx, (label, color, box_w) in enumerate(legend_items):
        box_h = 3.4
        y_box = leg_y - 7.0 - (idx * 4.5)
        x_box = leg_x - box_w

        box = mpatches.FancyBboxPatch(
            (x_box, y_box),
            box_w,
            box_h,
            boxstyle="round,pad=0.02,rounding_size=0.8",
            facecolor=color,
            edgecolor="none",
            transform=ax.transData,
        )
        ax.add_patch(box)

        ax.text(
            x_box + box_w / 2.0,
            y_box + box_h / 2.0,
            label,
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
            fontfamily="sans-serif",
            color="#2b2b2b",
        )

    # Category Labels
    for x_pos, cat_name in zip(x_positions, selected_categories):
        ax.text(
            x_pos,
            -2.5,
            cat_name,
            ha="center",
            va="top",
            fontsize=12,
            color="#333333",
            fontfamily="sans-serif",
        )

    # Footer Text
    source_note_text = (
        "Source: Current Population Survey of the U.S. Census Bureau (2023)\n"
        "Note: Each square represents 50,000 workers between the ages of 18 and 64. In 2023,\n"
        "there were 143 million workers in this age range."
    )

    ax.text(
        0,
        -7.0,
        source_note_text,
        ha="left",
        va="top",
        fontsize=10.5,
        color="#555555",
        fontfamily="serif",
        linespacing=1.35,
    )

    ax.set_xlim(-1, max_x + 1)
    ax.set_ylim(-13, 67)
    ax.set_aspect("equal")
    ax.axis("off")

    st.pyplot(fig)
