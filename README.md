# Deep Learning for the Classification of Adult Images and its Utilization in Social Applications

A chat application that is capable of identifying and masking pornographic images is developed. `3 Models` are used as part of this project:

1. MobileNet v1
2. MobileNet v2
3. Inception v3

The project includes two `iOS Application`:

1. APITest 
2. ChatApplication

The project includes code to create an `API endpoint` to for serving iOS Applications

#### Project requirements:

- [x] Swift 4
- [x] XCode 11.1
- [x] TensorFlow 1.12.3
- [x] Python 3.6
- [x] Django


### Steps to run the iOS Applications:

1. Open the terminal and go to the ChatApplication Folder

2. Install the required pods by running the following command in the terminal: pod install 
(If the command was not recognised, Cocoa-pods may not be installed on the computer. To get Cocoa-pods refer to: https://guides.cocoapods.org/using/getting-started.html)

3. Open ChatApplication.xcworkspace within the ChatApplication Folder in Xcode 11.1 or later

4. Select a Simulator or Device within Xcode.

5. Build and Run the project by clicking the button with the play icon in the main menu.

6. Done

#### Dependencies used for iOS Application:

**Alamofire:** Alamofire is a Swift-based HTTP networking library for iOS and macOS. It is used in this application to consume the Nectar service endpoint. (https://github.com/Alamofire/Alamofire.git)

**GeoFire:** GeoFire is an open-source library that allows you to store and query a set of keys based on their geographic location. It is used in this application to perform geo-quires to view application users that are in close proximity of the local user. ('https://github.com/firebase/geofire-objc.git')

**SwiftOverlays:** It is a Swift-based library that is used to display blocking overlays. (https://github.com/peterprokop/SwiftOverlays.git)

**lottie-ios:** It is a library that renders After Effects animations in real time. It is used in this application to display animations. (https://github.com/airbnb/lottie-ios.git)

### Steps to train / test models:

1. Go to `<model_name>` folder.
2. To Train - `python train.py`.
3. To Test - `python test.py`.

### Steps to run API endpoint:

1. Go to models_endpoint.2
2. `python manage.py runserver 0:80`

#### Dependencies used for Python Models:

- [x] pip install requirements.txt

#### Extra information to test the test image:

* http://45.113.235.180:80/mobilenetV1/test
* http://45.113.235.180:80/mobilenetV2/test
* http://45.113.235.180:80/inceptionV3/test