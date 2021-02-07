# Depth_Peeling_for_Point_Cloud

## Visualization of peeling process
### Noise Point Clouds
|Gaussian noise (10%)|Outlier noise (10%)|
|:-:|:-:|
|<img src="figures/funehoko_gif/funehoko-gaussian-10per.gif">|<img src="figures/funehoko_gif/funehoko-outlier-10per.gif">|

### Various Number of Points
|400,000 points (1%)|2,000,000 points (5%)|
|:-:|:-:|
|<img src="figures/atago_gif/atago_1per_slow.gif">|<img src="figures/atago_gif/atago_5per_slow.gif">|

|4,000,000 points (10%)|1,0000,000 points (25%)|
|:-:|:-:|
|<img src="figures/atago_gif/atago_10per_slow.gif">|<img src="figures/atago_gif/atago_25per_slow.gif">|

## New Command
```
#/LayerLevel 1
```

## Usage
```
$ sh config_dp.sh
$ make
$ make install

$ make test_ply_ascii
$ make test_ply_binary
$ make test_spbr_ascii
$ make test_spbr_binary
```


### Example
```
$ cat .param.spbr
#/LayerLevel 20

$ ./dp input.ply

===== Depth Peeling for Point Cloud =====

                2021/02/07
              Tomomasa Uchida
           Ritsumeikan University

 USAGE : dp file1.spbr file2.spbr ...
 HELP  : dp -h

~~~

Executing Depth Peeling "20" times...
Done! ( 0.3871 [sec] )

Automatically, snapshotted.
Saved image path: IMAGE_DATA/OUTPUT_LAYER_IMAGES/LayerImageX.bmp
```

<!-- ## Visualization Results

|Layer1|Layer5|Layer10|
|:-:|:-:|:-:|
|<img src="figures/LayerLevel1.bmp">|<img src="figures/LayerLevel5.bmp">|<img src="figures/LayerLevel10.bmp">|

|Layer20|Layer30|Layer40|
|:-:|:-:|:-:|
|<img src="figures/LayerLevel20.bmp">|<img src="figures/LayerLevel30.bmp">|<img src="figures/LayerLevel40.bmp">|

|Layer50|Layer60|Layer70|
|:-:|:-:|:-:|
|<img src="figures/LayerLevel50.bmp">|<img src="figures/LayerLevel60.bmp">|<img src="figures/LayerLevel70.bmp">|

|Layer80|Layer90|Layer100|
|:-:|:-:|:-:|
|<img src="figures/LayerLevel80.bmp">|<img src="figures/LayerLevel90.bmp">|<img src="figures/LayerLevel100.bmp">| -->

<!-- ## Layer Image Averaging
|Original|Layer1-5|Layer1-10|
|:-:|:-:|:-:|
|<img src="figures/LayerAvg/original.bmp">|<img src="figures/LayerAvg/Layer_Averaging_L1-5.png">|<img src="figures/LayerAvg/Layer_Averaging_L1-10.png">| -->