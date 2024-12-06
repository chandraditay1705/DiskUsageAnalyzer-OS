import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def collect_data(directory):
    """Collect disk usage data for all files and directories."""
    data = []
    for root, dirs, files in os.walk(directory):
        # Collect directory sizes
        for d in dirs:
            dir_path = os.path.join(root, d)
            try:
                size = sum(
                    os.path.getsize(os.path.join(dir_path, f))
                    for f in os.listdir(dir_path)
                    if os.path.isfile(os.path.join(dir_path, f))
                ) / (1024 * 1024)  # Convert to MB
                data.append((dir_path, size, "Directory"))
            except Exception:
                pass

        # Collect file sizes
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
                data.append((file_path, size, "File"))
            except Exception:
                pass

    return pd.DataFrame(data, columns=["Path", "Size_MB", "Type"])


def plot_usage(df, title="Disk Usage"):
    """Generate a bar chart for disk usage."""
    df_sorted = df.sort_values(by="Size_MB", ascending=False)

    plt.figure(figsize=(12, 8))
    plt.barh(df_sorted["Path"], df_sorted["Size_MB"], color="skyblue")
    plt.xlabel("Size (MB)")
    plt.ylabel("Paths")
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def plot_file_type_distribution(df):
    """Generate a pie chart for file type distribution."""
    df_files = df[df["Type"] == "File"]
    file_types = (
        df_files["Path"]
        .str.extract(r"\.([^.]+)$")[0]  # Extract file extensions
        .value_counts()
    )

    plt.figure(figsize=(8, 8))
    file_types.plot.pie(autopct="%1.1f%%", colors=plt.cm.Paired.colors)
    plt.title("File Type Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()


def visualize_directory_usage(directory):
    """Generate visualizations for the given directory."""
    if not Path(directory).is_dir():
        print("Invalid directory!")
        exit(1)  # Exit with error

    print(f"Analyzing directory: {directory}")
    df = collect_data(directory)

    if df.empty:
        print("No data found in the directory.")
        exit(1)  # Exit with error

    # Plot disk usage
    print("Generating disk usage visualization...")
    plot_usage(df, title="Disk Usage for All Files and Directories")

    # Plot file type distribution
    print("Generating file type distribution visualization...")
    plot_file_type_distribution(df)


if __name__ == "__main__":
    # Ensure a directory argument is provided
    if len(sys.argv) < 2:
        print("Error: Directory path is required as an argument!")
        print("Usage: python3 disk_usage_visualizer_tool.py <directory>")
        exit(1)

    directory = sys.argv[1]
    visualize_directory_usage(directory)

