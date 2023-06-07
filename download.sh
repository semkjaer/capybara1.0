#!/bin/sh

sudo apt-get install unzip

# URL of the zip file
URL="https://www.cbs.nl/-/media/cbs/dossiers/nederland-regionaal/wijk-en-buurtstatistieken/wijkbuurtkaart_2022_v1.zip"

# Directory to check
DIR="WijkBuurtkaart_2022_v1/"
ZIP="wijkbuurtkaart_2022_v1.zip"

if [ "$ZIP" ]; then
    rm -f $ZIP
    echo "File $ZIP deleted."
else
    echo "File $ZIP does not exist."
fi

# Check if the directory exists
if [ ! -d "$DIR" ]; then
    # Directory does not exist, proceed with download and unzip

    # Download the file
    curl -O $URL

    # Get the name of the file from the URL
    FILENAME=$(basename $URL)

    # Unzip the file
    unzip $FILENAME

    # Delete the zip file
    rm $FILENAME
else
    echo "Directory $DIR exists, skipping download and unzip"
fi
