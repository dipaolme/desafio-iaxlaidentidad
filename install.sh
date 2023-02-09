sudo apt-get -y install tesseract-ocr;
wget https://github.com/tesseract-ocr/tessdata_best/raw/main/spa.traineddata;
sudo mv spa.traineddata /usr/share/tesseract-ocr/4.00/tessdata/;
sudo apt-get -y install swig4.0;

mkdir input_data;
mkdir out_data;
sudo chmod 666 input_data;
sudo chmod 666 out_data;

cd src;
git clone https://github.com/bakwc/JamSpell.git;
sudo chmod 666 JamSpell;

cd JamSpell;
sudo chmod 777 *;
