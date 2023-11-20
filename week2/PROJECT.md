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

## Update `createContentTrainingData.py` to only output entries whose label is associated with at least 500 products for `pruned_labeled_products.txt`

Created: `createContentTrainingData-PRUNED-AtLeast500.py`

Run:
```bash
python createContentTrainingData-PRUNED-AtLeast500.py --min_products 500 --output /workspace/datasets/fasttext/pruned_labeled_products.txt
```

Output:
```bash
100%|██████████████████████████████████████████████████████████████████████| 256/256 [02:26<00:00,  1.75it/s]
Writing results to /workspace/datasets/fasttext/pruned_labeled_products.txt
```

To check if there are 28000 products:
Run:
```bash
wc -l /workspace/datasets/fasttext/pruned_labeled_products.txt
```
Output (validates there are ~28000 products ✅):
```bash
28921 /workspace/datasets/fasttext/pruned_labeled_products.txt
```

## Shuffle and split this data to extract 10000 training examples and 10000 test examples, normalize, and train a model with the learning rate of 1.0 and 25 epochs that have done well so far

### Shuffle data:
Run:
```bash
shuf /workspace/datasets/fasttext/pruned_labeled_products.txt > /workspace/datasets/fasttext/shuffled_pruned_labeled_products.txt
```

### Split the Data into Training and Test Sets:

Extract Training Data:
Run:
```bash
head -n 10000 /workspace/datasets/fasttext/shuffled_pruned_labeled_products.txt > /workspace/datasets/fasttext/training_data.txt
```

Extract Test Data:
Run:
```bash
tail -n +10001 /workspace/datasets/fasttext/shuffled_pruned_labeled_products.txt | head -n 10000 > /workspace/datasets/fasttext/test_data.txt
```

### Normalize the Data
Run (convert text to lowercase, remove special characters, etc): 
```bash
sed -e "s/\([.\!?,'/()]\)/ \1 /g" -e "s/[^[:alnum:]_]/ /g" /workspace/datasets/fasttext/training_data.txt | tr "[:upper:]" "[:lower:]" | tr -s ' ' > /workspace/datasets/fasttext/normalized_training_data.txt

sed -e "s/\([.\!?,'/()]\)/ \1 /g" -e "s/[^[:alnum:]_]/ /g" /workspace/datasets/fasttext/test_data.txt | tr "[:upper:]" "[:lower:]" | tr -s ' ' > /workspace/datasets/fasttext/normalized_test_data.txt
```

### Train and Test the FastText Model

Run:
```bash
~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/normalized_training_data.txt -output /workspace/datasets/fasttext/product_classifier -epoch 25 -lr 1.0 -wordNgrams 2
```

### Test
Run: 
```bash
~/fastText-0.9.2/fasttext test /workspace/datasets/fasttext/product_classifier.bin /workspace/datasets/fasttext/normalized_test_data.txt
```
Output:
```bash
N       10000
P@1     0.971
R@1     0.971
```
^ Precision is now 97% which is a HUGE improvement! Reducing the number of labels substantially improves the precision of the classifier, and allows it to run so much faster.

There is a more robust approach to leverage hierarchical nature of taxonomy and roll up infrquently used labels to their parent or other ancestor categories which could be used instead.





# Level 2: Derive Synonyms from Content
Build out a synonym set from raw content using machine learning.

## Get content to train a word representation model in fastText
Instead of outputting category IDs (like before), output the category names, which have more semantic signal.

Run:
```bash
python createContentTrainingData.py --output /workspace/datasets/fasttext/products.txt --label name
```

## Normalize text
Run:
```bash
cat /workspace/datasets/fasttext/products.txt |  cut -c 10- | sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]]/ /g" | tr -s ' ' > /workspace/datasets/fasttext/normalized_products.txt
```

## Feed the extracted output to fasttext skipgram for unsupervised training:

Run:
```bash
~/fastText-0.9.2/fasttext skipgram -input /workspace/datasets/fasttext/normalized_products.txt -output /workspace/datasets/fasttext/title_model
```

Output:
```bash
Query word? inkjet
deskjet 0.875077
officejet 0.867659
mvm 0.855943
laserjet 0.845024
mfc 0.844395
c5280 0.837644
jetprinter 0.835521
b1h 0.834211
564xl 0.82773
1074 0.823483

Query word? netbook
netbooks 0.942556
jetbook 0.910945
nextbook 0.824811
atom 0.804837
eee 0.748957
1005hab 0.743512
ibook 0.705364
n455 0.701041
n270 0.70026
slipskin 0.695806

Query word? backpack
backpacks 0.949453
fastpack 0.715392
ogio 0.697463
aw 0.688428
beltpack 0.686693
toploader 0.68662
shoulder 0.654632
briefcase 0.652874
bags 0.648567
trackpad 0.635948

Query word? briefcase
brief 0.895708
slimcase 0.780699
slipcase 0.757732
1041 0.742206
a7 0.733866
178 0.73348
172 0.732157
fūl 0.731195
1625 0.727156
177 0.726667

Query word? ipad
ipadÂ 0.919162
apple 0.806937
sleeves 0.792562
appleÂ 0.755348
fitfolio 0.739808
folio 0.738606
portfolio 0.723104
3rd 0.719737
sleeve 0.718055
easel 0.715427

Query word? iPad
ad 0.735105
bad 0.677663
mad 0.664957
cad 0.633713
dad 0.615607
dmpad 0.614916
catz 0.588597
gamepad 0.573838
nicad 0.565757
splitfish 0.562882

Query word? iPhone
hone 0.908387
phone 0.812849
ozone 0.790624
gophone 0.788092
palmone 0.726235
speakerphone 0.716139
tecnozone 0.699631
saxophone 0.693102
iphone 0.691046
clone 0.683176

Query word? iphone
4s 0.867548
apple 0.786042
3gs 0.750346
ipadÂ 0.732221
appleÂ 0.72477
ipod 0.712051
ipad 0.706191
fabshell 0.685112
ifrogz 0.671396
ipodÂ 0.667536
```

^ Pretty good synonyms, but also some strange tokens. 

## Repeat process training model on --minCount 100 to remove less frequently seen tokens

Run:
```bash
~/fastText-0.9.2/fasttext skipgram -input /workspace/datasets/fasttext/normalized_products.txt -output /workspace/datasets/fasttext/title_model_100 -minCount 100
```
Output:
```bash
Read 1M words
Number of words:  1556
Number of labels: 0
Progress: 100.0% words/sec/thread:    2957 lr:  0.000000 avg.loss:  1.306737 ETA:   0h 0m 0s
```


## Test
```bash
~/fastText-0.9.2/fasttext nn /workspace/datasets/fasttext/title_model_100.bin
```

Output:
```bash
Query word? inkjet
printer 0.802082
printers 0.80124
laserjet 0.751793
copier 0.710016
lexmark 0.697843
photosmart 0.684404
packard 0.679742
hewlett 0.674205
cartridge 0.660388
ink 0.65289

Query word? netbook
netbooks 0.922093
atom 0.77747
eee 0.708425
slip 0.62749
laptop 0.612029
aspire 0.507833
250gb 0.505721
intel 0.495615
sleeve 0.49419
briefcase 0.487922

Query word? backpack
shoulder 0.654632
bag 0.622703
messenger 0.600583
briefcase 0.593899
lowepro 0.571451
bags 0.569988
d90 0.560594
tote 0.538485
slr 0.528216
logo 0.520133

Query word? backpacks
backpack 0.935928
briefcase 0.601099
shoulder 0.60054
bag 0.600153
messenger 0.578737
d90 0.57535
bags 0.551714
tote 0.535134
case 0.534566
deals 0.525948

Query word? briefcase
slip 0.631154
samsonite 0.626147
team 0.615615
rolling 0.603543
sleeve 0.602192
laptop 0.597605
backpack 0.593899
tote 0.579316
messenger 0.577758
mouse 0.564758

Query word? ipad
folio 0.699219
sleeves 0.698969
covers 0.69199
apple 0.691502
3rd 0.683646
slip 0.624441
generation 0.612584
iphone 0.598492
kindle 0.591739
rico 0.567961

Query word? iPad
mad 0.674769
catz 0.660935
dead 0.59987
pad 0.556165
controller 0.539966
road 0.534473
head 0.519135
controllers 0.501595
ps3 0.488474
nfl 0.484295

Query word? iPhone
phone 0.799908
speakerphone 0.782337
iphone 0.690844
telephones 0.653724
handset 0.648103
handsets 0.646852
answering 0.622915
phones 0.622198
caller 0.621551
id 0.616621

Query word? iphone
4s 0.833591
apple 0.727374
3gs 0.726812
ipod 0.680449
ipad 0.598492
4th 0.584466
fitted 0.578811
phone 0.56179
silicone 0.560175
shell 0.550544
```

Specific tests of tokens for qualitative evaluation:

```bash
Query word? headphones
ear 0.896908
earbud 0.859221
bud 0.71857
noise 0.702953
skullcandy 0.657751
over 0.645013
sennheiser 0.640076
gumy 0.613696
earbuds 0.609976
microphones 0.608596

Query word? laptop
laptops 0.81118
notebook 0.746067
notebooks 0.694686
macbook 0.635716
netbook 0.612029
briefcase 0.597605
netbooks 0.555165
slip 0.535363
compaq 0.524121
dell 0.512924

Query word? freezer
freezers 0.922984
refrigerators 0.781482
frost 0.77881
refrigerator 0.770578
bottom 0.733069
counter 0.695368
monochromatic 0.687927
side 0.677465
cu 0.652178
ft 0.649999

Query word? nintendo
ds 0.884006
wii 0.855321
3ds 0.77028
dsi 0.748712
psp 0.694647
gamecube 0.690804
boy 0.665843
playstation 0.655219
advance 0.650607
mario 0.642152

Query word? whirlpool
maytag 0.858483
biscuit 0.804458
frigidaire 0.787001
bisque 0.735224
ge 0.714769
profile 0.675264
gallery 0.67512
bosch 0.67351
architect 0.672835
electrolux 0.672497

Query word? kodak
easyshare 0.83875
share 0.674532
coolpix 0.61845
canon 0.610548
photosmart 0.609062
fujifilm 0.581312
powershot 0.575278
finepix 0.556158
everio 0.552032
packard 0.547953

Query word? ps2
playstation 0.800707
psp 0.737161
xbox 0.71183
nba 0.705987
ps3 0.696338
360 0.691058
gamecube 0.681422
greatest 0.676183
vs 0.663505
game 0.660187

Query word? razr
razer 0.817047
geforce 0.551756
gaming 0.526776
force 0.523708
rate 0.520833
radeon 0.500068
ray 0.489327
mice 0.48741
corded 0.481481
caller 0.479737

Query word? stratocaster
roaster 0.742087
toaster 0.707938
slow 0.705135
toasters 0.68337
pizza 0.671257
crock 0.658007
cooker 0.648697
pots 0.627606
cookers 0.618411
slice 0.614333

Query word? holiday
indianapolis 0.664373
stuffed 0.662589
birthday 0.659069
tailgate 0.63841
carolina 0.634051
virginia 0.633548
animals 0.622305
colts 0.6213
fabrique 0.618241
miami 0.614847

Query word? plasma
600hz 0.834048
televisions 0.747018
240hz 0.700681
tvs 0.698267
panel 0.697475
hdtv 0.694937
flat 0.694048
120hz 0.658449
1080p 0.653599
46 0.648272

Query word? leather
recliner 0.716406
berkline 0.676113
seating 0.661851
curved 0.652798
theaterseatstore 0.607079
clips 0.593057
seat 0.566764
straight 0.56002
folio 0.534812
executive 0.532816
```

## Iterate to experiment if the synonyms are getting better or worse

### Increase epochs to 25

Parameters to pass into the `skipgram` training:
- `-input /workspace/datasets/fasttext/normalized_products.txt`: specifies the input file for training.
- `-output /workspace/datasets/fasttext/title_model`: specifies the base name for the output files.
- `-minCount 100`: sets the minimum number of occurrences for words to be included in the training.
- `-epoch 25`: increases the number of training epochs to 25.

Run:
```bash
~/fastText-0.9.2/fasttext skipgram -input /workspace/datasets/fasttext/normalized_products.txt -output /workspace/datasets/fasttext/title_model -minCount 100 -epoch 25
```

### Use the same nn (nearest neighbor) command to evaluate the quality of the synonyms as before
Run:
```bash
~/fastText-0.9.2/fasttext nn /workspace/datasets/fasttext/title_model.bin
```

My test:

Output:
```bash
Query word? inkjet
printers 0.783415
printer 0.751314
laserjet 0.665555
epson 0.635019
copier 0.625335
hp 0.618608
hewlett 0.604726
packard 0.602729
multifunction 0.597315
ink 0.593882

Query word? netbook
netbooks 0.888386
atom 0.763981
eee 0.709744
laptop 0.619467
slip 0.618083
notebook 0.513293
mouse 0.487527
briefcase 0.479063
sleeve 0.46592
mini 0.461379

Query word? backpack
messenger 0.581825
bag 0.565067
shoulder 0.560365
briefcase 0.539403
slr 0.533204
bags 0.527808
case 0.526327
sleeve 0.500874
slip 0.468269
lowepro 0.443399

Query word? backpacks
backpack 0.922301
case 0.556765
messenger 0.54768
slr 0.533012
bag 0.528992
bags 0.522583
briefcase 0.51113
shoulder 0.505254
packs 0.495113
battery 0.479309

Query word? briefcase
rolling 0.543154
backpack 0.539402
slip 0.534601
notebook 0.523338
laptop 0.519888
sleeve 0.519232
samsonite 0.482884
netbook 0.479063
messenger 0.46642
scoreboard 0.464073

Query word? ipad
apple 0.696349
sleeves 0.681702
covers 0.670105
iphone 0.631006
3rd 0.61705
folio 0.57789
generation 0.558684
tablet 0.543282
sleeve 0.538093
ipod 0.524788

Query word? iPad
mad 0.643589
catz 0.614093
pad 0.561103
dead 0.550131
ps3 0.5234
playstation 0.490512
road 0.490339
360 0.484501
xbox 0.479247
hero 0.470234

Query word? iPhone
speakerphone 0.762707
phone 0.693843
telephones 0.66715
caller 0.617781
handset 0.608442
corded 0.595266
hands 0.579289
id 0.575938
handsets 0.573916
answering 0.564649

Query word? iphone
4s 0.873662
apple 0.765594
3gs 0.68914
ipod 0.683545
ipad 0.631006
3g 0.573716
fitted 0.541358
blackberry 0.514837
4th 0.511251
phones 0.503199
```

Testing set:

Output:
```bash
Query word? headphones
earbud 0.899375
ear 0.899365
bud 0.701178
noise 0.67227
over 0.667513
skullcandy 0.590442
headset 0.573595
sennheiser 0.564302
gumy 0.543652
beats 0.541636

Query word? laptop
laptops 0.769928
notebook 0.74719
notebooks 0.621178
netbook 0.619467
netbooks 0.552174
macbook 0.525278
briefcase 0.519888
mouse 0.513865
dell 0.513161
inspiron 0.501458

Query word? freezer
freezers 0.857819
refrigerator 0.763114
refrigerators 0.742874
frost 0.710749
bottom 0.654554
cu 0.650716
ft 0.643925
side 0.643202
counter 0.584627
french 0.569223

Query word? nintendo
ds 0.941061
wii 0.882083
3ds 0.76787
psp 0.695532
advance 0.686687
dsi 0.676859
playstation 0.652655
ps2 0.641775
boy 0.635389
gamecube 0.629086

Query word? whirlpool
maytag 0.824362
frigidaire 0.786767
biscuit 0.743923
ge 0.732208
electrolux 0.658595
bisque 0.652098
kitchenaid 0.635125
bosch 0.625267
profile 0.613126
cu 0.604639

Query word? kodak
easyshare 0.804574
canon 0.597042
photosmart 0.562868
coolpix 0.528146
powershot 0.526456
finepix 0.525841
share 0.500011
elph 0.499018
fujifilm 0.48726
hewlett 0.482462

Query word? ps2
playstation 0.793399
xbox 0.706151
psp 0.699599
ps3 0.649311
wii 0.646517
360 0.645434
game 0.643039
nintendo 0.641775
gamecube 0.641592
greatest 0.621923

Query word? razr
razer 0.85611
gaming 0.535321
geforce 0.477865
essentio 0.444877
dragon 0.444504
oakland 0.442661
radeon 0.437779
graphics 0.431034
logitech 0.427934
cleveland 0.423945

Query word? stratocaster
roaster 0.662965
toaster 0.644918
crock 0.62008
pots 0.618027
slow 0.617731
cooker 0.592691
strategy 0.591057
toasters 0.588072
master 0.565575
pizza 0.560574

Query word? holiday
birthday 0.612923
miami 0.595988
day 0.583809
solid 0.546843
florida 0.538433
carolina 0.528972
happy 0.527125
virginia 0.519103
billiard 0.518931
iowa 0.518484

Query word? plasma
600hz 0.704821
tvs 0.649182
televisions 0.617054
flat 0.612904
panel 0.586286
65 0.56411
52 0.539704
3d 0.532713
32 0.527627
hdtv 0.518113

Query word? leather
recliner 0.632685
seating 0.556378
berkline 0.540002
executive 0.522281
curved 0.513693
theaterseatstore 0.493293
brown 0.484722
case 0.477769
cases 0.464642
milliken 0.461993
```
^ For running 0h15m29s (~15 mins), these synonyms are more optimized for the queries.
- Before when `~/fastText-0.9.2/fasttext test /workspace/datasets/fasttext/product_classifier.bin /workspace/datasets/fasttext/normalized_test_data.txt` was run, this was used to used for evaluating a supervised classification model in FastText.
     - The test command in FastText is specifically designed to evaluate supervised models (like with the trained version of the model with the supervised command). 
     - It calculates metrics such as precision and recall based on how well the model classifies the test data (in your case, the contents of normalized_test_data.txt).
- However, here, the `nn` method is used with unsupervised models (like with the skipgram or cbow commands in FastText), where the goal is to learn word embeddings. 
     - The nn method finds the nearest neighbors (most similar words) in the embedding space for a given query word. 
     - The evaluation of such models is more qualitative and typically involves manually checking the relevance and quality of the nearest neighbors for various query words.



# Level 3: Integrating Synonyms with Search
Use synonyms in a search application.

## Data normalization
- Take the most common words that occur in titles. 
- Eliminate stop words and other noise by excluding tokens containing less than 4 characters. 
- Use the following command-line approach to obtain the 1,000 most frequent words:

Run: 
```bash
cat /workspace/datasets/fasttext/normalized_products.txt | tr " " "\n" | grep "...." | sort | uniq -c | sort -nr | head -1000 | grep -oE '[^ ]+$' > /workspace/datasets/fasttext/top_words.txt
```
^ This does the following:
- Replace each space with a newline, so we get one word per line.
- Only keep words containing at least 4 characters.
- Sort the words in alphabetical order.
- Deduplicate the words and keep the counts, yielding a 2-columns file where each line is a count followed by the word.
- Sort the count-word pairs in descending order of count.
- Keep only the top 1,000 entries, i.e., the 1,000 most frequently occurring words.
- Remove the counts so we only output the words.
- Output the result of this process to /workspace/datasets/fasttext/top_words.txt.

## Generate Synonyms for Top Words

Wrote a script called `generateSynonymsForTopWords.py`

It does the following:
- Loads the fastText model you created in the previous step (and probably stored in workspace/datasets/fasttext/title_model.bin).
- Iterates through each line of /workspace/datasets/fasttext/top_words.txt (or wherever you stored the top 1,000 title words).
- Uses the model’s get_nearest_neighbors method to obtain each word’s nearest neighbors. Those are returned as an array of (similarity, word) pairs.
- Outputs, for each word, a comma-separated line that starts with the word and is followed by the neighbors whose similarity exceeds a threshold. Try setting the threshold to be 0.75 or 0.8.

Run:
```bash
python generateSynonymsForTopWords.py
```
OR
Run:
```bash
python generateSynonymsForTopWords.py --model /workspace/datasets/fasttext/title_model.bin --input /workspace/datasets/fasttext/top_words.txt --output /workspace/datasets/fasttext/synonyms.csv --threshold 0.8
```

This should run cleanly. If there is an error like `Warning : `load_model` does not return WordVectorModel or SupervisedModel any more, but a `FastText` object which is very similar.`, see the 🐞 Debugging section below:

### 🐞 Debugging: `Warning : `load_model` does not return WordVectorModel or SupervisedModel any more, but a `FastText` object which is very similar.`

I found that there was a `synonyms.csv` file generated in `/workspace/datasets/fasttext/synonyms.csv`, so I wanted to know how to get rid of this error. 

I found this StackOverflow thread that talked about adding a monkey patch to the script: https://stackoverflow.com/questions/66353366/cant-suppress-fasttext-warning-load-model-does-not-return

```py
import fasttext

fasttext.FastText.eprint = lambda x: None
```

I renamed my file so that I could create a backup:
```bash
mv /workspace/datasets/fasttext/synonyms.csv /workspace/datasets/fasttext/synonyms-backup.csv
```

Then I re-ran the script and didn't see that error again ✅:
```bash
python generateSynonymsForTopWords.py
```

I could validate that the `synonyms.csv` file was generated again:
```bash
gitpod /workspace/datasets/fasttext $ ls
labeled_products.txt               normalized_training_data.txt  shuffled_labeled_products.txt         title_model_100.vec
normalized_labeled_products.txt    output.fasttext               shuffled_pruned_labeled_products.txt  title_model.bin
normalized_product_classifier.bin  product_classifier.bin        synonyms-backup.csv                   title_model.vec
normalized_product_classifier.vec  product_classifier.vec        synonyms.csv                          top_words.txt
normalized_products.txt            products.txt                  test_data.txt                         training_data.txt
normalized_test_data.txt           pruned_labeled_products.txt   title_model_100.bin
```

I checked out the file with vim and saw this:
Run:
```bash
vim synonyms.csv
```
Output:
```bash
black
with
digital
white
case
memory
camera,cameras
electric
games
laptop
windows,mac
card
side,by
nintendo,ds,wii
mobile,phones
apple,ipod
cases
hard
package
wireless
drive
accessories
sony
guitar
battery
ipod,apple
flat,panel,tvs
panel,flat,tvs
range
cameras,camera
built
...
```

## Make the .csv file available to OpenSearch
Since OpenSearch is running in a Docker container, need to copy the synonyms.csv file to the container:

Run:
```bash
docker cp /workspace/datasets/fasttext/synonyms.csv opensearch-node1:/usr/share/opensearch/config/synonyms.csv
```
Output:
```bash
Successfully copied 13.3kB to opensearch-node1:/usr/share/opensearch/config/synonyms.csv
```
^ This puts the .csv data into OpenSearch config directly to allow access via analyzers

## Integrate Synonyms into OpenSearch indexing process and modify the search functionality to utilize these Synonyms 

In the `week2/conf/bbuy_products.json` file, modified to index two fields for "name" -- the (1.) original name fields and (2.) a “name.synonyms” field that adds a “synonym” filter to its analyzer.


### Add Synonym Analyzer to the Settings:
```json
{
  "settings": {
    "analysis": {
      "analyzer": {
        "synonym_analyzer": {
          "tokenizer": "standard",
          "filter": ["lowercase", "stemmer", "synonym_filter"]
        },
        "smarter_hyphens": {
          "tokenizer": "smarter_hyphens_tokenizer",
          "filter": [
            "smarter_hyphens_filter",
            "lowercase"
          ]
        }
      },
      "tokenizer": {
        "smarter_hyphens_tokenizer": {
          "type": "char_group",
          "tokenize_on_chars": [
            "whitespace",
            "\n"
          ]
        }
      },
      "filter": {
        "synonym_filter": {
          "type": "synonym",
          "synonyms_path": "synonyms.csv"
        },
        "smarter_hyphens_filter": {
          "type": "word_delimiter_graph",
          "catenate_words": true,
          "catenate_all": true
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "@timestamp": {
        "type": "date"
      },
...
```

### Update Mappings to Include name.synonyms
Added the synonyms object:
```json
...
"mappings": {
  "properties": {
    ...
    "name": {
      "type": "text",
      "analyzer": "english",
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 2048
        },
        "hyphens": {
          "type": "text",
          "analyzer": "smarter_hyphens"
        },
        "suggest": {
          "type": "completion"
        },
        "synonyms": {
          "type": "text",
          "analyzer": "synonym_analyzer"
        }
      }
    },
    ...
  }
}
...
```

### Reindex the subset of the data that excludes movies and music:
Run (from the root of the project folder in virtual env `search_with_ml`):
```bash
./index-data.sh -r -p /workspace/search_with_machine_learning_course/week2/conf/bbuy_products.json
```
Output:
```bash
mkdir: cannot create directory ‘/workspace/logs’: File exists
Running python scripts from /workspace/search_with_machine_learning_course/utilities
++ '[' '' '!=' --annotate ']'
++ echo 'Creating index settings and mappings'
Creating index settings and mappings
++ '[' -f /workspace/search_with_machine_learning_course/week2/conf/bbuy_products.json ']'
++ echo ' Product file: /workspace/search_with_machine_learning_course/week2/conf/bbuy_products.json'
 Product file: /workspace/search_with_machine_learning_course/week2/conf/bbuy_products.json
++ curl -k -X PUT -u admin https://localhost:9200/bbuy_products -H 'Content-Type: application/json' -d @/workspace/search_with_machine_learning_course/week2/conf/bbuy_products.json
Enter host password for user 'admin':
{"error":{"root_cause":[{"type":"resource_already_exists_exception","reason":"index [bbuy_products/6aVqkMPEQPOw1arA2Y4W1A] already exists","index":"bbuy_products","index_uuid":"6aVqkMPEQPOw1arA2Y4W1A"}],"type":"resource_already_exists_exception","reason":"index [bbuy_products/6aVqkMPEQPOw1arA2Y4W1A] already exists","index":"bbuy_products","index_uuid":"6aVqkMPEQPOw1arA2Y4W1A"},"status":400}++ '[' 0 -ne 0 ']'
++ '[' -f index_products.py ']'
++ echo 'Indexing product data in /workspace/datasets/product_data/products and writing logs to /workspace/logs/index_products.log'
Indexing product data in /workspace/datasets/product_data/products and writing logs to /workspace/logs/index_products.log
++ '[' 0 -ne 0 ']'
++ nohup python index_products.py --reduced -s /workspace/datasets/product_data/products
++ '[' -f /workspace/search_with_machine_learning_course/conf/bbuy_queries.json ']'
++ echo ''

++ echo ' Query file: /workspace/search_with_machine_learning_course/conf/bbuy_queries.json'
 Query file: /workspace/search_with_machine_learning_course/conf/bbuy_queries.json
++ curl -k -X PUT -u admin https://localhost:9200/bbuy_queries -H 'Content-Type: application/json' -d @/workspace/search_with_machine_learning_course/conf/bbuy_queries.json
nohup: redirecting stderr to stdout
Enter host password for user 'admin':
{"error":{"root_cause":[{"type":"resource_already_exists_exception","reason":"index [bbuy_queries/78xOfma-R_iVDETgMIf8VQ] already exists","index":"bbuy_queries","index_uuid":"78xOfma-R_iVDETgMIf8VQ"}],"type":"resource_already_exists_exception","reason":"index [bbuy_queries/78xOfma-R_iVDETgMIf8VQ] already exists","index":"bbuy_queries","index_uuid":"78xOfma-R_iVDETgMIf8VQ"},"status":400}++ '[' 0 -ne 0 ']'
++ '[' -f index_queries.py ']'
++ echo 'Indexing queries data and writing logs to /workspace/logs/index_queries.log'
Indexing queries data and writing logs to /workspace/logs/index_queries.log
++ '[' 0 -ne 0 ']'
++ nohup python index_queries.py -s /workspace/datasets/train.csv
++ '[' '' == --annotate ']'
nohup: redirecting stderr to stdout
```

### Test the reindexed index:

Run (OpenSearch):
```bash
GET /bbuy_products/_analyze
{
  "analyzer": "synonym_analyzer",
  "text": "Your text here"
}
```
Output:
```json
{
  "tokens": [
    {
      "token": "your",
      "start_offset": 0,
      "end_offset": 4,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "text",
      "start_offset": 5,
      "end_offset": 9,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "here",
      "start_offset": 10,
      "end_offset": 14,
      "type": "<ALPHANUM>",
      "position": 2
    }
  ]
}
```

Run (OpenSearch):
```bash
GET /bbuy_products/_analyze
{
  "analyzer": "synonym_analyzer",
  "text": "televisions"
}
```
Output:
```json
{
  "tokens": [
    {
      "token": "televis",
      "start_offset": 0,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 0
    }
  ]
}
```

Run (OpenSearch):
```bash
GET /bbuy_products/_analyze
{
  "analyzer": "synonym_analyzer",
  "text": "earbuds"
}
```
Output:
```json
{
  "tokens": [
    {
      "token": "earbud",
      "start_offset": 0,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "headphon",
      "start_offset": 0,
      "end_offset": 7,
      "type": "SYNONYM",
      "position": 0
    },
    {
      "token": "ear",
      "start_offset": 0,
      "end_offset": 7,
      "type": "SYNONYM",
      "position": 0
    }
  ]
}
```

### 🐞 Debugging: `failed to find analyzer [synonym_analyzer]`

Run (OpenSearch console):
```bash
GET /bbuy_products/_analyze
{
  "analyzer": "synonym_analyzer",
  "text": "Your text here"
}
```
Output:
```json
{
  "error": {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "failed to find analyzer [synonym_analyzer]"
      }
    ],
    "type": "illegal_argument_exception",
    "reason": "failed to find analyzer [synonym_analyzer]"
  },
  "status": 400
}
```

First I wanted to see all the indices to see if the one for products is there:
```bash
GET _cat/indices?v
```

This printed out many indices, but the one I want is this: 

```json
health status index                                     uuid                   pri rep docs.count docs.deleted store.size pri.store.size
...
yellow open   bbuy_products                             6aVqkMPEQPOw1arA2Y4W1A   1   1    1275077        98195      1.4gb          1.4gb
...
```

Next, I checked about the index settings to see if it included the custom analyzer configuration:

```bash
GET /bbuy_products/_settings?pretty
```

I saw this as the output - which doesn't look like the synonyms one is there:
```json
{
  "bbuy_products": {
    "settings": {
      "index": {
        "number_of_shards": "1",
        "provided_name": "bbuy_products",
        "creation_date": "1699820241967",
        "analysis": {
          "filter": {
            "smarter_hyphens_filter": {
              "catenate_all": "true",
              "type": "word_delimiter_graph",
              "catenate_words": "true"
            }
          },
          "analyzer": {
            "smarter_hyphens": {
              "filter": [
                "smarter_hyphens_filter",
                "lowercase"
              ],
              "tokenizer": "smarter_hyphens_tokenizer"
            }
          },
          "tokenizer": {
            "smarter_hyphens_tokenizer": {
              "type": "char_group",
              "tokenize_on_chars": [
                "whitespace",
                """
"""
              ]
            }
          }
        },
        "number_of_replicas": "1",
        "uuid": "6aVqkMPEQPOw1arA2Y4W1A",
        "version": {
          "created": "136267827"
        }
      }
    }
  }
}
```

I deleted the index with this command:
```bash
curl -k -X DELETE -u admin:admin https://localhost:9200/bbuy_products
```

I reindexed the data:
```bash
./index-data.sh -r -p /workspace/search_with_machine_learning_course/week2/conf/bbuy_products.json
```

Now when I run the GET to see the settings of the index, I will see the synonym analyzer:
Run:
```bash
GET /bbuy_products/_settings?pretty
```
Output:
```json
{
  "bbuy_products": {
    "settings": {
      "index": {
        "number_of_shards": "1",
        "provided_name": "bbuy_products",
        "creation_date": "1700437477379",
        "analysis": {
          "filter": {
            "smarter_hyphens_filter": {
              "catenate_all": "true",
              "type": "word_delimiter_graph",
              "catenate_words": "true"
            },
            "synonym_filter": {
              "type": "synonym",
              "synonyms_path": "synonyms.csv"
            }
          },
          "analyzer": {
            "smarter_hyphens": {
              "filter": [
                "smarter_hyphens_filter",
                "lowercase"
              ],
              "tokenizer": "smarter_hyphens_tokenizer"
            },
            "synonym_analyzer": {
              "filter": [
                "lowercase",
                "stemmer",
                "synonym_filter"
              ],
              "tokenizer": "standard"
            }
          },
          "tokenizer": {
            "smarter_hyphens_tokenizer": {
              "type": "char_group",
              "tokenize_on_chars": [
                "whitespace",
                """
"""
              ]
            }
          }
        },
        "number_of_replicas": "1",
        "uuid": "p6x29G4TSeKsJk-mD4_uog",
        "version": {
          "created": "136267827"
        }
      }
    }
  }
}
```

This confirms that `synonym_analyzer` has been successfully applied to the `bbuy_products` index ✅

## Check that synonyms query works:

### NORMAL: Testing `television`:
Run:
```bash
python utilities/query.py
```

Output:
```bash
Enter your query (type 'Exit' to exit or hit ctrl-c):
laptop
{
  "took": 754,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 7255,
      "relation": "eq"
    },
    "max_score": 601.4438,
    "hits": [
      {
        "_index": "bbuy_products",
        "_id": "4382768",
        "_score": 601.4438,
        "_source": {
          "name": [
            "Rocketfish\u2122 - Slim Universal AC Laptop Power Adapter"
          ],
          "shortDescription": [
            "Compatible with most Acer, Asus, Compaq, Dell, Fujitsu, Gateway, HP, Lenovo, Panasonic, Samsung, Sony and Toshiba laptops; 8 easy-match numbered tips; 6' AC input cord; 90W output; cord management wrap"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3560608",
        "_score": 583.564,
        "_source": {
          "name": [
            "Targus - Laptop Charger"
          ],
          "shortDescription": [
            "Compatible with most laptops; powers your device from an AC outlet; surge protection; interchangeable tip system"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "5373873",
        "_score": 448.75497,
        "_source": {
          "name": [
            "HP - 17.3\" Pavilion Laptop - 4GB Memory - 320GB Hard Drive - Pewter"
          ],
          "shortDescription": [
            "ENERGY STAR QualifiedWindows 7 Home Premium 64-bitTechnical details: AMD A4-Series processor; 17.3\" display; 4GB memory; 320GB hard driveSpecial features: HDMI output"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "5373828",
        "_score": 447.73242,
        "_source": {
          "name": [
            "HP - 14\" Pavilion Laptop - 4GB Memory - 320GB Hard Drive - Pewter"
          ],
          "shortDescription": [
            "ENERGY STAR QualifiedWindows 7 Home Premium 64-bitTechnical details: Intel\u00ae Pentium\u00ae processor; 14\" display; 4GB memory; 320GB hard driveSpecial features: HDMI output"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "8625311",
        "_score": 426.08353,
        "_source": {
          "name": [
            "Toshiba - Satellite TK-53 Laptop - Onyx Blue"
          ],
          "shortDescription": [
            "AMD Athlon\u2122 64 X2 processor TK-53; 2GB DDR2 SDRAM; DL DVD\u00b1RW/CD-RW drive; 15.4\" widescreen; 160GB hard drive; Windows Vista Home Premium"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "8625339",
        "_score": 402.6995,
        "_source": {
          "name": [
            "Gateway - T2080 Laptop"
          ],
          "shortDescription": [
            "Intel\u00ae Pentium\u00ae Dual-Core mobile processor T2080; 2GB DDR2 memory; DL DVD\u00b1RW/CD-RW drive; 15.4\" widescreen; 160GB hard drive; Windows Vista Home Premium"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "5483502",
        "_score": 378.1612,
        "_source": {
          "name": [
            "Samsung - 14\" Laptop - 4GB Memory - 500GB Hard Drive - Titan Silver"
          ],
          "shortDescription": [
            "Windows 7 Home Premium 64-bitTechnical details: 2nd Gen Intel\u00ae Core\u2122 i3 processor; 14\" display; 4GB memory; 500GB hard driveSpecial features: Bluetooth; HDMI output"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "5272499",
        "_score": 375.63943,
        "_source": {
          "name": [
            "Lenovo - 15.6\" Laptop - 4GB Memory - 320GB Hard Drive"
          ],
          "shortDescription": [
            "Windows 7 Home Premium 64-bitTechnical details: AMD E-Series processor; 15.6\" display; 4GB memory; 320GB hard driveSpecial features: Fingerprint reader; HDMI output"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "5608338",
        "_score": 369.7144,
        "_source": {
          "name": [
            "HP - 15.6\" Pavilion Laptop - 6GB Memory - 640GB Hard Drive - Midnight Black"
          ],
          "shortDescription": [
            "ENERGY STAR QualifiedWindows 7 Home Premium 64-bitTechnical details: AMD A10-Series processor; 15.6\" display; 6GB memory; 640GB hard driveSpecial features: Fingerprint reader; backlit keyboard; HDMI output"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "5218639",
        "_score": 367.43842,
        "_source": {
          "name": [
            "Asus - 15.6\" Laptop - 4GB Memory - 320GB Hard Drive - Black"
          ],
          "shortDescription": [
            "ENERGY STAR QualifiedWindows 7 Home Premium 64-bitTechnical details: Intel\u00ae Core\u2122 i3 processor; 15.6\" display; 4GB memory; 320GB hard driveSpecial features: HDMI output"
          ]
        }
      }
    ]
  }
}
```

### useSynonyms: Testing `television`:
Run:
```bash
python utilities/query.py --synonyms
```

Output:
```bash
Enter your query (type 'Exit' to exit): television
{
  "took": 222,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 835,
      "relation": "eq"
    },
    "max_score": 68.670906,
    "hits": [
      {
        "_index": "bbuy_products",
        "_id": "4740317",
        "_score": 68.670906,
        "_source": {
          "name": [
            "Toshiba - 32\" Class - LCD - 720p - 60Hz - HDTV"
          ],
          "shortDescription": []
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "1953594",
        "_score": 63.001427,
        "_source": {
          "name": [
            "KCPI - Digital TV Converter Box"
          ],
          "shortDescription": [
            "Compatible with most analog televisions and recording devices; converts digital TV broadcast signals to analog signals; TV tuner; parental controls"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "7686667",
        "_score": 37.64007,
        "_source": {
          "name": [
            "Canon - PowerShot 5.0MP Digital Camera"
          ],
          "shortDescription": [
            "4x optical/4x digital zoom; DIGIC II processor; 16:9 widescreen mode; direct-print capability"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "6986112",
        "_score": 22.207605,
        "_source": {
          "name": [
            "Magnavox - 15\" HD-Ready LCD TV w/HD Component Video Inputs"
          ],
          "shortDescription": [
            "Picture-in-picture; Smart Picture; Smart Sound; table stand converts for wall mounting"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "1026806",
        "_score": 18.74938,
        "_source": {
          "name": [
            "SOCOM 4: U.S. Navy SEALs - PlayStation 3"
          ],
          "shortDescription": [
            "Rescue a country in chaos to prevent an all-out global war"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "9881868",
        "_score": 13.430846,
        "_source": {
          "name": [
            "Rocketfish\u2122 - Low-Profile Tilting Wall Mount for Most 32\" to 70\" Flat-Panel TVs - Black"
          ],
          "shortDescription": [
            "Compatible with most 32\" - 70\" flat-panel TVs; fingertip tilt; powdercoat finish; locking mechanism"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2635031",
        "_score": 9.634539,
        "_source": {
          "name": [
            "Dynex\u2122 - RF Modulator"
          ],
          "shortDescription": [
            "Compatible with most DVD players, gaming systems, camcorders and other electronic devices; coaxial RF input"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "7686015",
        "_score": 7.31279,
        "_source": {
          "name": [
            "Sony - Progressive-Scan Multiformat DVD-R/-RW/+R/+RW Recorder/VCR Combo"
          ],
          "shortDescription": [
            "Dual-layer DVD+R, DVD+R/+RW/-R/-RW recording and playback; DVD, CD, VCD, SVCD, CD-R/RW playback"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "6654836",
        "_score": 7.0693283,
        "_source": {
          "name": [
            "TiVo\u00ae - Series2\u2122 Digital Video Recorder with 80-Hour Capacity - Silver"
          ],
          "shortDescription": [
            "80-hour capacity; create instant replays of live TV; Season Pass\u2122 recording; dual USB ports"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "9881777",
        "_score": 6.375951,
        "_source": {
          "name": [
            "Rocketfish\u2122 - Low-Profile Tilting Wall Mount for Most 26\" to 40\" Flat-Panel TVs - Black"
          ],
          "shortDescription": [
            "Compatible with most 26\" - 40\" flat-panel TVs; fingertip tilt; powdercoat finish; locking mechanism"
          ]
        }
      }
    ]
  }
}
```

^ synonyms not really for products, but more for words of words... like the below:

# List of Tests:

## `earbuds`

### With Synonyms
```json
Enter your query (type 'Exit' to exit): earbuds 
{
  "took": 221,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1205,
      "relation": "eq"
    },
    "max_score": 843.09705,
    "hits": [
      {
        "_index": "bbuy_products",
        "_id": "9084206",
        "_score": 843.09705,
        "_source": {
          "name": [
            "Apple\u00ae - Earbuds for Select Apple\u00ae iPod\u00ae Models"
          ],
          "shortDescription": [
            "Compatible with 4th-generation iPod nano, 120GB iPod classic and 2nd-generation iPod touch; remote for controlling music and video playback; microphone for recording voice memos"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2197043",
        "_score": 121.19351,
        "_source": {
          "name": [
            "Sony - Earbud Headphones - Black"
          ],
          "shortDescription": [
            "13.5mm drivers; neodymium magnet; 3 sets of silicone ear cushions"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3100277",
        "_score": 109.44192,
        "_source": {
          "name": [
            "Rocketfish\u2122 - Stereo Earbud Headphones"
          ],
          "shortDescription": [
            "10mm drivers; neodymium magnets; lightweight design"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2197089",
        "_score": 109.428734,
        "_source": {
          "name": [
            "Sony - Earbud Headphones - White"
          ],
          "shortDescription": [
            "13.5mm drivers; neodymium magnet; 3 sets of silicone ear cushions"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "8605459",
        "_score": 99.21863,
        "_source": {
          "name": [
            "JVC - Gumy Stereo Earbud Headphones - Olive Black"
          ],
          "shortDescription": [
            "Compatible with most portable audio devices; 3-1/3' cord; gold-plated stereo mini jack"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3316072",
        "_score": 98.27057,
        "_source": {
          "name": [
            "JVC - JVC Sport Clip Earbud Headphones - Black"
          ],
          "shortDescription": [
            "JVC Sport Clip Earbud Headphones: Rubber ear hooks; water-resistant design; sound isolating; 11mm drivers; neodymium magnets"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "8605253",
        "_score": 95.65777,
        "_source": {
          "name": [
            "JVC - Gumy Stereo Earbud Headphones - Coconut White"
          ],
          "shortDescription": [
            "From our expanded online assortment; compatible with most portable audio devices; 3-1/3' cord; gold-plated stereo mini jack"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "1232474",
        "_score": 92.01677,
        "_source": {
          "name": [
            "Beats By Dr. Dre - Beats iBeats Earbud Headphones"
          ],
          "shortDescription": [
            "3-button microphone; noise-canceling design; Duraflex protective jacket"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2197052",
        "_score": 86.037025,
        "_source": {
          "name": [
            "Sony - Earbud Headphones - Dark Blue"
          ],
          "shortDescription": [
            "13.5mm drivers; neodymium magnet; 3 sets of silicone ear cushions"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2264036",
        "_score": 85.73258,
        "_source": {
          "name": [
            "JayBird - Freedom Bluetooth Earbud Headphones"
          ],
          "shortDescription": [
            "GeckoGrip active ear tips; 6 earbud sizes; Bluetooth-ready; sound isolating; tangle-free flat cord; magnet-sealed hard shell carrying case"
          ]
        }
      }
    ]
  }
}
```

### With Synonyms
```json
Enter your query (type 'Exit' to exit): earbuds 
{
  "took": 12,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1205,
      "relation": "eq"
    },
    "max_score": 843.09705,
    "hits": [
      {
        "_index": "bbuy_products",
        "_id": "9084206",
        "_score": 843.09705,
        "_source": {
          "name": [
            "Apple\u00ae - Earbuds for Select Apple\u00ae iPod\u00ae Models"
          ],
          "shortDescription": [
            "Compatible with 4th-generation iPod nano, 120GB iPod classic and 2nd-generation iPod touch; remote for controlling music and video playback; microphone for recording voice memos"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2197043",
        "_score": 121.19351,
        "_source": {
          "name": [
            "Sony - Earbud Headphones - Black"
          ],
          "shortDescription": [
            "13.5mm drivers; neodymium magnet; 3 sets of silicone ear cushions"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3100277",
        "_score": 109.44192,
        "_source": {
          "name": [
            "Rocketfish\u2122 - Stereo Earbud Headphones"
          ],
          "shortDescription": [
            "10mm drivers; neodymium magnets; lightweight design"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2197089",
        "_score": 109.428734,
        "_source": {
          "name": [
            "Sony - Earbud Headphones - White"
          ],
          "shortDescription": [
            "13.5mm drivers; neodymium magnet; 3 sets of silicone ear cushions"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "8605459",
        "_score": 99.21863,
        "_source": {
          "name": [
            "JVC - Gumy Stereo Earbud Headphones - Olive Black"
          ],
          "shortDescription": [
            "Compatible with most portable audio devices; 3-1/3' cord; gold-plated stereo mini jack"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3316072",
        "_score": 98.27057,
        "_source": {
          "name": [
            "JVC - JVC Sport Clip Earbud Headphones - Black"
          ],
          "shortDescription": [
            "JVC Sport Clip Earbud Headphones: Rubber ear hooks; water-resistant design; sound isolating; 11mm drivers; neodymium magnets"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "8605253",
        "_score": 95.65777,
        "_source": {
          "name": [
            "JVC - Gumy Stereo Earbud Headphones - Coconut White"
          ],
          "shortDescription": [
            "From our expanded online assortment; compatible with most portable audio devices; 3-1/3' cord; gold-plated stereo mini jack"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "1232474",
        "_score": 92.01677,
        "_source": {
          "name": [
            "Beats By Dr. Dre - Beats iBeats Earbud Headphones"
          ],
          "shortDescription": [
            "3-button microphone; noise-canceling design; Duraflex protective jacket"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2197052",
        "_score": 86.037025,
        "_source": {
          "name": [
            "Sony - Earbud Headphones - Dark Blue"
          ],
          "shortDescription": [
            "13.5mm drivers; neodymium magnet; 3 sets of silicone ear cushions"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2264036",
        "_score": 85.73258,
        "_source": {
          "name": [
            "JayBird - Freedom Bluetooth Earbud Headphones"
          ],
          "shortDescription": [
            "GeckoGrip active ear tips; 6 earbud sizes; Bluetooth-ready; sound isolating; tangle-free flat cord; magnet-sealed hard shell carrying case"
          ]
        }
      }
    ]
  }
}
```


## `nespresso`

### With Synonyms
```json
Enter your query (type 'Exit' to exit): nespresso
{
  "took": 25,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 8,
      "relation": "eq"
    },
    "max_score": 0.07420327,
    "hits": [
      {
        "_index": "bbuy_products",
        "_id": "1720059",
        "_score": 0.07420327,
        "_source": {
          "name": [
            "Nespresso - Essenza Espresso Maker - Black"
          ],
          "shortDescription": [
            "Automatic and programmable; compact brewing unit technology; included Aeroccino milk frother; backlit on/off and coffee volume buttons"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3990516",
        "_score": 0.07420327,
        "_source": {
          "name": [
            "Nespresso - Essenza Espresso Maker - Black"
          ],
          "shortDescription": [
            "Makes espresso and lungo; 19-bar high-pressure pump; Thermobloc heating element; Compact Brewing Unit technology; 30-oz. removable water tank; manual volume control; backlit coffee buttons; 1260 watts of power"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3990589",
        "_score": 0.07074005,
        "_source": {
          "name": [
            "Nespresso - CitiZ Espresso Maker - Black"
          ],
          "shortDescription": [
            "Makes espresso and lungo; 19-bar high-pressure pump; automatic volume control; thermo block heating element; auto power-off after 9 minutes; folding drip tray; removable 34-oz. water tank; adaptable grid"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3990831",
        "_score": 0.07074005,
        "_source": {
          "name": [
            "Nespresso - CitiZ Espresso Maker - Red"
          ],
          "shortDescription": [
            "Makes espresso and lungo; 19-bar high-pressure pump; automatic volume control; thermo block heating element; auto power-off after 9 minutes; folding drip tray; removable 34-oz. water tank; adaptable grid"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2588376",
        "_score": 0.07073941,
        "_source": {
          "name": [
            "Nespresso - Essenza Espresso Maker - Titan Gray"
          ],
          "shortDescription": [
            "Automatic and programmable; compact unit brewing technology; included Aeroccino milk frother; backlit on/off and coffee volume buttons"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3990534",
        "_score": 0.07073941,
        "_source": {
          "name": [
            "Nespresso - Pixie Espresso Maker - Electric Aluminum"
          ],
          "shortDescription": [
            "Thermoblock heating element; 19-bar high-pressure pump; automatic volume control; folding drip tray; cable storage"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3990561",
        "_score": 0.07073941,
        "_source": {
          "name": [
            "Nespresso - Pixie Espresso Maker - Electric Titan"
          ],
          "shortDescription": [
            "Thermoblock heating element; 19-bar high-pressure pump; folding drip tray; cable storage; capsule container"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3991039",
        "_score": 0.06758508,
        "_source": {
          "name": [
            "Nespresso - CitiZ & Milk Coffeemaker - Silver Chrome"
          ],
          "shortDescription": [
            "Thermoblock heating element; froths hot or cold milk; 19-bar high-pressure pump; folding drip tray; cable storage"
          ]
        }
      }
    ]
  }
}
```

### Without Synonyms
```json
Enter your query (type 'Exit' to exit): nespresso
{
  "took": 13,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 8,
      "relation": "eq"
    },
    "max_score": 0.07420327,
    "hits": [
      {
        "_index": "bbuy_products",
        "_id": "1720059",
        "_score": 0.07420327,
        "_source": {
          "name": [
            "Nespresso - Essenza Espresso Maker - Black"
          ],
          "shortDescription": [
            "Automatic and programmable; compact brewing unit technology; included Aeroccino milk frother; backlit on/off and coffee volume buttons"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3990516",
        "_score": 0.07420327,
        "_source": {
          "name": [
            "Nespresso - Essenza Espresso Maker - Black"
          ],
          "shortDescription": [
            "Makes espresso and lungo; 19-bar high-pressure pump; Thermobloc heating element; Compact Brewing Unit technology; 30-oz. removable water tank; manual volume control; backlit coffee buttons; 1260 watts of power"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3990589",
        "_score": 0.07074005,
        "_source": {
          "name": [
            "Nespresso - CitiZ Espresso Maker - Black"
          ],
          "shortDescription": [
            "Makes espresso and lungo; 19-bar high-pressure pump; automatic volume control; thermo block heating element; auto power-off after 9 minutes; folding drip tray; removable 34-oz. water tank; adaptable grid"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3990831",
        "_score": 0.07074005,
        "_source": {
          "name": [
            "Nespresso - CitiZ Espresso Maker - Red"
          ],
          "shortDescription": [
            "Makes espresso and lungo; 19-bar high-pressure pump; automatic volume control; thermo block heating element; auto power-off after 9 minutes; folding drip tray; removable 34-oz. water tank; adaptable grid"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2588376",
        "_score": 0.07073941,
        "_source": {
          "name": [
            "Nespresso - Essenza Espresso Maker - Titan Gray"
          ],
          "shortDescription": [
            "Automatic and programmable; compact unit brewing technology; included Aeroccino milk frother; backlit on/off and coffee volume buttons"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3990534",
        "_score": 0.07073941,
        "_source": {
          "name": [
            "Nespresso - Pixie Espresso Maker - Electric Aluminum"
          ],
          "shortDescription": [
            "Thermoblock heating element; 19-bar high-pressure pump; automatic volume control; folding drip tray; cable storage"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3990561",
        "_score": 0.07073941,
        "_source": {
          "name": [
            "Nespresso - Pixie Espresso Maker - Electric Titan"
          ],
          "shortDescription": [
            "Thermoblock heating element; 19-bar high-pressure pump; folding drip tray; cable storage; capsule container"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3991039",
        "_score": 0.06758508,
        "_source": {
          "name": [
            "Nespresso - CitiZ & Milk Coffeemaker - Silver Chrome"
          ],
          "shortDescription": [
            "Thermoblock heating element; froths hot or cold milk; 19-bar high-pressure pump; folding drip tray; cable storage"
          ]
        }
      }
    ]
  }
}
```



## `dslr`

### With Synonyms
```json
Enter your query (type 'Exit' to exit): dslr
{
  "took": 155,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2837,
      "relation": "eq"
    },
    "max_score": 408.17416,
    "hits": [
      {
        "_index": "bbuy_products",
        "_id": "1980124",
        "_score": 408.17416,
        "_source": {
          "name": [
            "Canon - EOS Rebel T3i 18.0-Megapixel DSLR Camera with 18-55mm Lens - Black"
          ],
          "shortDescription": [
            "Vari-angle 3.0-inch Clear View LCD screen1080 full HD video3.7 FPS (frames per second)ISO 100-6400 (expandable to 12800)"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "1989073",
        "_score": 347.9671,
        "_source": {
          "name": [
            "Nikon - D5100 16.2-Megapixel DSLR Camera with 18-55mm VR Lens - Black"
          ],
          "shortDescription": [
            "High Resolution 16.2 MP DX-format CMOS sensor3\" Super-Density Vari-Angle LCD Monitor1080 full HD videoISO sensitivity 100-6400 (expandable to ISO 25,600 equivalent)"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "6813362",
        "_score": 193.71939,
        "_source": {
          "name": [
            "Canon - DSLR Gadget Bag - Black"
          ],
          "shortDescription": [
            "Convenient storage for Canon EOS DSLR cameras"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2705145",
        "_score": 27.712948,
        "_source": {
          "name": [
            "DigiPower - Travel Charger"
          ],
          "shortDescription": [
            "Compatible with select Canon DSLR batteries; provides uninterrupted power for your digital camera; lightweight design"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "9778635",
        "_score": 27.528584,
        "_source": {
          "name": [
            "Canon - EOS Rebel T2i 18.0-Megapixel DSLR Camera with EF-S 18-55mm Lens - Black"
          ],
          "shortDescription": [
            "3\" LCD screenFull HD videoISO 100-6400 (expandable to 12800)"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "1223834",
        "_score": 11.542395,
        "_source": {
          "name": [
            "PNY - 16GB Secure Digital High Capacity (SDHC) Class 10 Memory Card"
          ],
          "shortDescription": [
            "Compatible with most digital cameras and camcorders with a Secure Digital High Capacity slot; 16GB capacity; shock protection and RTV silicone coating"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "1227075",
        "_score": 10.8557005,
        "_source": {
          "name": [
            "PNY - 8GB Secure Digital High Capacity (SDHC) Class 10 Memory Card"
          ],
          "shortDescription": [
            "Compatible with most digital cameras and camcorders with a Secure Digital High Capacity slot; 8GB capacity; shock protection and RTV silicone coating"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3099128",
        "_score": 10.553733,
        "_source": {
          "name": [
            "Nikon - D3100 14.2-Megapixel DSLR Camera with 18-55mm VR Lens - Red"
          ],
          "shortDescription": [
            "3\" TFT-LCD display1080p full HD videoUp to 3 fpsISO 100-3200 (expandable to 12,800)"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2300602",
        "_score": 6.7035723,
        "_source": {
          "name": [
            "PNY - 32GB Secure Digital High Capacity (SDHC) Class 10 Memory Card"
          ],
          "shortDescription": [
            "Compatible with most digital cameras with a Secure Digital High Capacity slot; 32GB capacity; 20MB/sec. transfer rate"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "8758114",
        "_score": 6.677643,
        "_source": {
          "name": [
            "Canon - 55-250mm f/4-5.6 Telephoto Zoom Lens for Select Canon Cameras"
          ],
          "shortDescription": [
            "Compatible with Canon cameras with an EF-S mount; optical image stabilizer maintains clarity at slow shutter speeds; 12 elements in 10 groups"
          ]
        }
      }
    ]
  }
}
```

### Without Synonyms
```json
Enter your query (type 'Exit' to exit): dslr
{
  "took": 14,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2837,
      "relation": "eq"
    },
    "max_score": 408.17416,
    "hits": [
      {
        "_index": "bbuy_products",
        "_id": "1980124",
        "_score": 408.17416,
        "_source": {
          "name": [
            "Canon - EOS Rebel T3i 18.0-Megapixel DSLR Camera with 18-55mm Lens - Black"
          ],
          "shortDescription": [
            "Vari-angle 3.0-inch Clear View LCD screen1080 full HD video3.7 FPS (frames per second)ISO 100-6400 (expandable to 12800)"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "1989073",
        "_score": 347.9671,
        "_source": {
          "name": [
            "Nikon - D5100 16.2-Megapixel DSLR Camera with 18-55mm VR Lens - Black"
          ],
          "shortDescription": [
            "High Resolution 16.2 MP DX-format CMOS sensor3\" Super-Density Vari-Angle LCD Monitor1080 full HD videoISO sensitivity 100-6400 (expandable to ISO 25,600 equivalent)"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "6813362",
        "_score": 193.71939,
        "_source": {
          "name": [
            "Canon - DSLR Gadget Bag - Black"
          ],
          "shortDescription": [
            "Convenient storage for Canon EOS DSLR cameras"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2705145",
        "_score": 27.712948,
        "_source": {
          "name": [
            "DigiPower - Travel Charger"
          ],
          "shortDescription": [
            "Compatible with select Canon DSLR batteries; provides uninterrupted power for your digital camera; lightweight design"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "9778635",
        "_score": 27.528584,
        "_source": {
          "name": [
            "Canon - EOS Rebel T2i 18.0-Megapixel DSLR Camera with EF-S 18-55mm Lens - Black"
          ],
          "shortDescription": [
            "3\" LCD screenFull HD videoISO 100-6400 (expandable to 12800)"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "1223834",
        "_score": 11.542395,
        "_source": {
          "name": [
            "PNY - 16GB Secure Digital High Capacity (SDHC) Class 10 Memory Card"
          ],
          "shortDescription": [
            "Compatible with most digital cameras and camcorders with a Secure Digital High Capacity slot; 16GB capacity; shock protection and RTV silicone coating"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "1227075",
        "_score": 10.8557005,
        "_source": {
          "name": [
            "PNY - 8GB Secure Digital High Capacity (SDHC) Class 10 Memory Card"
          ],
          "shortDescription": [
            "Compatible with most digital cameras and camcorders with a Secure Digital High Capacity slot; 8GB capacity; shock protection and RTV silicone coating"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "3099128",
        "_score": 10.553733,
        "_source": {
          "name": [
            "Nikon - D3100 14.2-Megapixel DSLR Camera with 18-55mm VR Lens - Red"
          ],
          "shortDescription": [
            "3\" TFT-LCD display1080p full HD videoUp to 3 fpsISO 100-3200 (expandable to 12,800)"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "2300602",
        "_score": 6.7035723,
        "_source": {
          "name": [
            "PNY - 32GB Secure Digital High Capacity (SDHC) Class 10 Memory Card"
          ],
          "shortDescription": [
            "Compatible with most digital cameras with a Secure Digital High Capacity slot; 32GB capacity; 20MB/sec. transfer rate"
          ]
        }
      },
      {
        "_index": "bbuy_products",
        "_id": "8758114",
        "_score": 6.677643,
        "_source": {
          "name": [
            "Canon - 55-250mm f/4-5.6 Telephoto Zoom Lens for Select Canon Cameras"
          ],
          "shortDescription": [
            "Compatible with Canon cameras with an EF-S mount; optical image stabilizer maintains clarity at slow shutter speeds; 12 elements in 10 groups"
          ]
        }
      }
    ]
  }
}
```


## OpenSearch query:
```bash
GET /bbuy_products/_search
{
  "size": 10,
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "name.synonyms": {
              "query": "nespresso",
              "fuzziness": "1",
              "prefix_length": 2
            }
          }
        },
        {
          "match_phrase": {
            "name.hyphens": {
              "query": "nespresso",
              "slop": 1
            }
          }
        },
        {
          "multi_match": {
            "query": "nespresso",
            "type": "phrase",
            "slop": "6",
            "fields": [
              "name.synonyms^10",
              "name.hyphens^10",
              "shortDescription^5",
              "longDescription^5",
              "department^0.5",
              "sku",
              "manufacturer",
              "features",
              "categoryPath"
            ]
          }
        }
      ],
      "filter": []
    }
  }
}
```

Output:
```bash
{
  "took": 9,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 8,
      "relation": "eq"
    },
    "max_score": 148.75043,
    "hits": [
      {
        "_index": "bbuy_products",
        "_id": "1720059",
        "_score": 148.75043,
        "_source": {
          "productId": [
            "1218285823699"
          ],
          "sku": [
            "1720059"
          ],
          "name": [
            "Nespresso - Essenza Espresso Maker - Black"
          ],
          "type": [
            "HardGood"
          ],
          "startDate": [
            "2010-12-30"
          ],
          "active": [
            "false"
          ],
          ...
```