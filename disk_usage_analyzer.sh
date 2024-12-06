#!/bin/bash

# Function to visualize disk usage using Python script
visualize_disk_usage() {
    echo "Generating visualizations for directory: $1"
    if python3 disk_usage_visualizer_tool.py "$1"; then
        echo "Visualizations generated successfully!"
    else
        echo "Error: Unable to generate visualizations. Check the directory path or Python script."
    fi
}

# Main menu
while true; do
    echo "===== Disk Usage Analyzer ====="
    echo "1. Analyze specific directory and save report"
    echo "2. Analyze system-wide disk usage and save report"
    echo "3. Display top 10 large files in a directory and save report"
    echo "4. Analyze every 60 seconds"
    echo "5. Exit"
    echo "6. Visualize disk usage with Python"
    echo "=============================="
    read -p "Enter your choice: " choice

    case $choice in
        1)
            read -p "Enter directory path: " dir
            if [ -d "$dir" ]; then
                du -sh "$dir"
            else
                echo "Directory not found!"
            fi
            ;;
        2)
            df -h
            ;;
        3)
            read -p "Enter directory path: " dir
            if [ -d "$dir" ]; then
                find "$dir" -type f -exec du -h {} + | sort -rh | head -n 10
            else
                echo "Directory not found!"
            fi
            ;;
        4)
            while true; do
                df -h
                sleep 60
            done
            ;;
        5)
            echo "Exiting..."
            exit 0
            ;;
        6)
            read -p "Enter directory path: " dir
            if [ -d "$dir" ]; then
                visualize_disk_usage "$dir"
            else
                echo "Directory not found!"
            fi
            ;;
        *)
            echo "Invalid choice, please try again."
            ;;
    esac
done

