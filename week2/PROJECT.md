# Ecommerce Data Training and Testing


# Level 1: Classifying Product Names to Categories
Use the Best Buy ecommerce dataset as source of labeled data to train a model and train a classifier that maps product names to categories.

Step 1: Extract a file in a format that fastText can read

Run to extract labeled product names from a subset (removed music and movies) of the Best Buy product XML files so that fastText can consume the category id as a label followed by the product name as the rest of the line
```bash
python createContentTrainingData.py
```

The XML contains content that looks like this:
```html
<product>   
       <sku>4041128</sku>   
       <productId>1218452838259</productId>   
       <name>LG - Nitro HD 4G Mobile Phone - Black (AT&amp;T)</name>
       …
       <categoryPath>      
            <category>         
                 <id>cat00000</id>         
                 <name>Best Buy</name>         
            </category>      
            <category>         
                 <id>abcat0800000</id>         
                 <name>Mobile Phones</name>         
            </category>      
            <category>         
                 <id>pcmcat209400050001</id>         
                 <name>All Mobile Phones with Plans</name>         
            </category>      
       </categoryPath>
       …
	</product>
```

Running the file extracts this entry for the product:
```bash
__label__pcmcat209400050001 LG - Nitro HD 4G Mobile Phone - Black (AT&T)
```

To view data that was just written, vim into the file: 
```bash
vim /workspace/datasets/fasttext/output.fasttext
```
The first several lines look like this:
```bash
__label__abcat0107029 Recoton - 1/8" Mini Stereo 3.5mm Y Adapter
__label__abcat0202007 Panasonic - Technics Quartz Synthesizer Direct-Drive Turntable
__label__abcat0908001 Holmes - Replacement Filter for Select Holmes Ultrasonic Humidifiers
__label__abcat0107031 Monster Cable - 10' Pair of 10-Gauge Speaker Wire
__label__pcmcat223000050008 Pioneer - 4" 3-Way Surface-Mount Speakers with IMPP Composite Cones (Pair)
__label__abcat0802002 AT&T - Trimline Telephone - White
__label__abcat0916011 Hoover - Type S Filtration Vacuum Bags (3-Pack)
__label__abcat0811012 AT&T - 3.6V NiCad Battery for 900MHz Phones
__label__pcmcat211400050011 Directed Electronics - Viper Audio Glass Break Sensor
__label__abcat0410026 Sony - 8mm Standard Metal MP Videotapes (3-Pack)
__label__abcat0916012 Dirt Devil - Vacuum Belt
__label__abcat0307010 Best Buy - Mitsubishi In-Dash Installation Kit
__label__abcat0307010 Best Buy - Subaru w/Computer
__label__pcmcat165900050033 Metra - Radio Installation Dash Kit for Most 1989-2000 Ford, Lincoln & Mercury Vehicles - Black
...
```

Run to generate training data and then use it to train a fastText model:
Run (in the week2 directory):
```bash
python createContentTrainingData.py --output /workspace/datasets/fasttext/labeled_products.txt
```

See the outputs in real time:
Run
```bash
tail -f /workspace/datasets/fasttext/labeled_products.txt
```

Outputs look like this (there should be about 115503 entries in labeled data file):
```bash
...
__label__pcmcat212600050011 HP Pavilion p2-1124 Desktop & 20" LCD-LED Monitor Package
__label__pcmcat212600050011 HP Pavilion p2-1124 Desktop & 23" LED IPS Monitor Package
__label__pcmcat212600050011 Dell Inspiron I660S-2000BK Desktop & 20" LED Monitor Package
__label__pcmcat212600050011 Dell Inspiron I660S-2000BK Desktop & 24" LED Monitor Package
__label__pcmcat212600050011 Gateway DX4870-UB20P Desktop & 21.5" LCD Monitor Package
__label__pcmcat212600050011 Asus Essentio CM6730-06 Desktop & 20" LED Monitor Package
__label__pcmcat212600050011 Asus Essentio CM6730-06 Desktop & 24" LED Monitor Package
__label__abcat0300000 Two Alpine Single Voice Coil Subwoofer Pairs
__label__abcat0300000 Two Pioneer 12" Dual Voice Coil Subwoofers Package
__label__abcat0910002 LG White High-Efficiency Steam Washer and Steam Electric Dryer Package
__label__abcat0910002 LG White High-Efficiency Steam Washer and Steam Gas Dryer Package
__label__abcat0910002 LG Red High-Efficiency Steam Washer and Steam Electric Dryer Package
__label__abcat0910002 LG Red High-Efficiency Steam Washer and Steam Gas Dryer Package
__label__abcat0101001 LG 47" Class LED 1080p Smart 3D HDTV, Blu-ray Player & 3D Glasses Package
__label__abcat0101001 LG 55" Class LED 1080p Smart 3D HDTV, Blu-ray Player & 3D Glasses Package
```

To avoid bias in the ordering when labeled data split into training and test rdrata, use command-line utility `shuf` to shuffle the data. Random shuffling is deterministic (everyone gets the same results):
```bash
shuf /workspace/datasets/fasttext/labeled_products.txt --random-source=<(seq 99999) > /workspace/datasets/fasttext/shuffled_labeled_products.txt
```

Copy the first 10000 lines of `shuffled_labeled_products.txt` to `training_data.txt` using the command-line utility head. Then use the command-line utility tail to copy last 10000 lines to test_data.txt. Since the data is shuffled these are both random samples.

Run to uses head to take the first 10,000 lines from shuffled_labeled_products.txt and redirect the output to training_data.txt using the > operator, which will create or overwrite training_data.txt:
```bash
head -n 10000 /workspace/datasets/fasttext/shuffled_labeled_products.txt > /workspace/datasets/fasttext/training_data.txt
```

Run to copy the last 10,000 lines from shuffled_labeled_products.txt and then writes them to test_data.txt:
```bash
tail -n 10000 /workspace/datasets/fasttext/shuffled_labeled_products.txt > /workspace/datasets/fasttext/test_data.txt
```


Each of these files has data in them now ✅
```bash
vim /workspace/datasets/fasttext/training_data.txt
vim /workspace/datasets/fasttext/shuffled_labeled_products.txt
vim /workspace/datasets/fasttext/test_data.txt 
```

Confirm file sizes with command-line utility `wc`:

Run:
```bash
wc /workspace/datasets/fasttext/training_data.txt
```
Output is:
```bash
10000 102727 813914 /workspace/datasets/fasttext/training_data.txt
```

Run:
```bash
wc /workspace/datasets/fasttext/shuffled_labeled_products.txt
```
Output is:
```bash
115503 1180198 9329538 /workspace/datasets/fasttext/shuffled_labeled_products.txt
```

Run:
```bash
wc /workspace/datasets/fasttext/test_data.txt
```
Output is:
```bash
10000 106578 840840 /workspace/datasets/fasttext/test_data.txt
```

Train the model using `fasttext supervised` with default settings and call the model `product_classifier`
Run:
```bash
~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/training_data.txt -output /workspace/datasets/fasttext/product_classifier

```

Output:
```bash
Read 0M words
Number of words:  10754
Number of labels: 1341
Progress: 100.0% words/sec/thread:     570 lr:  0.000000 avg.loss: 13.675712 ETA:   0h 0m 0s
```

Test the model:
```bash
~/fastText-0.9.2/fasttext test /workspace/datasets/fasttext/product_classifier.bin /workspace/datasets/fasttext/test_data.txt
```

Output:
```
N       9669
P@1     0.17
R@1     0.17
```

Start fastText in predict mode:
Run:
```bash
~/fastText-0.9.2/fasttext predict /workspace/datasets/fasttext/product_classifier.bin -

Sharp - 46" 1080p Flat-Panel LCD HDTV
Nikon D3000 10.2MP Digital SLR with Extra 55-200mm Lens, Tripod and Bag
Sony - VAIO Laptop with Intel® Centrino® Processor Technology - Sangria Red
```
Output:
```
Sharp - 46" 1080p Flat-Panel LCD HDTV
__label__abcat0101001

Nikon D3000 10.2MP Digital SLR with Extra 55-200mm Lens, Tripod and Bag
__label__pcmcat180400050006

Sony - VAIO Laptop with Intel® Centrino® Processor Technology - Sangria Red
__label__pcmcat247400050000
```

Trying to optimize model ✅
```bash
~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/training_data.txt -output /workspace/datasets/fasttext/product_classifier -epoch 25 -lr 1.0 -wordNgrams 2
~/fastText-0.9.2/fasttext test /workspace/datasets/fasttext/product_classifier.bin /workspace/datasets/fasttext/test_data.txt
```
Output (took ~5 min):
```
Read 0M words
Number of words:  10754
Number of labels: 1341
Progress: 100.0% words/sec/thread:     583 lr:  0.000000 avg.loss:  1.251436 ETA:   0h 0m 0s
N       9669
P@1     0.655
R@1     0.655
```
^ Increased the precision dramatically up to 66%


Normalize the labeled data:
- Remove all non-alphanumeric characters other than underscore.
- Convert all letters to lowercase.
- Trim excess space characters so that tokens are separated by a single space.
```bash
cat /workspace/datasets/fasttext/shuffled_labeled_products.txt |sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]_]/ /g" | tr -s ' ' > /workspace/datasets/fasttext/normalized_labeled_products.txt
```

### Check the data was normalized ✅

ORIGINAL: Check original file: 
```bash
head /workspace/datasets/fasttext/shuffled_labeled_products.txt
```
Output:
```bash
__label__abcat0401002 Canon - PowerShot 10.0-Megapixel Digital Camera - Black
__label__abcat0701001 Microsoft - Xbox 360 4GB Special Edition Kinect Family Bundle
__label__abcat0905001 KitchenAid - Architect P Series 23-7/8" Tall Tub Built-in Dishwasher - Black
__label__abcat0106008 Bush - Midnight Mist Audio Tower
__label__pcmcat209000050008 Viewsonic - ViewPad V7E_1WNA1US7_01 7" 4 GB Tablet Computer - Wi-Fi - Samsung S5PV210 1 GHz - White
__label__abcat0912019 Maxi-Matic - Popcorn Popper - Red
__label__pcmcat151600050024 Marshall - MS4 Guitar Mini Stack
__label__pcmcat152200050013 Rico - Royal #3.0 Bb Clarinet Reeds (3-Pack) - Blue
__label__pcmcat152100050038 Sennheiser - Instrument Microphone
__label__pcmcat147400050010 Science Papa - Nintendo Wii
```

NEW: Check the normalized file ✅
```bash
head /workspace/datasets/fasttext/normalized_labeled_products.txt
```
Output:
```bash
__label__abcat0401002 canon powershot 10 0 megapixel digital camera black
__label__abcat0701001 microsoft xbox 360 4gb special edition kinect family bundle
__label__abcat0905001 kitchenaid architect p series 23 7 8 tall tub built in dishwasher black
__label__abcat0106008 bush midnight mist audio tower
__label__pcmcat209000050008 viewsonic viewpad v7e_1wna1us7_01 7 4 gb tablet computer wi fi samsung s5pv210 1 ghz white
__label__abcat0912019 maxi matic popcorn popper red
__label__pcmcat151600050024 marshall ms4 guitar mini stack
__label__pcmcat152200050013 rico royal 3 0 bb clarinet reeds 3 pack blue
__label__pcmcat152100050038 sennheiser instrument microphone
__label__pcmcat147400050010 science papa nintendo wii
```

### To extract the training and test data from the normalized file and then train and test your FastText model with new data

Extract Training Data:
Run:
```bash
head -n 10000 /workspace/datasets/fasttext/normalized_labeled_products.txt > /workspace/datasets/fasttext/normalized_training_data.txt
```

Extract Test Data:
Run:
```bash
tail -n 10000 /workspace/datasets/fasttext/normalized_labeled_products.txt > /workspace/datasets/fasttext/normalized_test_data.txt
```

Train the Model:
Run:
```bash
~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/normalized_training_data.txt -output /workspace/datasets/fasttext/normalized_product_classifier -epoch 25 -lr 1.0 -wordNgrams 2
```
Output:
```bash
Read 0M words
Number of words:  8449
Number of labels: 1341
Progress: 100.0% words/sec/thread:     504 lr:  0.000000 avg.loss:  1.171260 ETA:   0h 0m 0s
```

Test the Model:
Run:
```bash
~/fastText-0.9.2/fasttext test /workspace/datasets/fasttext/normalized_product_classifier.bin /workspace/datasets/fasttext/normalized_test_data.txt
```
Output:
```bash
N       9669
P@1     0.653
R@1     0.653
```
^ This decreased the precision and recall by .002
- The data is pretty normalized already, so normalization doesn't provide much benefit.



```bash
~/fastText-0.9.2/fasttext nn /workspace/datasets/fasttext/title_model_100.bin
```